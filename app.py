# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# ---------------------------
# App Title
# ---------------------------
st.set_page_config(page_title="Financial Data Dashboard", layout="wide")
st.title("📊 Financial Data Dashboard")
st.write("Interactive dashboard for Stocks, Crypto, and Forex data using Yahoo Finance API.")

# ---------------------------
# Sidebar Inputs
# ---------------------------
st.sidebar.header("Settings")

# Select asset type
asset_type = st.sidebar.selectbox("Choose Asset Type", ["Stock", "Crypto", "Forex"])

# Input ticker
if asset_type == "Stock":
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
elif asset_type == "Crypto":
    ticker = st.sidebar.text_input("Enter Crypto Ticker (e.g., BTC-USD, ETH-USD)", "BTC-USD")
else:
    ticker = st.sidebar.text_input("Enter Forex Pair (e.g., EURUSD=X, JPY=X)", "EURUSD=X")

# Date range
end_date = datetime.today()
start_date = st.sidebar.date_input("Start Date", end_date - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", end_date)

# ---------------------------
# Fetch Data
# ---------------------------
try:
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        st.error("No data found for given ticker. Please try again.")
    else:
        st.success(f"Showing data for: {ticker}")
        
        # ---------------------------
        # Show Raw Data
        # ---------------------------
        st.subheader("📑 Historical Data")
        st.dataframe(data.tail(10))

        # ---------------------------
        # Candlestick Chart
        # ---------------------------
        st.subheader("📈 Price Chart")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'],
                                     name="Candlestick"))
        
        # Moving Averages
        data['MA20'] = data['Close'].rolling(20).mean()
        data['MA50'] = data['Close'].rolling(50).mean()
        
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='blue', width=1), name="MA20"))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], line=dict(color='orange', width=1), name="MA50"))
        
        fig.update_layout(xaxis_rangeslider_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------
        # Key Stats
        # ---------------------------
        st.subheader("📊 Key Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Close", f"${data['Close'][-1]:.2f}")
        col2.metric("20-day Avg", f"${data['MA20'][-1]:.2f}")
        col3.metric("50-day Avg", f"${data['MA50'][-1]:.2f}")
        
except Exception as e:
    st.error(f"Error fetching data: {e}")
