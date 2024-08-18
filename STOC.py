import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr
import plotly.express as px
import timedelta
from datetime import date, timedelta
import yagmail 

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

# Dictionary mapping exchanges to their major indices or benchmarks
exchange_indices = {
    "NYSE": "^GSPC",  # S&P 500
    "NASDAQ": "^IXIC",  # NASDAQ Composite
    "BSE": "^BSESN",  # SENSEX
    "NSE": "^NSEI",  # NIFTY 50
    "Cboe Indices": "^VIX",  # Cboe Volatility Index (VIX)
    "Chicago Board of Trade (CBOT)***": "^VIX",  # S&P 500 VIX (example, needs actual ticker)
    "Chicago Mercantile Exchange (CME)***": "CME",  # CME Group (example, needs actual ticker)
    "Dow Jones Indexes": "^DJI",  # Dow Jones Industrial Average
    "Nasdaq Stock Exchange": "^IXIC",  # NASDAQ Composite
    "ICE Futures US": "^RUT",  # Russell 2000
    "New York Commodities Exchange (COMEX)***": "GC=F",  # COMEX Gold (example, needs actual ticker)
    "New York Mercantile Exchange (NYMEX)***": "CL=F",  # NYMEX Crude Oil (example, needs actual ticker)
    "Options Price Reporting Authority (OPRA)": "OPRA",  # OPRA Index (example, needs actual ticker)
    "OTC Markets Group**": "OTCM",  # OTCQX Best Market (example, needs actual ticker)
    "S & P Indices": "^GSPC",  # S&P 500
    "Buenos Aires Stock Exchange (BYMA)": "^MERV",  # MERVAL
    "Vienna Stock Exchange": "^ATX",  # ATX
    "Australian Stock Exchange (ASX)": "^AXJO",  # S&P/ASX 200
    "Cboe Australia": "^XVI",  # S&P/ASX 200 VIX (example, needs actual ticker)
    "Euronext Brussels": "^BFX",  # BEL 20
    "Sao Paolo Stock Exchange (BOVESPA)": "^BVSP",  # IBOVESPA
    "Canadian Securities Exchange": "^GSPTSE",  # S&P/TSX Composite
    "Cboe Canada": "^VIXC",  # S&P/TSX Composite VIX (example, needs actual ticker)
    "Toronto Stock Exchange (TSX)": "^GSPTSE",  # S&P/TSX Composite
    "TSX Venture Exchange (TSXV)": "^JX",  # TSX Venture Composite (example, needs actual ticker)
    "Santiago Stock Exchange": "^IPSA",  # IPSA
    "Shanghai Stock Exchange": "000001.SS",  # SSE Composite Index
    "Shenzhen Stock Exchange": "399001.SZ",  # SZSE Component Index
    "Prague Stock Exchange Index": "^PX",  # PX
    "Nasdaq OMX Copenhagen": "^OMXC25",  # OMX Copenhagen 25
    "Egyptian Exchange Index (EGID)": "^EGX30.CA",  # EGX 30
    "Nasdaq OMX Tallinn": "^OMXTGI",  # OMX Tallinn
    "Cboe Europe": "^STOXX50E",  # EURO STOXX 50
    "Euronext": "^N100",  # Euronext 100
    "Nasdaq OMX Helsinki": "^OMXH25",  # OMX Helsinki 25
    "Euronext Paris": "^FCHI",  # CAC 40
    "Berlin Stock Exchange": "^GDAXI",  # DAX
    "Bremen Stock Exchange": "BREXIT",  # BREXIT (example, needs actual ticker)
    "Dusseldorf Stock Exchange": "^GDAXI",  # DAX
    "Frankfurt Stock Exchange": "^GDAXI",  # DAX
    "Hamburg Stock Exchange": "BREXIT",  # BREXIT (example, needs actual ticker)
    "Hanover Stock Exchange": "BREXIT",  # BREXIT (example, needs actual ticker)
    "Munich Stock Exchange": "^GDAXI",  # DAX
    "Stuttgart Stock Exchange": "BREXIT",  # BREXIT (example, needs actual ticker)
    "Deutsche Boerse XETRA": "^GDAXI",  # DAX
    "Collectable Indices": "COLLECT",  # COLLECT (example, needs actual ticker)
    "Cryptocurrencies": "CRYPTO",  # CRYPTO (example, needs actual ticker)
    "Currency Rates": "CURRENCY",  # CURRENCY (example, needs actual ticker)
    "MSCI Indices": "MSCI",  # MSCI (example, needs actual ticker)
    "Athens Stock Exchange (ATHEX)": "^ATG",  # ASE
    "Hang Seng Indices": "^HSI",  # HANG SENG
    "Hong Kong Stock Exchange (HKEX)*": "^HSI",  # HANG SENG
    "Budapest Stock Exchange": "^BUX",  # BUX
    "Nasdaq OMX Iceland": "^OMXICELAND",  # OMX
    "Bombay Stock Exchange": "^BSESN",  # BSE
    "National Stock Exchange of India": "^NSEI",  # NSE
    "Indonesia Stock Exchange (IDX)": "^JKSE",  # IDX
    "Euronext Dublin": "^ISEQ",  # INDEX (example, needs actual ticker)
    "Tel Aviv Stock Exchange": "^TA125.TA",  # TEL AVIV
    "EuroTLX": "^TLX",  # EURO TLX (example, needs actual ticker)
    "Italian Stock Exchange": "FTSEMIB.MI",  # ITALY (example, needs actual ticker)
    "Nikkei Indices": "^N225",  # NIKKEI
    "Tokyo Stock Exchange": "^TPX",  # TOKYO (example, needs actual ticker)
    "Boursa Kuwait": "^KWSE",  # KW (example, needs actual ticker)
    "Nasdaq OMX Riga": "^OMXRGI",  # RIGA
    "Nasdaq OMX Vilnius": "^OMXVGI",  # VILNIUS
    "Malaysian Stock Exchange": "^KLSE",  # MALAYSIA (example, needs actual ticker)
    "Mexico Stock Exchange (BMV)": "^MXX",  # BMV (example, needs actual ticker)
    "Euronext Amsterdam": "^AEX",  # EUROPE (example, needs actual ticker)
    "New Zealand Stock Exchange (NZX)": "^NZ50",  # NZX (example, needs actual ticker)
    "Oslo Stock Exchange": "^OSEAX",  # OSLO (example, needs actual ticker)
    "Philippine Stock Exchange Indices": "^PSEi",  # PHILIPPINES (example, needs actual ticker)
    "Warsaw Stock Exchange": "^WIG",  # WSE (example, needs actual ticker)
    "Euronext Lisbon": "^PSI20",  # LISBON (example, needs actual ticker)
    "Qatar Stock Exchange": "^QSI",  # QATAR (example, needs actual ticker)
    "Bucharest Stock Exchange": "^BET",  # BUCHAREST (example, needs actual ticker)
    "Singapore Stock Exchange (SGX)": "^STI",  # SGX (example, needs actual ticker)
    "Johannesburg Stock Exchange": "^J203.JO",  # JOHANNESBURG (example, needs actual ticker)
    "Korea Stock Exchange": "^KS11",  # KOREA (example, needs actual ticker)
    "KOSDAQ": "^KQ11",  # KOSDAQ (example, needs actual ticker)
    "Madrid SE C.A.T.S.": "^IBEX",  # MADRID (example, needs actual ticker)
    "Saudi Stock Exchange (Tadawul)": "^TASI.SR",  # TADAWUL (example, needs actual ticker)
    "Nasdaq OMX Stockholm": "^OMX",  # OMX (example, needs actual ticker)
    "Swiss Exchange (SIX)": "^SSMI",  # SIX (example, needs actual ticker)
    "Taiwan OTC Exchange": "^TWO",  # OTC (example, needs actual ticker)
    "Taiwan Stock Exchange (TWSE)": "^TWII",  # TWSE (example, needs actual ticker)
    "Stock Exchange of Thailand (SET)": "^SET.BK",  # SET (example, needs actual ticker)
    "Borsa İstanbul": "^XU100",  # ISTANBUL (example, needs actual ticker)
    "Dubai Financial Market": "^DFMGI",  # DFM (example, needs actual ticker)
    "Cboe UK": "^UKX",  # UK (example, needs actual ticker)
    "FTSE Indices": "^FTSE",  # FTSE (example, needs actual ticker)
    "London Stock Exchange": "^FTSE",  # LSE (example, needs actual ticker)
    "Caracas Stock Exchange": "^IBC"
}

