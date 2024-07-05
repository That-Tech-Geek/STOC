import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from googlefinance import getQuotes
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
            data = getQuotes(company_name)
            df = pd.DataFrame(data)
            
            st.write("Data:")
            st.dataframe(df)
            
            df.to_csv(f'{company_name}.csv', mode='a', header=False, index=True)
            
            columns = ['LastTradePrice', 'Volume', 'Open']
            column_titles = {'LastTradePrice': 'Last Trade Price', 'Volume': 'Share Trade Volume', 'Open': 'Opening Price'}
            column_desc = {'LastTradePrice': 'The last trade price of the stock.', 
                        'Volume': 'The number of shares traded during the day.',
                        'Open': 'The opening price of the stock.'}
            plot_descriptions = {
                'LastTradePrice': 'This graph shows the trend of last trade prices for the selected company.',
                'Volume': 'This graph shows the share trade volume for the selected company.',
                'Open': 'This graph shows the opening prices for the selected company.',
                'LastTradePrice-Open': "This graph compares the trend of last trade prices and opening prices for the selected company."
            }
            
            option = st.selectbox('Select a plot:', ['LastTradePrice', 'Volume', 'Open', 'LastTradePrice-Open'])
            
            if option == 'LastTradePrice':
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
            elif option == 'Open':
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
            elif option == 'LastTradePrice-Open':
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
                ax.plot(df['LastTradePrice'], label='Last Trade Price')
                ax.plot(df['Open'], label='Opening Price')
                ax.legend()
                st.pyplot(fig)
        except Exception as e:
            st.write("Error: Unable to download data for the specified company. Please check the company ticker symbol and try again.")
            st.write(str(e))

if __name__ == '__main__':
    main()
