import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

# Dictionary to map exchanges to suffixes
exchange_suffixes = {
    "NYSE": "",
    "NASDAQ": "",
    "BSE": "",
    "NSE": ".NS",
    "Cboe Indices": ".CI",
    "Chicago Board of Trade (CBOT)***": ".CBT",
    "Chicago Mercantile Exchange (CME)***": ".CME",
    "Dow Jones Indexes": ".DJ",
    "Nasdaq Stock Exchange": ".NSQ",
    "ICE Futures US": ".NYB",
    "New York Commodities Exchange (COMEX)***": ".CMX",
    "New York Mercantile Exchange (NYMEX)***": ".NYM",
    "Options Price Reporting Authority (OPRA)": ".OPR",
    "OTC Markets Group**": ".OTC",
    "S & P Indices": ".SP",
    "Buenos Aires Stock Exchange (BYMA)": ".BA",
    "Vienna Stock Exchange": ".VI",
    "Australian Stock Exchange (ASX)": ".AX",
    "Cboe Australia": ".CBA",
    "Euronext Brussels": ".BR",
    "Sao Paolo Stock Exchange (BOVESPA)": ".SA",
    "Canadian Securities Exchange": ".CN",
    "Cboe Canada": ".CBOE",
    "Toronto Stock Exchange (TSX)": ".TO",
    "TSX Venture Exchange (TSXV)": ".TV",
    "Santiago Stock Exchange": ".SN",
    "Shanghai Stock Exchange": ".SS",
    "Shenzhen Stock Exchange": ".SZ",
    "Prague Stock Exchange Index": ".PR",
    "Nasdaq OMX Copenhagen": ".CO",
    "Egyptian Exchange Index (EGID)": ".CA",
    "Nasdaq OMX Tallinn": ".TL",
    "Cboe Europe": ".CE",
    "Euronext": ".EU",
    "Nasdaq OMX Helsinki": ".HE",
    "Euronext Paris": ".PA",
    "Berlin Stock Exchange": ".BE",
    "Bremen Stock Exchange": ".BM",
    "Dusseldorf Stock Exchange": ".DU",
    "Frankfurt Stock Exchange": ".F",
    "Hamburg Stock Exchange": ".HM",
    "Hanover Stock Exchange": ".HA",
    "Munich Stock Exchange": ".MU",
    "Stuttgart Stock Exchange": ".SG",
    "Deutsche Boerse XETRA": ".DE",
    "Collectable Indices": ".REGA",
    "Cryptocurrencies": "",
    "Currency Rates": ".X",
    "MSCI Indices": ".MSCI",
    "Athens Stock Exchange (ATHEX)": ".AT",
    "Hang Seng Indices": ".HSI",
    "Hong Kong Stock Exchange (HKEX)*": ".HK",
    "Budapest Stock Exchange": ".BD",
    "Nasdaq OMX Iceland": ".IC",
    "Bombay Stock Exchange": ".BO",
    "National Stock Exchange of India": ".NS",
    "Indonesia Stock Exchange (IDX)": ".JK",
    "Euronext Dublin": ".ID",
    "Tel Aviv Stock Exchange": ".TA",
    "EuroTLX": ".TLX",
    "Italian Stock Exchange": ".MI",
    "Nikkei Indices": ".NIKKEI",
    "Tokyo Stock Exchange": ".T",
    "Boursa Kuwait": ".KW",
    "Nasdaq OMX Riga": ".RG",
    "Nasdaq OMX Vilnius": ".VL",
    "Malaysian Stock Exchange": ".KL",
    "Mexico Stock Exchange (BMV)": ".MX",
    "Euronext Amsterdam": ".AS",
    "New Zealand Stock Exchange (NZX)": ".NZ",
    "Oslo Stock Exchange": ".OL",
    "Philippine Stock Exchange Indices": ".PS",
    "Warsaw Stock Exchange": ".WA",
    "Euronext Lisbon": ".LS",
    "Qatar Stock Exchange": ".QA",
    "Bucharest Stock Exchange": ".RO",
    "Singapore Stock Exchange (SGX)": ".SI",
    "Johannesburg Stock Exchange": ".JO",
    "Korea Stock Exchange": ".KS",
    "KOSDAQ": ".KQ",
    "Madrid SE C.A.T.S.": ".MC",
    "Saudi Stock Exchange (Tadawul)": ".SAU",
    "Nasdaq OMX Stockholm": ".ST",
    "Swiss Exchange (SIX)": ".SW",
    "Taiwan OTC Exchange": ".TWO",
    "Taiwan Stock Exchange (TWSE)": ".TW",
    "Stock Exchange of Thailand (SET)": ".BK",
    "Borsa İstanbul": ".IS",
    "Dubai Financial Market": ".AE",
    "Cboe UK": ".CUK",
    "FTSE Indices": ".FTSE",
    "London Stock Exchange": ".L",
    "Caracas Stock Exchange": ".CR"
}

