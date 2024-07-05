import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from alpha_vantage.timeseries import TimeSeries
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
            api_key = 'YOUR_API_KEY'  # Replace with your Alpha Vantage API key
            ts = TimeSeries(key=api_key, output_format='pandas')
            data, meta_data = ts.get_daily_adjusted(symbol=company_name, outputsize='full')
            
            st.write("Data since 1900-01-01 to date of usage:")
            st.dataframe(data)
            
            data.to_csv(f'{company_name}.csv', mode='a', header=False, index=True)
            
            columns = ['4. close', '5. adjusted close', '6. volume', '1. open']
            column_titles = {'4. close': 'Closing Stock Prices', '5. adjusted close': 'Adjusted Closing Stock Prices', '6. volume': 'Share Trade Volume', '1. open': 'Opening Stock Prices'}
            column_desc = {'4. close': 'The closing price of the stock at the end of the trading day.', 
                        '5. adjusted close': 'The adjusted closing price of the stock at the end of the trading day, adjusted for dividends and splits.', 
                        '6. volume': 'The number of shares traded during the day.',
                        '1. open': 'The opening price of the stock at the beginning of the trading day.'}
            plot_descriptions = {
                '4. close': 'This graph shows the trend of closing stock prices for the selected company over the specified time period.',
                '5. adjusted close': 'This graph shows the trend of adjusted closing stock prices for the selected company over the specified time period.',
                '6. volume': 'This graph shows the share trade volume for the selected company over the specified time period.',
                '4. close-5. adjusted close': "This graph compares the trend of closing stock prices and adjusted closing stock prices for the selected company over the specified time period. This is important so that the investor can know about the dividend payouts of the stock. Contrary to popular belief, the majority of an investor's earnings come from dividend payouts, and not the resale value of the stock he/she holds.",
                '4. close-1. open': "This graph compares the trend of closing stock prices and opening stock prices for the selected company over the specified time period. This is important so that the investor can know about the daily price movement of the stock."
            }
            
            option = st.selectbox('Select a plot:', ['4. close', '5. adjusted close', '6. volume', '4. close-5. adjusted close', '4. close-1. open'])
            
            if option == '4. close':
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
            elif option == '5. adjusted close':
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
            elif option == '6. volume':
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
            elif option == '4. close-5. adjusted close':
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
                ax.plot(data['4. close'], label='Close')
                ax.plot(data['5. adjusted close'], label='Adj Close')
                ax.legend()
                st.pyplot(fig)
            elif option == '4. close-1. open':
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
                ax.plot(data['4. close'], label='Close')
                ax.plot(data['1. open'], label='Open')
                ax.legend()
                st.pyplot(fig)
        except Exception as e:
            st.write("Error: Unable to download data for the specified company. Please check the company ticker symbol and try again.")
            st.write(str(e))

if __name__ == '__main__':
    main()
