import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import requests
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

def get_nse_historical_data(symbol, start_date, end_date):
    url = f"https://finance.google.com/finance/historical?q={symbol}&startdate={start_date}&enddate={end_date}&output=csv"
    response = requests.get(url)
    data = response.text
    df = pd.read_csv(io.StringIO(data))
    return df

def main():
    st.title("Welcome to S.T.O.C (Strategic Trading Optimization Console)!")
    
    company_name = st.text_input("Enter a company ticker symbol (e.g. NSE:INFY):")
    
    if company_name:
        try:
            start_date = st.date_input("Enter start date:")
            end_date = st.date_input("Enter end date:")
            df = get_nse_historical_data(company_name, start_date.strftime("%b %d, %Y"), end_date.strftime("%b %d, %Y"))
            
            st.write("Data:")
            st.dataframe(df)
            
            df.to_csv(f'{company_name}.csv', mode='a', header=False, index=True)
            
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            column_titles = {'Open': 'Opening Price', 'High': 'Highest Price', 'Low': 'Lowest Price', 'Close': 'Closing Price', 'Volume': 'Share Trade Volume'}
            column_desc = {'Open': 'The opening price of the stock.', 
                        'High': 'The highest price of the stock during the day.',
                        'Low': 'The lowest price of the stock during the day.',
                        'Close': 'The closing price of the stock.',
                        'Volume': 'The number of shares traded during the day.'}
            plot_descriptions = {
                'Open': 'This graph shows the trend of opening prices for the selected company.',
                'High': 'This graph shows the trend of highest prices for the selected company.',
                'Low': 'This graph shows the trend of lowest prices for the selected company.',
                'Close': 'This graph shows the trend of closing prices for the selected company.',
                'Volume': 'This graph shows the share trade volume for the selected company.',
                'Open-Close': "This graph compares the trend of opening and closing prices for the selected company."
            }
            
            option = st.selectbox('Select a plot:', ['Open', 'High', 'Low', 'Close', 'Volume', 'Open-Close'])
            
            if option == 'Open':
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
                ax.plot(df[option])
                st.pyplot(fig)
            elif option == 'High':
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
                ax.plot(df[option])
                st.pyplot(fig)
            elif option == 'Low':
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
                ax.plot(df[option])
                st.pyplot(fig)
            elif option == 'Close':
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
                ax.plot(df[option])
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
                ax.plot(df[option])
                st.pyplot(fig)
            elif option == 'Open-Close':
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
                ax.plot(df['Open'], label='Opening Price')
                ax.plot(df['Close'], label='Closing Price')
                ax.legend()
                st.pyplot(fig)
        except Exception as e:
            st.write("Error: Unable to download data for the specified company. Please check the company ticker symbol and try again.")
            st.write(str(e))

if __name__ == '__main__':
    main()
