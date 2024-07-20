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
    "Large-cap": 10e9,
    "Mid-cap": 2e9,
    "Small-cap": 500e6,
    "Micro-cap": 50e6,
    "Nano-cap": 0
}

# Function to fetch data
def fetch_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, progress=False)
    return data

# Function to plot time series data
def plot_time_series(data, excluded_columns):
    st.header("Time Series Data")
    columns_to_plot = [col for col in data.columns if col not in excluded_columns]
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
def plot_correlation_heatmap(data, excluded_columns):
    st.header("Correlation Heatmap")
    columns_to_include = [col for col in data.columns if col not in excluded_columns]
    corr = data[columns_to_include].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Function to display mean and median
def display_mean_median(data, excluded_columns):
    st.header("Mean and Median Values")
    columns_to_include = [col for col in data.columns if col not in excluded_columns]
    mean_values = data[columns_to_include].mean()
    median_values = data[columns_to_include].median()
    summary = pd.DataFrame({'Mean': mean_values, 'Median': median_values})
    st.dataframe(summary)

# Function to display summary statistics
def display_summary_statistics(data, excluded_columns):
    st.header("Summary Statistics")
    columns_to_include = [col for col in data.columns if col not in excluded_columns]
    summary_stats = data[columns_to_include].describe()
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

