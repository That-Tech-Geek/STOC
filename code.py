import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import io

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
    else:
        st.warning("DataFrame is empty. No data to plot.")

# Function to detect numeric columns
def get_numeric_columns(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    return numeric_cols

# Function to edit numeric columns
def edit_columns(numeric_cols):
    edited_cols = st.multiselect("Select numeric columns to include", numeric_cols, default=numeric_cols)
    return edited_cols

# Function to plot correlation graphs
def plot_correlations(df, cols):
    try:
        if len(cols) > 1:
            corr = df[cols].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            st.pyplot(fig)
            
            # Calculate and display correlation coefficients
            corr_coefficients = corr.unstack().sort_values(ascending=False)
            st.write("How the financial metrics are related:")
            st.write(corr_coefficients)
            
            # Identify highly correlated columns
            highly_correlated_cols = [(cols[i], cols[j]) for i in range(len(corr)) for j in range(i) if abs(corr.iloc[i, j]) > 0.8 and i != j]
            st.write("Financial metrics that are strongly linked:")
            st.write(highly_correlated_cols)
            
            # Explain correlations
            st.write("Positive correlation (+ve) means a direct relationship; negative correlation (-ve) means an inverse relationship.")
            
            # Simple weighting to determine good investment
            weights = {col: abs(corr[col].sum()) for col in cols}
            weighted_sum = sum(weights.values())
            if weighted_sum > len(cols):
                st.success("This appears to be a good investment based on the correlation metrics.")
            else:
                st.warning("This may not be a good investment based on the correlation metrics.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

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
exchange = st.selectbox("Select the exchange", list(exchange_suffixes.keys()))
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

if st.button("Fetch Data"):
    data = download_data(ticker, exchange, start_date, end_date)
    
    # Save the dataframe to a CSV buffer
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Display the dataframe
    st.subheader("Ticker Data")
    st.dataframe(data)

    # Upload CSV automatically
    uploaded_file = csv_buffer.getvalue()
    if uploaded_file:
        st.subheader("CSV Uploaded Data")
        df = pd.read_csv(io.StringIO(uploaded_file))
        
        # Detect and edit numeric columns
        numeric_cols = get_numeric_columns(df)
        edited_cols = edit_columns(numeric_cols)
        
        # Plot correlation graphs
        plot_correlations(df, edited_cols)
    else:
        st.error("Error in uploading CSV data.")

# Plot data
if 'data' in locals() and not data.empty:
    plot_data(data)

if __name__ == "__main__":
    main()