# Function to download data and calculate additional metrics
def download_data(ticker, exchange, start_date, end_date):
    suffix = exchange_suffixes.get(exchange, "")
    if suffix:
        ticker = f"{ticker}{suffix}"

    quote_summary = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if not quote_summary.empty:
        t = yf.Ticker(ticker)
        data = t.info

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
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(df['Date'], df['Close'], label='Close Price', color='blue')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Close Price', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.plot(df['Date'], df['Variability Index'], label='Variability Index', color='green')
        ax2.set_ylabel('Variability Index', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        ax1.set_title(f"Stock Data Analysis for {df['Symbol'].iloc[0]}")
        fig.tight_layout()
        st.pyplot(fig)

# Function to detect numeric columns
def get_numeric_columns(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    return numeric_cols

# Function to edit numeric columns
def edit_columns(numeric_cols):
    edited_cols = st.multiselect("Select numeric columns to include", numeric_cols, default=numeric_cols)
    return edited_cols

# Function to plot correlation graphs
def plot_correlations(df, cols):
    if len(cols) > 1:
        corr = df[cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Select at least two numeric columns to plot correlations.")

# Main function to run the app
def main():
    st.title("Company Data Downloader and Analyzer")

    ticker = st.text_input("Enter the ticker symbol of the company (e.g., AAPL for Apple, RELIANCE for Reliance Industries):")
    exchange = st.selectbox("Select the exchange:", [""] + list(exchange_suffixes.keys()))
    start_date = st.date_input("Enter the start date:")
    end_date = st.date_input("Enter the end date (optional):")

    submit_button = st.button("Submit")

    if submit_button:
        if ticker and exchange:
            ticker = ticker.strip().upper()

            st.write(f"Fetching data for ticker: {ticker} from exchange: {exchange}")

            start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
            end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

            df = download_data(ticker, exchange, start_date=start_date_str, end_date=end_date_str)

            if not df.empty:
                plot_data(df)

                csv_file_path = f"{ticker}.csv"
                df.to_csv(csv_file_path, index=False)
                st.success(f"Data extracted and saved for {ticker} from exchange: {exchange}.")
                st.download_button(label="Download CSV", data=df.to_csv().encode('utf-8'), file_name=csv_file_path, mime='text/csv')
        else:
            st.error("Please provide the ticker symbol and select the exchange.")

    st.title("Correlation Graphs for Numeric Columns")

    if 'df' in locals() and not df.empty:
        numeric_cols = get_numeric_columns(df)

        if numeric_cols:
            st.write("Numeric columns detected:")
            st.write(numeric_cols)

            edited_cols = edit_columns(numeric_cols)

            if st.button("Generate Correlation Graphs"):
                plot_correlations(df, edited_cols)
        else:
            st.warning("No numeric columns found in the downloaded data.")
    else:
        st.info("Please download data to proceed with correlation analysis.")

if __name__ == "__main__":
    main()
