import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
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
    # Determine suffix based on exchange selection
    suffix = exchange_suffixes.get(exchange, "")

    # Concatenate suffix to ticker if it's not empty
    if suffix:
        ticker = f"{ticker}{suffix}"

    # Download historical data
    quote_summary = yf.download(ticker, start=start_date, end=end_date, progress=False)

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

# Function to fetch national average data
def fetch_national_average(exchange, start_date, end_date):
    # Initialize an empty DataFrame
    national_avg_data = pd.DataFrame()

    # Fetch data for each exchange suffix available in exchange_suffixes
    for exch, suffix in exchange_suffixes.items():
        if suffix:  # Only fetch if a suffix is provided
            index_ticker = f"{exch}{suffix}"
            index_data = yf.download(index_ticker, start=start_date, end=end_date, progress=False)
            if not index_data.empty:
                index_data['Exchange'] = exch
                national_avg_data = pd.concat([national_avg_data, index_data], axis=0)

    return national_avg_data

# Function to plot comparison graph
def plot_comparison(company_data, national_avg_data):
    if not company_data.empty and not national_avg_data.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(company_data['Date'], company_data['Adj Close'], label=f"{company_data['Symbol'].iloc[0]}")
        
        # Plot each national average by exchange
        for exch in national_avg_data['Exchange'].unique():
            exch_data = national_avg_data[national_avg_data['Exchange'] == exch]
            plt.plot(exch_data.index, exch_data['Adj Close'], label=f"{exch} National Average", linestyle='--')

        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.title(f"{company_data['Symbol'].iloc[0]} vs National Averages")
        plt.legend()
        st.pyplot()
    else:
        st.warning("No data available for comparison.")

# Custom CSS to set background to black
st.markdown(
    """
    <style>
    body {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to STOC, the Share Trading Optimisation Console!")

# User input
ticker = st.text_input("Enter the ticker symbol of the company (e.g., AAPL for Apple, RELIANCE for Reliance Industries):")
exchange = st.selectbox("Select the exchange:", [""] + list(exchange_suffixes.keys()))
start_date = st.date_input("Enter the start date:")

# Maximum possible end date
end_date = st.date_input("Enter the end date (optional):", max_value=pd.Timestamp.today() + pd.DateOffset(years=10))

submit_button = st.button("Submit")

if submit_button:
    if ticker and exchange:
        ticker = ticker.strip().upper()
        
        st.write(f"Fetching data for ticker: {ticker} from exchange: {exchange}")

        # Convert start_date and end_date to string format if not None
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

        # Download data
        company_data = download_data(ticker, exchange, start_date=start_date_str, end_date=end_date_str)
        national_avg_data = fetch_national_average(exchange, start_date=start_date_str, end_date=end_date_str)

        if not company_data.empty and not national_avg_data.empty:
            plot_comparison(company_data, national_avg_data)
        national_avg_data = fetch_national_average(exchange, start_date=start_date_str, end_date=end_date_str)

        if not company_data.empty and not national_avg_data.empty:
            plot_comparison(company_data, national_avg_data)