market_cap_categories = {
    "Mega-cap": 200e9,
    "Large-cap": 10e9,# Function to fetch data
def fetch_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, progress=False)
    # Keep only the specified columns
    data = data[['Open', 'Close', 'Volume', 'High', 'Low', 'Adj Close']]
    return data

# Function to plot time series data
def plot_time_series(data):
    st.header("Time Series Data")
    columns_to_plot = ['Open', 'Close', 'Volume', 'High', 'Low', 'Adj Close']
    for col in columns_to_plot:
        st.subheader(f"{col} over time")
        plt.style.use('dark_background')  # Set plot background to black
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data.index, data[col], color='blue')  # Set plot color to blue
        ax.set_xlabel('Time')
        ax.set_ylabel(col)
        ax.grid(color='white')  # Set gridline color to white
        ax.set_facecolor('black')  # Set axis background to black
        ax.spines['bottom'].set_color('black')  # Set axis spines to black
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['left'].set_color('black')
        st.pyplot(fig)

# Function to plot correlation heatmap
def plot_correlation_heatmap(data):
    st.header("Correlation Heatmap")
    corr = data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Function to display mean and median
def display_mean_median(data):
    st.header("Mean and Median Values")
    mean_values = data.mean()
    median_values = data.median()
    summary = pd.DataFrame({'Mean': mean_values, 'Median': median_values})
    st.dataframe(summary)

