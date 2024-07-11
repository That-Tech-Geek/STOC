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

# Function to detect numeric columns
def get_numeric_columns(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    return numeric_cols

# Function to plot time series and correlation graphs
def plot_graphs(df, numeric_cols):
    if len(numeric_cols) > 1:
        fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(12, 6 * len(numeric_cols)))

        for i, col in enumerate(numeric_cols):
            axes[i].plot(df['Date'], df[col], label=col)
            axes[i].set_xlabel('Date')
            axes[i].set_ylabel(col)
            axes[i].legend()
        
        plt.tight_layout()
        st.pyplot(fig)

        # Plot correlation heatmap
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Select at least two numeric columns to plot correlations.")

# Main function to run the app
def main():
    st.title("Welcome to STOC, the Stock Trading Optimisation Console")

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
                numeric_cols = get_numeric_columns(df)

                if numeric_cols:
                    st.write("Numeric columns detected:")
                    st.write(numeric_cols)

                    plot_graphs(df, numeric_cols)
                else:
                    st.warning("No numeric columns found in the downloaded data.")
        else:
            st.error("Please provide the ticker symbol and select the exchange.")

if __name__ == "__main__":
    main()
