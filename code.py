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

# Function to fetch data from Yahoo Finance
def fetch_data(symbol, exchange):
    ticker = symbol + exchange_suffixes[exchange]
    data = yf.download(ticker, start='1900-01-01', end='2024-07-12', progress=False)  # Suppress progress bar
    return data

# Main function to run the Streamlit app
def main():
    st.title("Stock Data Analysis Tool")
    
    # Sidebar options
    exchange = st.sidebar.selectbox("Select Exchange", list(exchange_suffixes.keys()))
    symbol = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL)")
    
    if st.sidebar.button("Get Data"):
        st.write(f"Fetching data for {symbol} from {exchange}")
        data = fetch_data(symbol, exchange)
        
        if not data.empty:
            st.write("Data Sample:")
            st.write(data.head())
            
            # Plotting parameters against time
            st.write("Plotting parameters against time:")
            columns = [col for col in data.columns if col not in ['Volume', 'Adj Close']]
            
            for column in columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(data.index, data[column])
                ax.set_title(f"{column} over Time")
                ax.set_xlabel("Date")
                ax.set_ylabel(column)
                st.pyplot(fig)
            
            # Correlation plot
            st.write("Correlation Matrix:")
            corr = data.corr()
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, ax=ax)
            ax.set_title("Correlation Matrix")
            st.pyplot(fig)
            
            # Download CSV button
            st.write("Download CSV Output:")
            csv = data.to_csv(index=False)
            st.markdown(f"[Download CSV]({csv})", unsafe_allow_html=True)
        else:
            st.write("No data found for the selected symbol and exchange.")

if __name__ == "__main__":
    main()
