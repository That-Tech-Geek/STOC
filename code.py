import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Function to download data and calculate additional metrics
def download_data(ticker, start_date, end_date):
    # Download historical data
    quote_summary = yf.download(ticker, start=start_date, end=end_date)
    
    if not quote_summary.empty:
        # Extract financial data
        t = yf.Ticker(ticker)
        data = t.info
        
        # Create a DataFrame with day-wise data
        df = quote_summary.reset_index()
        df['Symbol'] = ticker
        df['Sector'] = data.get('sector', 'N/A')
        df['Industry'] = data.get('industry', 'N/A')
        df['Market'] = data.get('market', 'N/A')
        df['QuoteType'] = data.get('quoteType', 'N/A')
        df['Debt-to-Equity Ratio'] = data.get('debtToEquity', None)
        df['Current Ratio'] = data.get('currentRatio', None)
        df['Earning per Share'] = data.get('trailingEps', None)
        df['Variability Index'] = (df['High'] - df['Low']) / df['Low']
        df['Dividend Yield'] = data.get('dividendYield', None)
        
        return df
    else:
        st.error("No data available for the given ticker.")
        return pd.DataFrame()

# Function to plot data
def plot_data(df):
    if not df.empty:
        st.subheader("Close Price")
        st.line_chart(df.set_index('Date')['Close'])

        st.subheader("Variability Index")
        st.line_chart(df.set_index('Date')['Variability Index'])

        st.subheader("Open vs Close")
        st.line_chart(df.set_index('Date')[['Open', 'Close']])

        st.subheader("High vs Low")
        st.line_chart(df.set_index('Date')[['High', 'Low']])

        st.subheader("Close vs Adjusted Close")
        st.line_chart(df.set_index('Date')[['Close', 'Adj Close']])

# Streamlit app layout
st.title("Welcome to STOC, The open-source Stock Visualiser!")
st.write("In case you are unaware of the ticker of the company, feel free to look it up at https://docs.google.com/spreadsheets/d/e/2PACX-1vQCLhtWX-fxnIxqLGrUUgZNtstUvkYztRKHYegInZqTFfzCzXoUOT77nZ2o5DZn33b6g7ydCwH2Kea2/pubhtml")
# User input
ticker = st.text_input("Enter the ticker symbol of the company (e.g., AAPL for Apple, RELIANCE for Reliance Industries):")
exchange = st.selectbox("Select the exchange:", ["NASDAQ", "NSE"])
submit_button = st.button("Submit")

if submit_button:
    if ticker and exchange:
        ticker = ticker.strip().upper()
        
        # Add suffix for NSE
        if exchange == "NSE":
            ticker = f"{ticker}.NS"
        
        st.write(f"Fetching data for ticker: {ticker}")

        # Download data
        df = download_data(ticker, start_date="1924-01-01", end_date="2024-07-04")

        if not df.empty:
            # Plot data
            plot_data(df)
            
            # Save to CSV
            csv_file_path = f"{ticker}.csv"
            df.to_csv(csv_file_path, index=False)
            st.success(f"Data extracted and saved for {ticker}.")
            st.download_button(label="Download CSV", data=df.to_csv().encode('utf-8'), file_name=csv_file_path, mime='text/csv')
    else:
        st.error("Please provide the ticker symbol and select the exchange.")