# Function to display summary statistics
def display_summary_statistics(data):
    st.header("Summary Statistics")
    summary_stats = data.describe()
    st.dataframe(summary_stats)

# Function to plot Volatility Index (VIX)
def plot_vix(start_date, end_date):
    st.header("Volatility Index (VIX)")
    vix_data = yf.download('^VIX', start=start_date, end=end_date, progress=False)
    plt.style.use('dark_background')  # Set plot background to black
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(vix_data.index, vix_data['Close'], color='blue')  # Set plot color to blue
    ax.set_xlabel('Time')
    ax.set_ylabel('VIX')
    ax.grid(color='white')  # Set gridline color to white
    ax.set_facecolor('black')  # Set axis background to black
    ax.spines['bottom'].set_color('black')  # Set axis spines to black
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    st.pyplot(fig)

# Function to calculate and plot estimated debt volume
def plot_estimated_debt_volume(data):
    st.header("Estimated Debt Volume")
    data['Estimated Debt Volume'] = (data['Close'] - data['Adj Close']) * data['Volume']
    plt.style.use('dark_background')  # Set plot background to black
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Estimated Debt Volume'], color='blue')  # Set plot color to blue
    ax.set_xlabel('Time')
    ax.set_ylabel('Estimated Debt Volume')
    ax.grid(color='white')  # Set gridline color to white
    ax.set_facecolor('black')  # Set axis background to black
    ax.spines['bottom'].set_color('black')  # Set axis spines to black
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    st.pyplot(fig)

def main():
    st.title("Welcome to STOC!")
    st.write("STOC is your one-stop solution to everything you need to know about a company, so go out there and do your best as an investor!")
    st.write("NOTE TO USER: This is a project built for educational purposes, and may not be considered as financial advice, although best efforts by the developer to prevent any such inadvertent instances.")

    # Input fields
    ticker = st.text_input("Enter stock ticker:")
    exchange = st.selectbox("Select exchange:", list(exchange_suffixes.keys()))
    date_range = st.selectbox("Select date range:", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])

    if date_range == "1d":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=1)
        end_date = pd.to_datetime('today')
    elif date_range == "5d":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=5)
        end_date = pd.to_datetime('today')
    elif date_range == "1mo":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=30)
        end_date = pd.to_datetime('today')
    elif date_range == "3mo":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=90)
        end_date = pd.to_datetime('today')
    elif date_range == "6mo":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=180)
        end_date = pd.to_datetime('today')
    elif date_range == "1y":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=365)
        end_date = pd.to_datetime('today')
    elif date_range == "2y":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=730)
        end_date = pd.to_datetime('today')
    elif date_range == "5y":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=1825)
        end_date = pd.to_datetime('today')
    elif date_range == "10y":
        start_date = pd.to_datetime('today') - pd.Timedelta(days=3650)
        end_date = pd.to_datetime('today')
    elif date_range == "ytd":
        start_date = pd.to_datetime(f'{pd.to_datetime("today").year}-01-01')
        end_date = pd.to_datetime('today')
    elif date_range == "max":
        start_date = pd.to_datetime('1924-01-01')
        end_date = pd.to_datetime('today')

    if ticker and exchange and start_date and end_date:
        ticker_with_suffix = ticker + exchange_suffixes[exchange]
        data = fetch_data(ticker_with_suffix, start=start_date, end=end_date)
        
        # Dropdown to select parameter to plot
        parameters = ['Open', 'Close', 'Volume', 'High', 'Low', 'Adj Close']
        parameter_to_plot = st.selectbox("Select parameter to plot:", parameters)
        
        if parameter_to_plot == 'Open':
            st.write("The Open price is the price at which the stock opens for trading on a given day.")
        elif parameter_to_plot == 'High':
            st.write("The High price is the highest price at which the stock trades on a given day.")
        elif parameter_to_plot == 'Low':
            st.write("The Low price is the lowest price at which the stock trades on a given day.")
        elif parameter_to_plot == 'Close':
            st.write("The Close price is the price at which the stock closes for trading on a given day.")
        elif parameter_to_plot == 'Adj Close':
            st.write("The Adjusted Close price is the closing price of the stock adjusted for dividends and splits.")
        elif parameter_to_plot == 'Volume':
            st.write("The Volume is the number of shares traded on a given day.")
        elif parameter_to_plot == 'Estimated Debt Volume':
            st.write("The Estimated Debt Volume is an estimate of the company's debt. It is the product of Share Trade Volume and the difference of adjusted closing and closing prices. It is the replacement quantity for the debt quantity, for more info, refer to below the plot.")
        elif parameter_to_plot == 'VIX':
            st.write("The VIX is a measure of the market's expected volatility.")
        else:
            st.write("Please select a parameter to plot.")

        if parameter_to_plot == 'VIX':
            plot_vix(start_date, end_date)
        else:
            plot_time_series(data)
            plot_correlation_heatmap(data)
            display_mean_median(data)
            display_summary_statistics(data)
            plot_estimated_debt_volume(data)

    else:
        st.write("NO DATA FOUND")

if __name__ =="__main__":
    main()
