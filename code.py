import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date, timedelta

# Set up Streamlit theme
st.markdown("""
<style>
body {
    background-color: #000000;
    color: #FFFFFF;
    text-shadow: none;
}
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}
.stSidebar {
    background-color: #000000;
    color: #FFFFFF;
}
.stSidebar .stRadio {
    color: #FFFFFF;
}
.stButton {
    background-color: #000000;
    color: #FFFFFF;
    border: none;
}
.stButton:hover {
    background-color: #333333;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Welcome to S.T.O.C (Strategic Trading Optimization Console)!")
    
    # Load company data from GitHub
    company_data = pd.read_csv("https://raw.githubusercontent.com/your-username/your-repo-name/main/Directory%20-%20Sheet1%20(1).csv")
    
    company_name = st.selectbox("Select a company:", company_data["NAME OF COMPANY"])
    
    if company_name:
        try:
            ticker_symbol = company_data.loc[company_data["NAME OF COMPANY"] == company_name, "NSE CODE"].values[0]
            
            # Load data from GitHub
            file_path1 = f"https://raw.githubusercontent.com/That-Tech-Geek/STOC/main/Datasets/{ticker_symbol}.csv"
            file_path2 = f"https://raw.githubusercontent.com/That-Tech-Geek/STOC/main/datasets2/{ticker_symbol}.csv"
            
            try:
                data = pd.read_csv(file_path1)
            except FileNotFoundError:
                try:
                    data = pd.read_csv(file_path2)
                except FileNotFoundError:
                    st.write("Error: File not found in either path")
                    return
            
            data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
            
            min_date = data['Date'].min()
            max_date = data['Date'].max()
            
            start_date = st.date_input("Select start date:", value=min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("Select end date:", value=max_date, min_value=min_date, max_value=max_date)
            
            start_date_pd = pd.to_datetime(start_date)
            end_date_pd = pd.to_datetime(end_date)
            
            data_filtered = data[(data['Date'] >= start_date_pd) & (data['Date'] <= end_date_pd)]
            
            st.write("Loaded data from GitHub:")
            
            if st.button("Download CSV"):
                data_filtered.to_csv(f"{ticker_symbol}_output.csv", index=False)
                st.write("CSV file downloaded successfully!")
            
            st.write(data_filtered)
            
            columns = ['Close', 'Adj Close', 'Variability Index', 'Volume']
            column_titles = {'Close': 'Closing Stock Prices', 'Adj Close': 'Adjusted Closing Stock Prices', 'Variability Index': 'Variability Index', 'Volume': 'Share Trade Volume'}
            column_desc = {'Close': 'The closing price of the stock at the end of the trading day.', 
                        'Adj Close': 'The adjusted closing price of the stock at the end of the trading day, adjusted for dividends and splits.', 
                        'Variability Index': "A measure of the stock's volatility.", 
                        'Volume': 'The number of shares traded during the day.'}
            plot_descriptions = {
                'Close': 'This graph shows the trend of closing stock prices for the selected company over the specified time period.',
                'Adj Close': 'This graph shows the trend of adjusted closing stock prices for the selected company over the specified time period.',
                'Variability Index': 'This graph shows the trend of variability index for the selected company over the specified time period.',
                'Volume': 'This graph shows the share trade volume for the selected company over the specified time period.',
                'Close-Adj Close': "This graph compares the trend of closing stock prices and adjusted closing stock prices for the selected company over the specified time period. This is important so that the investor can know about the dividend payouts of the stock. Contrary to popular belief, the majority of an investor's earnings ceom from dividend payouts, and not the resale value of the stock he/she holds."
            }
            
            option = st.selectbox('Select a plot:', ['Close', 'Adj Close', 'Variability Index', 'Volume', 'Close-Adj Close'])
            
            if option == 'Close':
                st.write(f"**You selected: {column_titles[option]}**")
                st.write(f"{column_desc[option]}")
                st.write(f"{plot_descriptions[option]}")
                fig, ax = plt.subplots(figsize=(10,6))
                plt.style.use('dark_background')  
                ax.spines['bottom'].set_color('black')  
                ax.spines['left'].set_color('black')  
                ax.tick_params(axis='x', colors='white')  
                ax.tick_params(axis='y', colors='white')  
                ax.grid(True, color='white', linestyle='--', linewidth=0.5)  
                ax.plot(data_filtered['Date'], data_filtered[option], color='blue')  
                ax.set_title(f'{ticker_symbol} {column_titles[option]} Over Time', color='white')  
                ax.set_xlabel('Date', color='white')  
                ax.set_ylabel(column_titles[option], color='white')  
                st.pyplot(fig)  
            
            #... (rest of the code remains the same)

        except Exception as e:
            st.write("Error:", str(e))

if __name__ == "__main__":
    main()
