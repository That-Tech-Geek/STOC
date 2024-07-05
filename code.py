import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Create a Streamlit app
st.title("Stock Data Analyzer")

# Get user input for stock ticker and date range
stock_ticker = st.text_input("Enter stock ticker (e.g. AAPL): ")
start_date = st.date_input("Select start date:")
end_date = st.date_input("Select end date:")

# Load data from Yahoo Finance
@st.cache
def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start_date, end_date)
    return data

data = load_data(stock_ticker, start_date, end_date)

# Calculate additional metrics
data["Variability Index"] = data["Close"].rolling(window=20).std()
data["Dividend Yield"] = data["Dividends"] / data["Close"]
data["Debt-to-Equity Ratio"] = data["Total Debt"] / data["Total Equity"]
data["Current Ratio"] = data["Total Current Assets"] / data["Total Current Liabilities"]

# Create plots
fig, axs = plt.subplots(3, 2, figsize=(15, 15))

axs[0, 0].plot(data["Close"])
axs[0, 0].set_title("Closing Price")

axs[0, 1].plot(data["Variability Index"])
axs[0, 1].set_title("Variability Index")

axs[1, 0].plot(data["Volume"])
axs[1, 0].set_title("Trade Volume")

axs[1, 1].plot(data["Adj Close"])
axs[1, 1].set_title("Adjusted Closing Price")

axs[2, 0].plot(data["Close"], label="Closing Price")
axs[2, 0].plot(data["Adj Close"], label="Adjusted Closing Price")
axs[2, 0].legend()
axs[2, 0].set_title("Closing vs. Adjusted Closing Price")

axs[2, 1].plot(data["Open"], label="Opening Price")
axs[2, 1].plot(data["Close"], label="Closing Price")
axs[2, 1].legend()
axs[2, 1].set_title("Opening vs. Closing Price")

st.pyplot(fig)
