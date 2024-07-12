import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

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
    # Determine suffix based on exchange selection
    suffix = exchange_suffixes.get(exchange, "")

    # Concatenate suffix to ticker if it's not empty
    if suffix:
        ticker = f"{ticker}{suffix}"

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
        df['Variability Index'] = (df['High'] - df['Low']) / df['Low']
        
        return df
    else:
        st.error("No data available for the given ticker.")
        return pd.DataFrame()

# Function to plot data
def plot_data(df):
    if not df.empty:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in ['Debt-to-Equity Ratio', 'Current Ratio']]
        
        plt.style.use('dark_background')

        for col in numeric_cols:
            if col != 'Date':
                st.subheader(f"Time Series of {col}")
                fig, ax = plt.subplots()
                ax.plot(df['Date'], df[col], color='blue')
                ax.set_xlabel('Date', color='white')
                ax.set_ylabel(col, color='white')
                ax.set_title(f"{col} over Time", color='white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.grid(True, color='white')
                st.pyplot(fig)

        if len(numeric_cols) > 1:
            st.subheader("Correlation Heatmap")
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            ax.set_facecolor('black')
            st.pyplot(fig)

# Streamlit app layout
st.title("Company Data Downloader and Analyzer")

# User input
ticker = st.text_input("Enter the ticker symbol of the company (e.g., AAPL for Apple, RELIANCE for Reliance Industries):")
exchange = st.selectbox("Select the exchange:", [""] + list(exchange_suffixes.keys()))
start_date = st.date_input("Enter the start date:")
end_date = st.date_input("Enter the end date (optional):")

submit_button = st.button("Submit")

if submit_button:
    if ticker and exchange:
        ticker = ticker.strip().upper()
        
        st.write(f"Fetching data for ticker: {ticker} from exchange: {exchange}")

        # Convert start_date and end_date to string format if not None
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

        # Download data
        df = download_data(ticker, exchange, start_date=start_date_str, end_date=end_date_str)

        if not df.empty:
            # Plot data
            plot_data(df)
            
            # Save to CSV
            csv_file_path = f"{ticker}.csv"
            df.to_csv(csv_file_path, index=False)
            st.success(f"Data extracted and saved for {ticker} from exchange: {exchange}.")
            st.download_button(label="Download CSV", data=df.to_csv().encode('utf-8'), file_name=csv_file_path, mime='text/csv')
    else:
        st.error("Please provide the ticker symbol and select the exchange.")
