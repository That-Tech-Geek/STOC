import pandas as pd
import yfinance as yf
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

def download_ticker_data(ticker_symbol, start_date, end_date):
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return data

def plot_data(data, option, ticker_symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    plt.style.use('dark_background')  # Set dark background
    ax.spines['bottom'].set_color('black')  # Set black border
    ax.spines['left'].set_color('black')  # Set black border
    ax.tick_params(axis='x', colors='white')  # Set white tick labels
    ax.tick_params(axis='y', colors='white')  # Set white tick labels
    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines

    if option == 'Close':
        ax.plot(data.index, data['Close'], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Closing Stock Prices Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Price', color='white')  # Set white y-axis label
    elif option == 'Adj Close':
        ax.plot(data.index, data['Adj Close'], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Adjusted Closing Stock Prices Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Price', color='white')  # Set white y-axis label
    elif option == 'Variability Index':
        ax.plot(data.index, data['Volume'], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Variability Index Over Time', color='white')  # Set white title
        ax.set_xlabel('Date', color='white')  # Set white x-axis label
        ax.set_ylabel('Index', color='white')  # Set white y-axis label
    elif option == 'Volume':
        ax.bar(data.index, data['Volume'], color='blue')  # Set blue plot lines
        ax.set_title(f'{ticker_symbol} Share Trade Volume Over Time', color='white')  # Set white title
