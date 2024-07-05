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

def main():
    st.title("Welcome to S.T.O.C (Strategic Trading Optimization Console)!")

    company_data = pd.read_csv("C:\\Users\\91891\\Downloads\\Directory - Sheet1 (1).csv")

    company_name = st.selectbox("Select a company:", company_data["NAME OF COMPANY"])

    if company_name:
        try:
            ticker_symbol = company_data.loc[company_data["NAME OF COMPANY"] == company_name, "NSE CODE"].values[0]

            print("Ticker symbol:", ticker_symbol)

            file_path = f"D:\\Datasets\\{ticker_symbol}.csv"
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)

                print("Data loaded:", data.head())

                data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

                print("Data converted:", data.head())

                min_date = data['Date'].min()
                max_date = data['Date'].max()

                print("Min date:", min_date)
                print("Max date:", max_date)

                start_date = st.date_input("Select start date:", value=min_date, min_value=min_date, max_value=max_date)
                end_date = st.date_input("Select end date:", value=max_date, min_value=min_date, max_value=max_date)

                print("Start date:", start_date)
                print("End date:", end_date)

                start_date_pd = pd.to_datetime(start_date)
                end_date_pd = pd.to_datetime(end_date)

                print("Start date pd:", start_date_pd)
                print("End date pd:", end_date_pd)

                data_filtered = data[(data['Date'] >= start_date_pd) & (data['Date'] <= end_date_pd)]

                print("Data filtered:", data_filtered.head())

                st.write("Loaded data from local CSV file:")

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
                    plt.style.use('dark_background')  # Set dark background
                    ax.spines['bottom'].set_color('black')  # Set black border
                    ax.spines['left'].set_color('black')  # Set black border
                    ax.tick_params(axis='x', colors='white')  # Set white tick labels
                    ax.tick_params(axis='y', colors='white')  # Set white tick labels
                    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines
                    ax.plot(data_filtered['Date'], data_filtered[option], color='blue')  # Set blue plot lines
                    ax.set_title(f'{ticker_symbol} {column_titles[option]} Over Time', color='white')  # Set white title
                    ax.set_xlabel('Date', color='white')  # Set white x-axis label
                    ax.set_ylabel(column_titles[option], color='white')  # Set white y-axis label
                    st.pyplot(fig)  # Move this line inside the loop to display each plot separately

                elif option == 'Adj Close':
                    st.write(f"**You selected: {column_titles[option]}**")
                    st.write(f"{column_desc[option]}")
                    st.write(f"{plot_descriptions[option]}")
                    fig, ax = plt.subplots(figsize=(10,6))
                    plt.style.use('dark_background')  # Set dark background
                    ax.spines['bottom'].set_color('black')  # Set black border
                    ax.spines['left'].set_color('black')  # Set black border
                    ax.tick_params(axis='x', colors='white')  # Set white tick labels
                    ax.tick_params(axis='y', colors='white')  # Set white tick labels
                    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines
                    ax.plot(data_filtered['Date'], data_filtered[option], color='blue')  # Set blue plot lines
                    ax.set_title(f'{ticker_symbol} {column_titles[option]} Over Time', color='white')  # Set white title
                    ax.set_xlabel('Date', color='white')  # Set white x-axis label
                    ax.set_ylabel(column_titles[option], color='white')  # Set white y-axis label
                    st.pyplot(fig)  # Move this line inside the loop to display each plot separately

                elif option == 'Variability Index':
                    st.write(f"**You selected: {column_titles[option]}**")
                    st.write(f"{column_desc[option]}")
                    st.write(f"{plot_descriptions[option]}")
                    fig, ax = plt.subplots(figsize=(10,6))
                    plt.style.use('dark_background')  # Set dark background
                    ax.spines['bottom'].set_color('black')  # Set black border
                    ax.spines['left'].set_color('black')  # Set black border
                    ax.tick_params(axis='x', colors='white')  # Set white tick labels
                    ax.tick_params(axis='y', colors='white')  # Set white tick labels
                    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines
                    ax.plot(data_filtered['Date'], data_filtered[option], color='blue')  # Set blue plot lines
                    ax.set_title(f'{ticker_symbol} {column_titles[option]} Over Time')  # Set white title
                    ax.set_xlabel('Date', color='white')  # Set white x-axis label
                    ax.set_ylabel(column_titles[option], color='white')  # Set white y-axis label
                    st.pyplot(fig)  # Move this line inside the loop to display each plot separately

                elif option == 'Volume':
                    st.write(f"**You selected: {column_titles[option]}**")
                    st.write(f"{column_desc[option]}")
                    st.write(f"{plot_descriptions[option]}")
                    fig, ax = plt.subplots(figsize=(10,6))
                    plt.style.use('dark_background')  # Set dark background
                    ax.spines['bottom'].set_color('black')  # Set black border
                    ax.spines['left'].set_color('black')  # Set black border
                    ax.tick_params(axis='x', colors='white')  # Set white tick labels
                    ax.tick_params(axis='y', colors='white')  # Set white tick labels
                    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines
                    ax.bar(data_filtered['Date'], data_filtered[option], color='blue')  # Set blue plot lines
                    ax.set_title(f'{ticker_symbol} {column_titles[option]} Over Time', color='white')  # Set white title
                    ax.set_xlabel('Date', color='white')  # Set white x-axis label
                    ax.set_ylabel(column_titles[option], color='white')  # Set white y-axis label
                    st.pyplot(fig)  # Move this line inside the loop to display each plot separately

                elif option == 'Close-Adj Close':
                    st.write(f"**You selected: {column_titles['Close']} and {column_titles['Adj Close']}**")
                    st.write(f"{column_desc['Close']} and {column_desc['Adj Close']}")
                    st.write(f"{plot_descriptions[option]}")
                    fig, ax = plt.subplots(figsize=(10,6))
                    plt.style.use('dark_background')  # Set dark background
                    ax.spines['bottom'].set_color('black')  # Set black border
                    ax.spines['left'].set_color('black')  # Set black border
                    ax.tick_params(axis='x', colors='white')  # Set white tick labels
                    ax.tick_params(axis='y', colors='white')  # Set white tick labels
                    ax.grid(True, color='white', linestyle='--', linewidth=0.5)  # Set white grid lines
                    ax.plot(data_filtered['Date'], data_filtered['Close'], color='blue', label='Close')  # Set blue plot lines
                    ax.plot(data_filtered['Date'], data_filtered['Adj Close'], color='red', label='Adj Close')  # Set red plot lines
                    ax.set_title(f'{ticker_symbol} {column_titles["Close"]} and {column_titles["Adj Close"]} Over Time"]', color='white')  # Set white title
                    ax.set_xlabel('Date', color='white')  # Set white x-axis label
                    ax.set_ylabel('Price', color='white')  # Set white y-axis label
                    ax.legend()  # Add legend
                    st.pyplot(fig)  # Move this line inside the loop to display each plot separately
            else:
                st.write("Error: No data found for the selected ticker symbol.")
        except Exception as e:
            st.write("Error:", str(e))
if __name__ == "__main__":
    main()
