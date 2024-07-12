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

# Function to fetch national average data for each exchange suffix
def fetch_national_averages(exchange_suffixes, start_date, end_date):
    national_avg_data = pd.DataFrame()

    for exchange, suffix in exchange_suffixes.items():
        if suffix:
            index_ticker = f"{exchange}{suffix}"
            index_data = yf.download(index_ticker, start=start_date, end=end_date, progress=False)
            if not index_data.empty:
                index_data['Exchange'] = exchange
                national_avg_data = pd.concat([national_avg_data, index_data], axis=0)

    return national_avg_data

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

        # Download company data
        company_data = yf.download(ticker, start=start_date_str, end=end_date_str, progress=False)

        if not company_data.empty:
            # Fetch national averages for each exchange suffix
            national_avg_data = fetch_national_averages(exchange_suffixes, start_date=start_date_str, end_date=end_date_str)

            if not national_avg_data.empty:
                # Plot comparison with national averages
                plt.figure(figsize=(12, 6))
                plt.plot(company_data.index, company_data['Adj Close'], label=f"{ticker} - {exchange} Data")

                for exch, suffix in exchange_suffixes.items():
                    if suffix:
                        avg_data = national_avg_data[national_avg_data['Exchange'] == exch]
                        if not avg_data.empty:
                            plt.plot(avg_data.index, avg_data['Adj Close'], label=f"{exch} - National Average", linestyle='--')

                plt.xlabel('Date')
                plt.ylabel('Adjusted Close Price')
                plt.title(f"{ticker} vs National Averages")
                plt.legend()
                st.pyplot()

                # Save company data to CSV
                company_filename = f"{ticker}_{exchange}_data.csv"
                company_data.to_csv(company_filename, index=True)
                st.success(f"Company data saved to {company_filename}")

                # Save national averages data to CSV
                national_avg_filename = f"national_averages_data.csv"
                national_avg_data.to_csv(national_avg_filename, index=True)
                st.success(f"National averages data saved to {national_avg_filename}")

            else:
                st.warning("No national averages data available.")
        else:
            st.error("No data available for the given ticker.")
