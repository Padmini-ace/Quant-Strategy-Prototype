import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from datetime import datetime

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet - Matches the name in your main.py
SHEET_NAME = "AlgoTrading"   
try:
    worksheet = client.open(SHEET_NAME).worksheet("TradeLog")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    df = pd.DataFrame()

# Streamlit dashboard config
st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")

st.title("📊 Algo Trading Dashboard")
st.subheader("Live Trade Log Results")

if df.empty:
    st.warning("No data found in Google Sheet.")
else:
    # --- DATA CLEANING ---
    # Convert Timestamp to datetime objects
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    
    # Professional touch: Sort by time so the chart flows correctly
    df = df.sort_values("Timestamp")

    # --- DISPLAY METRICS ---
    # Show the raw trade log
    st.dataframe(df)

    st.subheader("📈 Performance Summary")
    col1, col2 = st.columns(2)

    # Calculate stats using the cleaned data
    avg_return = df["TotalReturn%"].mean()
    avg_accuracy = df["MLAccuracy%"].mean()

    with col1:
        st.metric("Average Return", f"{avg_return:.2f}%")
    with col2:
        st.metric("ML Model Accuracy", f"{avg_accuracy:.2f}%")

    # --- CHART VISUALIZATION ---
    st.subheader("📊 Returns Over Time")
    
    # We use the TradeLog specifically because it doesn't have "TOTAL" rows, 
    # making it perfect for time-series visualization.
    chart_data = df.set_index("Timestamp")[["TotalReturn%", "MLAccuracy%"]]
    st.line_chart(chart_data)
