import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Dictionaries provided
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
    "Collectable Indices": "COLLECT",  # Collectable Indices (example, needs actual ticker)
    "Cryptocurrencies": "BTC-USD",  # Bitcoin (example, needs actual ticker)
    "Currency Rates": "EURUSD=X",  # EUR/USD
    "MSCI Indices": "^MSCI",  # MSCI World (example, needs actual ticker)
    "Athens Stock Exchange (ATHEX)": "^ASE",  # ATHEX Composite
    "Hang Seng Indices": "^HSI",  # HSI
    "Hong Kong Stock Exchange (HKEX)*": "^HSI",  # HSI
    "Budapest Stock Exchange": "^BUX",  # BUX
    "Nasdaq OMX Iceland": "^OMXI10",  # OMX Iceland 10
    "Bombay Stock Exchange": "^BSESN",  # SENSEX
    "National Stock Exchange of India": "^NSEI",  # NIFTY 50
    "Indonesia Stock Exchange (IDX)": "^JKSE",  # Jakarta Composite
    "Euronext Dublin": "^ISEQ",  # ISEQ Overall Index
    "Tel Aviv Stock Exchange": "^TA125",  # TA-125
    "EuroTLX": "EUROTLX",  # EuroTLX (example, needs actual ticker)
    "Italian Stock Exchange": "^FTSEMIB",  # FTSE MIB
    "Nikkei Indices": "^N225",  # Nikkei 225
    "Tokyo Stock Exchange": "^N225",  # Nikkei 225
    "Boursa Kuwait": "KUWAIT",  # Kuwait Index (example, needs actual ticker)
    "Nasdaq OMX Riga": "^OMXRGI",  # OMX Riga
    "Nasdaq OMX Vilnius": "^OMXVGI",  # OMX Vilnius
    "Malaysian Stock Exchange": "^KLSE",  # FTSE Bursa Malaysia KLCI
    "Mexico Stock Exchange (BMV)": "^MXX",  # IPC
    "Euronext Amsterdam": "^AEX",  # AEX
    "New Zealand Stock Exchange (NZX)": "^NZ50",  # S&P/NZX 50
    "Oslo Stock Exchange": "^OBX",  # OBX
    "Philippine Stock Exchange Indices": "^PSEI",  # PSEi
    "Warsaw Stock Exchange": "^WIG20",  # WIG 20
    "Euronext Lisbon": "^PSI20",  # PSI 20
    "Qatar Stock Exchange": "^QE",  # QE Index
    "Bucharest Stock Exchange": "^BETI",  # BET Index
    "Singapore Stock Exchange (SGX)": "^STI",  # STI
    "Johannesburg Stock Exchange": "^J203",  # JSE Top 40
    "Korea Stock Exchange": "^KS11",  # KOSPI
    "KOSDAQ": "^KQ11",  # KOSDAQ
    "Madrid SE C.A.T.S.": "^IBEX",  # IBEX 35
    "Saudi Stock Exchange (Tadawul)": "^TASI",  # TASI
    "Nasdaq OMX Stockholm": "^OMXSPI",  # OMX Stockholm PI
    "Swiss Exchange (SIX)": "^SSMI",  # SMI
    "Taiwan OTC Exchange": "^TWOTCI",  # TAIEX
    "Taiwan Stock Exchange (TWSE)": "^TWII",  # TAIEX
    "Stock Exchange of Thailand (SET)": "^SET50",  # SET 50
    "Borsa İstanbul": "XU100",  # BIST 100
    "Dubai Financial Market": "^DFM",  # DFM Index
    "Cboe UK": "^FTSE",  # FTSE 100
    "FTSE Indices": "^FTSE",  # FTSE 100
    "London Stock Exchange": "^FTSE",  # FTSE 100
    "Caracas Stock Exchange": "IBC",  # IBC
}

def main():
    st.title("Share Price Retrieval App")
    st.write("Retrieve share prices of any company within a selected date range from Yahoo Finance.")

    # User inputs
    exchange = st.selectbox("Select Exchange", list(exchange_suffixes.keys()))
    company_ticker = st.text_input("Enter Company Ticker (e.g., AAPL)")

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    # Debugging output
    st.write(f"Selected exchange: {exchange}")
    st.write(f"Entered ticker: {company_ticker}")
    st.write(f"Date range: {start_date} to {end_date}")

    # Check if ticker and dates are provided
    if company_ticker and start_date and end_date:
        try:
            # Append exchange suffix
            ticker = company_ticker + exchange_suffixes[exchange]

            # Retrieve data from Yahoo Finance
            data = yf.download(ticker, start=start_date, end=end_date)
            
            if not data.empty:
                st.write(f"Showing data for {ticker}")
                
                # Plot Opening Prices
                st.subheader("Opening Stock Prices")
                st.line_chart(data['Open'])
                
                # Plot Closing Prices
                st.subheader("Closing Stock Prices")
                st.line_chart(data['Close'])
                
                # Plot Adjusted Closing Prices
                st.subheader("Adjusted Closing Prices")
                st.line_chart(data['Adj Close'])

                # Calculate and plot Variability Index (Standard Deviation of Close Prices)
                st.subheader("Variability Index (Standard Deviation of Close Prices)")
                variability_index = data['Close'].rolling(window=20).std()
                st.line_chart(variability_index)
                
                # Adjusted Variability Index (Adjusted Standard Deviation)
                st.subheader("Adjusted Variability Index (Standard Deviation of Adjusted Close Prices)")
                adj_variability_index = data['Adj Close'].rolling(window=20).std()
                st.line_chart(adj_variability_index)
                
                st.write(data)
            else:
                st.write(f"No data found for {ticker} within the selected date range.")
        except Exception as e:
            st.write(f"An error occurred: {e}")
    else:
        st.write("Please enter a company ticker and select a date range.")

if __name__ == "__main__":
    main()
