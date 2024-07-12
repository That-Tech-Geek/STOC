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
    "NYSE": "S&P 500",
    "NASDAQ": "NASDAQ Composite",
    "BSE": "SENSEX",
    "NSE": "NIFTY 50",
    "Cboe Indices": "Cboe Volatility Index (VIX)",
    "Chicago Board of Trade (CBOT)***": "S&P 500 VIX",
    "Chicago Mercantile Exchange (CME)***": "CME Group",
    "Dow Jones Indexes": "Dow Jones Industrial Average",
    "Nasdaq Stock Exchange": "NASDAQ Composite",
    "ICE Futures US": "Russell 2000",
    "New York Commodities Exchange (COMEX)***": "COMEX Gold",
    "New York Mercantile Exchange (NYMEX)***": "NYMEX Crude Oil",
    "Options Price Reporting Authority (OPRA)": "OPRA Index",
    "OTC Markets Group**": "OTCQX Best Market",
    "S & P Indices": "S&P 500",
    "Buenos Aires Stock Exchange (BYMA)": "MERVAL",
    "Vienna Stock Exchange": "ATX",
    "Australian Stock Exchange (ASX)": "S&P/ASX 200",
    "Cboe Australia": "S&P/ASX 200 VIX",
    "Euronext Brussels": "BEL 20",
    "Sao Paolo Stock Exchange (BOVESPA)": "IBOVESPA",
    "Canadian Securities Exchange": "S&P/TSX Composite",
    "Cboe Canada": "S&P/TSX Composite VIX",
    "Toronto Stock Exchange (TSX)": "S&P/TSX Composite",
    "TSX Venture Exchange (TSXV)": "TSX Venture Composite",
    "Santiago Stock Exchange": "IPSA",
    "Shanghai Stock Exchange": "SSE Composite Index",
    "Shenzhen Stock Exchange": "SZSE Component Index",
    "Prague Stock Exchange Index": "PX",
    "Nasdaq OMX Copenhagen": "OMX Copenhagen 25",
    "Egyptian Exchange Index (EGID)": "EGX 30",
    "Nasdaq OMX Tallinn": "OMX Tallinn",
    "Cboe Europe": "EURO STOXX 50",
    "Euronext": "Euronext 100",
    "Nasdaq OMX Helsinki": "OMX Helsinki 25",
    "Euronext Paris": "CAC 40",
    "Berlin Stock Exchange": "DAX",
    "Bremen Stock Exchange": "BREXIT",
    "Dusseldorf Stock Exchange": "DAX",
    "Frankfurt Stock Exchange": "DAX",
    "Hamburg Stock Exchange": "BREXIT",
    "Hanover Stock Exchange": "BREXIT",
    "Munich Stock Exchange": "DAX",
    "Stuttgart Stock Exchange": "BREXIT",
    "Deutsche Boerse XETRA": "DAX",
    "Collectable Indices": "COLLECT",
    "Cryptocurrencies": "CRYPTO",
    "Currency Rates": "CURRENCY",
    "MSCI Indices": "MSCI",
    "Athens Stock Exchange (ATHEX)": "ASE",
    "Hang Seng Indices": "HANG SENG",
    "Hong Kong Stock Exchange (HKEX)*": "HANG SENG",
    "Budapest Stock Exchange": "BUX",
    "Nasdaq OMX Iceland": "OMX",
    "Bombay Stock Exchange": "BSE",
    "National Stock Exchange of India": "NSE",
    "Indonesia Stock Exchange (IDX)": "IDX",
    "Euronext Dublin": "INDEX",
    "Tel Aviv Stock Exchange": "TEL AVIV",
    "EuroTLX": "EURO TLX",
    "Italian Stock Exchange": "ITALY",
    "Nikkei Indices": "NIKKEI",
    "Tokyo Stock Exchange": "TOKYO",
    "Boursa Kuwait": "KW",
    "Nasdaq OMX Riga": "RIGA",
    "Nasdaq OMX Vilnius": "VILNIUS",
    "Malaysian Stock Exchange": "MALAYSIA",
    "Mexico Stock Exchange (BMV)": "BMV",
    "Euronext Amsterdam": "EUROPE",
    "New Zealand Stock Exchange (NZX)": "NZX",
    "Oslo Stock Exchange": "OSLO",
    "Philippine Stock Exchange Indices": "PHILIPPINES",
    "Warsaw Stock Exchange": "WSE",
    "Euronext Lisbon": "LISBON",
    "Qatar Stock Exchange": "QATAR",
    "Bucharest Stock Exchange": "BUCHAREST",
    "Singapore Stock Exchange (SGX)": "SGX",
    "Johannesburg Stock Exchange": "JOHANNESBURG",
    "Korea Stock Exchange": "KOREA",
    "KOSDAQ": "KOSDAQ",
    "Madrid SE C.A.T.S.": "MADRID",
    "Saudi Stock Exchange (Tadawul)": "TADAWUL",
    "Nasdaq OMX Stockholm": "OMX",
    "Swiss Exchange (SIX)": "SIX",
    "Taiwan OTC Exchange": "OTC",
    "Taiwan Stock Exchange (TWSE)": "TWSE",
    "Stock Exchange of Thailand (SET)": "SET",
    "Borsa İstanbul": "ISTANBUL",
    "Dubai Financial Market": "DFM",
    "Cboe UK": "UK",
    "FTSE Indices": "FTSE",
    "London Stock Exchange": "LSE",
    "Caracas Stock Exchange": "CARACAS"
}

# Function to fetch data from Yahoo Finance
def fetch_data(symbol, exchange):
    ticker = symbol + exchange_suffixes[exchange]
    data = yf.download(ticker, start='2020-01-01', end='2023-01-01')
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
                plt.figure(figsize=(10, 6))
                plt.plot(data.index, data[column])
                plt.title(f"{column} over Time")
                plt.xlabel("Date")
                plt.ylabel(column)
                st.pyplot()
            
            # Correlation plot
            st.write("Correlation Matrix:")
            corr = data.corr()
            plt.figure(figsize=(12, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
            plt.title("Correlation Matrix")
            st.pyplot()
            
            # Output CSV with selected columns
            st.write("CSV Output:")
            selected_columns = st.multiselect("Select columns to include in CSV", data.columns)
            if selected_columns:
                selected_data = data[selected_columns]
                st.write(selected_data.head())
                st.markdown(get_csv_download_link(selected_data), unsafe_allow_html=True)
        else:
            st.write("No data found for the selected symbol and exchange.")

# Function to create a download link for a DataFrame as CSV
def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    href = f'<a href="data:file/csv;base64,{b64encode(csv.encode()).decode()}" download="data.csv">Download CSV File</a>'
    return href

if __name__ == "__main__":
    main()