def fetch_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, progress=False)
    return data

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
        
        if not data.empty:
            # Calculate estimated debt volume
            data['Estimated Debt Volume'] = (data['Close'] - data['Adj Close']) * data['Volume']
            data['Average Total Assets'] = data['Adj Close'] * data['Volume']
            data['Asset Turnover Ratio'] = data['Volume'] / data['Average Total Assets']
            data['EBIT'] = (data['Volume'] * data['Close']) - (data['Volume'] * data['Close']) - ((data['Volume'] * data['Close']) * (data['Close'] - data['Open']) / data['Volume'])
            data['Interest Rate'] = 0.08
            data['Corporate Tax'] = 0.235
            # Calculate various ratios
            data['Debt-to-Equity Ratio'] = data['Estimated Debt Volume'] / data['Adj Close']
            data['Current Ratio'] = data['Adj Close'] / data['Estimated Debt Volume']
            data['Interest Coverage Ratio'] = data['Adj Close'] / (data['Estimated Debt Volume'] * 0.05)
            data['Debt-to-Capital Ratio'] = data['Estimated Debt Volume'] / (data['Adj Close'] + data['Estimated Debt Volume'])
            data['Price-to-Earnings Ratio'] = data['Close'] / data['Adj Close']
            data['Price-to-Book Ratio'] = data['Close'] / data['Adj Close']
            data['Return on Equity (ROE)'] = (data['Close'] - data['Open']) / data['Adj Close']
            data['Return on Assets (ROA)'] = (data['Close'] - data['Open']) / data['Volume']
            data['Earnings Yield'] = data['Adj Close'] / data['Close']
            data['Dividend Yield'] = data['Adj Close'] / data['Close']
            data['Price-to-Sales Ratio'] = data['Close'] / data['Volume']
            data['Enterprise Value-to-EBITDA Ratio'] = (data['Close'] * data['Volume']) / (data['Adj Close'] * 0.05)
            data['Asset Turnover Ratio'] = data['Volume'] / data['Adj Close']
            data['Inventory Turnover Ratio'] = data['Volume'] / (data['Close'] - data['Open'])
            data['Receivables Turnover Ratio'] = data['Volume'] / (data['Close'] - data['Open'])
            data['Payables Turnover Ratio'] = data['Volume'] / (data['Close'] - data['Open'])
            data['Cash Conversion Cycle'] = (data['Close'] - data['Open']) / data['Volume']
            data['Interest Coverage Ratio'] = data['Adj Close'] / (data['Estimated Debt Volume'] * 0.05)
            data['Debt Service Coverage Ratio'] = data['Adj Close'] / (data['Estimated Debt Volume'] * 0.05)
            data['Return on Invested Capital (ROIC)'] = (data['Close'] - data['Open']) / (data['Adj Close'] + data['Estimated Debt Volume'])
            data['Return on Common Equity (ROCE)'] = (data['Close'] - data['Open']) / data['Adj Close']
            data['Gross Margin Ratio'] = (data['Close'] - data['Open']) / data['Volume']
            data['Operating Margin Ratio'] = (data['Close'] - data['Open']) / data['Volume']
            data['Net Profit Margin Ratio'] = (data['Close'] - data['Open']) / data['Volume']
            data['Debt to Assets Ratio'] = data['Estimated Debt Volume'] / data['Asset Turnover Ratio']
            data['Equity Ratio'] = data['Volume'] / data['Asset Turnover Ratio']
            data['Financial Leverage Ratio'] = data['Asset Turnover Ratio'] / data['Volume']
            data['Proprietary Ratio'] = data['Volume'] / data['Asset Turnover Ratio']
            data['Capital Gearing Ratio'] = data['Estimated Debt Volume'] / data['Volume']
            data['Interest Coverage Ratio'] = data['EBIT'] / (data['Estimated Debt Volume'] * data['Interest Rate'])
            data['DSCR'] = (data['Adj Close'] * data['Volume']) / (data['Estimated Debt Volume'])
            data['Gross Profit Ratio'] = (data['Adj Close'] * data['Volume']) - (data['Close'] * data['Volume']) / (data['Adj Close'] * data['Volume'])
            data['Net Profit Ratio'] = (data['Close'] * data['Volume']) * data['Corporate Tax'] / (data['Adj Close'] * data['Volume'])
            data['ROI'] = (data['Close'] * data['Volume']) * data['Corporate Tax'] / data['High']
            data['EBITDA Margin'] = data['EBIT'] / (data['Adj Close'] * data['Volume'])
            data['Asset Turnover Ratio'] = (data['Adj Close'] * data['Volume']) / data['Asset Turnover Ratio']
            data['Fixed Asset Turnover Ratio'] = (data['Adj Close'] * data['Volume']) / data['Volume'] * (data['Open'] + data['Close']) / 2
            data['Capital Turnover Ratio'] = (data['Adj Close'] * data['Volume']) / (data['Volume'] + data['Estimated Debt Volume'])

            # Dropdown to select parameter to plot
            parameters = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Estimated Debt Volume', 'VIX', 'Debt-to-Equity Ratio', 'Capital Turnover Ratio', 'Fixed Asset Turnover Ratio', 'ROI', 'EBITDA Margin', 'Asset Turnover Ratio', 'Current Ratio', 'Interest Coverage Ratio', 'Debt-to-Capital Ratio', 'Price-to-Earnings Ratio', 'Price-to-Book Ratio', 'Return on Equity (ROE)', 'Return on Assets (ROA)', 'Earnings Yield', 'Dividend Yield', 'Price-to-Sales Ratio', 'Enterprise Value-to-EBITDARatio', 'Asset Turnover Ratio', 'Inventory Turnover Ratio', 'Receivables Turnover Ratio', 'Payables Turnover Ratio', 'Cash Conversion Cycle', 'Interest Coverage Ratio', 'Debt Service Coverage Ratio', 'Return on Invested Capital (ROIC)', 'Return on Common Equity (ROCE)', 'Gross Margin Ratio', 'Operating Margin Ratio', 'Net Profit Margin Ratio']
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
            elif parameter_to_plot == 'Debt-to-Equity Ratio':
                st.write("The Debt-to-Equity Ratio is a measure of a company's leverage. It is calculated by dividing the estimated debt volume by the adjusted closing price. A higher ratio indicates higher leverage and potentially higher risk.")
            elif parameter_to_plot == 'Current Ratio':
                st.write("The Current Ratio is a measure of a company's liquidity. It is calculated by dividing the adjusted closing price by the estimated debt volume. A higher ratio indicates higher liquidity and ability to pay short-term debts.")
            elif parameter_to_plot == 'Interest Coverage Ratio':
                st.write("The Interest Coverage Ratio is a measure of a company's ability to pay interest on its debt. It is calculated by dividing the adjusted closing price by the estimated debt volume multiplied by 0.05. A higher ratio indicates higher ability to pay interest.")
            elif parameter_to_plot == 'Debt-to-Capital Ratio':
                st.write("The Debt-to-Capital Ratio is a measure of a company's leverage. It is calculated by dividing the estimated debt volume by the sum of the adjusted closing price and estimated debt volume. A higher ratio indicates higher leverage and potentially higher risk.")
            elif parameter_to_plot == 'Price-to-Earnings Ratio':
                st.write("The Price-to-Earnings Ratio is a measure of a company's valuation. It is calculated by dividing the closing price by the adjusted closing price. A higher ratio indicates higher valuation and potentially higher growth expectations.")
            elif parameter_to_plot == 'Price-to-Book Ratio':
                st.write("The Price-to-Book Ratio is a measure of a company's valuation. It is calculated by dividing the closing price by the adjusted closing price. A higher ratio indicates higher valuation and potentially higher growth expectations.")
            elif parameter_to_plot == 'Return on Equity (ROE)':
                st.write("The Return on Equity (ROE) is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the adjusted closing price. A higher ratio indicates higher profitability.")
            elif parameter_to_plot == 'Return on Assets (ROA)':
                st.write("The Return on Assets (ROA) is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the volume. A higher ratio indicates higher profitability.")
            elif parameter_to_plot == 'Earnings Yield':
                st.write("The Earnings Yield is a measure of a company's valuation. It is calculated by dividing the adjusted closing price by the closing price. A higher ratio indicates higher valuation and potentially higher growth expectations.")
            elif parameter_to_plot == 'Dividend Yield':
                st.write("The Dividend Yield is a measure of a company's dividend payments. It is calculated by dividing the adjusted closing price by the closing price. A higher ratio indicates higher dividend payments.")
            elif parameter_to_plot == 'Price-to-Sales Ratio':
                st.write("The Price-to-Sales Ratio is a measure of a company's valuation. It is calculated by dividing the closing price by the volume. A higher ratio indicates higher valuation and potentially higher growth expectations.")
            elif parameter_to_plot == 'Enterprise Value-to-EBITDA Ratio':
                st.write("The Enterprise Value-to-EBITDA Ratio is a measure of a company's valuation. It is calculated by dividing the product of the closing price and volume by the adjusted closing price multiplied by 0.05. A higher ratio indicates higher valuation and potentially higher growth expectations.")
            elif parameter_to_plot == 'Asset Turnover Ratio':
                st.write("The Asset Turnover Ratio is a measure of a company's efficiency. It is calculated by dividing the volume by the adjusted closing price. A higher ratio indicates higher efficiency.")
            elif parameter_to_plot == 'Inventory Turnover Ratio':
                st.write("The Inventory Turnover Ratio is a measureof a company's efficiency. It is calculated by dividing the volume by the difference between the closing and opening prices. A higher ratio indicates higher efficiency.")
            elif parameter_to_plot == 'Receivables Turnover Ratio':
                st.write("The Receivables Turnover Ratio is a measure of a company's efficiency. It is calculated by dividing the volume by the difference between the closing and opening prices. A higher ratio indicates higher efficiency.")
            elif parameter_to_plot == 'Payables Turnover Ratio':
                st.write("The Payables Turnover Ratio is a measure of a company's efficiency. It is calculated by dividing the volume by the difference between the closing and opening prices. A higher ratio indicates higher efficiency.")
            elif parameter_to_plot == 'Cash Conversion Cycle':
                st.write("The Cash Conversion Cycle is a measure of a company's efficiency. It is calculated by dividing the difference between the closing and opening prices by the volume. A higher ratio indicates higher efficiency.")
            elif parameter_to_plot == 'Interest Coverage Ratio':
                st.write("The Interest Coverage Ratio is a measure of a company's ability to pay interest on its debt. It is calculated by dividing the adjusted closing price by the estimated debt volume multiplied by 0.05. A higher ratio indicates higher ability to pay interest.")
            elif parameter_to_plot == 'Debt Service Coverage Ratio':
                st.write("The Debt Service Coverage Ratio is a measure of a company's ability to pay its debt. It is calculated by dividing the adjusted closing price by the estimated debt volume multiplied by 0.05. A higher ratio indicates higher ability to pay debt.")
            elif parameter_to_plot == 'Return on Invested Capital (ROIC)':
                st.write("The Return on Invested Capital (ROIC) is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the sum of the adjusted closing price and estimated debt volume. A higher ratio indicates higher profitability.")
            elif parameter_to_plot == 'Return on Common Equity (ROCE)':
                st.write("The Return on Common Equity (ROCE) is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the adjusted closing price. A higher ratio indicates higher profitability.")
            elif parameter_to_plot == 'Gross Margin Ratio':
                st.write("The Gross Margin Ratio is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the volume. A higher ratio indicates higher profitability.")
            elif parameter_to_plot == 'Operating Margin Ratio':
                st.write("The Operating Margin Ratio is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the volume. A higher ratio indicates higher profitability.")
            elif parameter_to_plot == 'Net Profit Margin Ratio':
                st.write("The Net Profit Margin Ratio is a measure of a company's profitability. It is calculated by dividing the difference between the closing and opening prices by the volume. A higher ratio indicates higher profitability.")
            else:
                st.write("Please select a parameter to plot.")
            if parameter_to_plot == 'VIX':
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
                latest_value = vix_data['Close'].iloc[-1]
                st.write(f"Latest VIX: {latest_value:.2f}, rounded off to two decimal placecs.")
            else:
                plt.style.use('dark_background')  # Set plot background to black
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(data.index, data[parameter_to_plot], color='blue')  # Set plot color to blue
                ax.set_xlabel('Time')
                ax.set_ylabel(parameter_to_plot)
                ax.grid(color='white')  # Set gridline color to white
                ax.set_facecolor('black')  # Set axis background to black
                ax.spines['bottom'].set_color('black')  # Set axis spines to black
                ax.spines['top'].set_color('black')
                ax.spines['right'].set_color('black')
                ax.spines['left'].set_color('black')
                st.pyplot(fig)
                latest_value = data[parameter_to_plot].iloc[-1]
                st.write(f"Latest {parameter_to_plot}: {latest_value:.2f}, rounded off to two decimal places.")
            st.write("This plot may be reliant on the parameter of debt. Due to inability to source debt data reliably, it has been assumed, globally through all analyses, that the company does not pay dividends, and uses all that money to repay debt obligations. This is why we urge you not to consider this as financial advice. We are working hard to find a way to get more reliable and workabe data for you. This replacement quantity is **Estimated Debt Volume**. Sit tight!")
            st.write("This program also assumes that any income made by the company is from the stock market and the stock market only, since this code has not yet been developed enough to access data from Financial Statements of companies. While we are sure we have the capability, we're working hard to make it happen, and further expand the horizons of STOC to give you a lot more insight into a company, all in a single place. Thanks for waiting around!")
            excluded_columns = []
            def display_correlation_table(data, excluded_columns):
                st.header("Correlation Table")
                columns_to_include = [col for col in data.columns if col not in excluded_columns]
                corr = data[columns_to_include].corr()
                st.dataframe(corr.style.format("{:.2f}"))  # Display correlation matrix as a table
            def display_mean_median(data, excluded_cols):
                # Drop the excluded columns
                data = data.drop(excluded_cols, axis=1)
                
                # Calculate and display the mean
                st.write("Mean:")
                st.write(data.mean())
                
                # Calculate and display the median
                st.write("\nMedian:")
                st.write(data.median())
            
            # Now you can call the function
            display_mean_median(data, excluded_columns)

            # Display mean and median values
            display_mean_median(data, excluded_columns)

            # Display summary statistics
            display_summary_statistics(data, excluded_columns)

            # Display Correlation Heatmap
            display_correlation_table(data, excluded_columns)
            # Option to download data
            st.header("Download Data")
            csv = data.to_csv(index=True)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='stock_data.csv',
                mime='text/csv',
                )
            st.title("Get in Touch!")
            st.write("After you submit this data which we assure is confidential, we will send you an email. You can list any suggestions or revies to us from that email. We're looking forward to what you have to say!")
           # Get email credentials from Streamlit secrets
            email_address = "recipient@example.com"  # Define recipient email
            subject = "Test Email"  # Define email subject
            body = "This is a test email."  # Define email body
            try:
                # Get email credentials from Streamlit secrets
                email_id = st.secrets["EMAIL_ID "]["email_id"]
                email_password = st.secrets["EMAIL_PASSWORD "]["email_password"]
        
                yag = yagmail.SMTP(email_id, email_password)
                yag.send(to=email_address, subject=subject, contents=body)
                st.success("Email sent successfully!")
            except KeyError as e:
                st.error(f"Key error: {e}. Check if the secrets are correctly set up.")
            except yagmail.error.YagInvalidEmailAddress as e:
                st.error(f"Invalid email address: {e}")
            except yagmail.error.YagAddressError as e:
                st.error(f"Address error: {e}")
            except yagmail.error.YagConnectionClosed as e:
                st.error(f"Connection closed: {e}")
            except yagmail.error.YagSMTPError as e:
                st.error(f"SMTP error: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("No data available for the given ticker and date range.")

if __name__ =="__main__":
    main()
