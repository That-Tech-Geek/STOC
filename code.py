import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
from datetime import date, timedelta

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
.stSidebar.stRadio {
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
    
    company_name = st.text_input("Enter a company ticker symbol:")
    
    if company_name:
        try:
            start_date = '1900-01-01'
            end_date = date.today()
            data = pd.DataFrame()

            for year in range(1900, end_date.year + 1):
                start = f'{year}-01-01'
                end = f'{year}-12-31' if year < end_date.year else end_date.strftime('%Y-%m-%d')
                temp_data = yf.download(company_name + '.NS', start=start, end=end, progress=False)
                st.write(temp_data)
                data = pd.concat([data, temp_data])

            st.write("Data since 1900-01-01 to date of usage:")
            st.dataframe(data)
            
            columns = ['Close', 'Adj Close', 'Volume', 'Open']
            column_titles = {'Close': 'Closing Stock Prices', 'Adj Close': 'Adjusted Closing Stock Prices', 'Volume': 'Share Trade Volume', 'Open': 'Opening Stock Prices'}
            column_desc = {'Close': 'The closing price of the stock at the end of the trading day.', 
                        'Adj Close': 'The adjusted closing price of the stock at the end of the trading day, adjusted for dividends and splits.', 
                        'Volume': 'The number of shares traded during the day.',
                        'Open': 'The opening price of the stock at the beginning of the trading day.'}
            plot_descriptions = {
                'Close': 'This graph shows the trend of closing stock prices for the selected company over the specified time period.',
                'Adj Close': 'This graph shows the trend of adjusted closing stock prices for the selected company over the specified time period.',
                'Volume': 'This graph shows the share trade volume for the selected company over the specified time period.',
                'Close-Adj Close': "This graph compares the trend of closing stock prices and adjusted closing stock prices for the selected company over the specified time period. This is important so that the investor can know about the dividend payouts of the stock. Contrary to popular belief, the majority of an investor's earnings come from dividend payouts, and not the resale value of the stock he/she holds.",
                'Close-Open': "This graph compares the trend of closing stock prices and opening stock prices for the selected company over the specified time period. This is important so that the investor can know about the daily price movement of the stock."
            }
            
            option = st.selectbox('Select a plot:', ['Close', 'Adj Close', 'Volume', 'Close-Adj Close', 'Close-Open'])
            
            if option == 'Close':
                st.write(f"**You selected: {column_titles[option]}**")
                st.write(f"{column_desc[option]}")
                st.write(f"{plot_descriptions[option]}")
                fig, ax = plt.subplots(figsize=(10,6))
                plt.style.use('dark_background')  # Set dark background
                ax.spines['bottom'].set_color('white')  # Set axis color
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.plot(data[option])
                st.pyplot(fig)
            elif option == 'Adj Close':
                st.write(f"**You selected: {column_titles[option]}**")
                st.write(f"{column_desc[option]}")
                st.write(f"{plot_descriptions[option]}")
                fig, ax = plt.subplots(figsize=(10,6))
                plt.style.use('dark_background')  # Set dark background
                ax.spines['bottom'].set_color('white')  # Set axis color
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.plot(data[option])
                st.pyplot(fig)
            elif option == 'Volume':
                st.write(f"**You selected: {column_titles[option]}**")
                st.write(f"{column_desc[option]}")
                st.write(f"{plot_descriptions[option]}")
                fig, ax = plt.subplots(figsize=(10,6))
                plt.style.use('dark_background')  # Set dark background
                ax.spines['bottom'].set_color('white')  # Set axis color
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.plot(data[option])
                st.pyplot(fig)
            elif option == 'Close-Adj Close':
                st.write(f"**You selected: {column_titles[option]}**")
                st.write(f"{column_desc[option]}")
                st.write(f"{plot_descriptions[option]}")
                fig, ax = plt.subplots(figsize=(10,6))
                plt.style.use('dark_background')  # Set dark background
                ax.spines['bottom'].set_color('white')  # Set axis color
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.plot(data['Close'], label='Close')
                ax.plot(data['Adj Close'], label='Adj Close')
                ax.legend()
                st.pyplot(fig)
            elif option == 'Close-Open':
                st.write(f"**You selected: {column_titles[option]}**")
                st.write(f"{column_desc[option]}")
                st.write(f"{plot_descriptions[option]}")
                fig, ax = plt.subplots(figsize=(10,6))
                plt.style.use('dark_background')  # Set dark background
                ax.spines['bottom'].set_color('white')  # Set axis color
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.plot(data['Close'], label='Close')
                ax.plot(data['Open'], label='Open')
                ax.legend()
                st.pyplot(fig)
        except Exception as e:
            st.write("Error: Unable to download data for the specified company. Please check the company ticker symbol and try again.")
            st.write(str(e))

if __name__ == '__main__':
    main()
