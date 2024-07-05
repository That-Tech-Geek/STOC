import pandas as pd
import os
import matplotlib.pyplot as plt
import streamlit as st
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

def download_ticker_data(ticker_symbol):
    file_path = f"D:\\Datasets\\{ticker_symbol}.csv"
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        return data
    else:
        st.write("Error: No data found for the selected ticker symbol.")
        return None

def plot_data(data, option, ticker_symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    plt.style.use('dark_background')  # Set dark background
    ax.spines['bottom'].set_color('black')  # Set black border
    ax.spines['left'].set_color('black')  # Set black border
    ax.tick_params(axis='x', colors='white')  # Set white tick labels
    ax.tick_params(axis='y', colors='white')  # Set white tick labels
    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines

    if option == 'Close':
        ax.plot(data['Date'], data[option], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Closing Stock Prices Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Price', color='white')  # Set white y-axis label
    elif option == 'Adj Close':
        ax.plot(data['Date'], data[option], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Adjusted Closing Stock Prices Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Price', color='white')  # Set white y-axis label
    elif option == 'Variability Index':
        ax.plot(data['Date'], data[option], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Variability Index Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Index', color='white')  # Set white y-axis label
    elif option == 'Volume':
        ax.bar(data['Date'], data[option], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Share Trade Volume Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Volume', color='white')  # Set white y-axis label
    elif option == 'Close-Adj Close':
        ax.plot(data['Date'], data['Close'], color='blue', label='Close')  # Set blue plot lines
        ax.plot(data['Date'], data['Adj Close'], color='red', label='Adj Close')  # Set red plot lines
        ax.set_title(f'{ticker_symbol} Closing and Adjusted Closing Stock Prices Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Price', color='white')  # Set white y-axis label
        ax.legend()  # Add legend

    st.pyplot(fig)  # Display the plot

def main():
    st.title("Welcome to S.T.O.C (Strategic Trading Optimization Console)!")
    company_data = pd.read_csv("C:\\Users\\91891\\Downloads\\Directory - Sheet1 (1).csv")

    company_name = st.selectbox("Select a company:", company_data["NAME OF COMPANY"])

    if company_name:
        try:
            ticker_symbol = company_data.loc[company_data["NAME OF COMPANY"] == company_name, "NSE CODE"].values[0]
            data = download_ticker_data(ticker_symbol)

            if data is not None:
                data['Date
