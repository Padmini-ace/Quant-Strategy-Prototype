import yfinance as yf
import pandas as pd
import numpy as np
import ta
import logging
import socket
import gspread
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

# Force Python to use IPv4 instead of IPv6 for API stability
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_wrapper(host, *args, **kwargs):
    return [ai for ai in orig_getaddrinfo(host, *args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = getaddrinfo_wrapper

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --------- GOOGLE SHEETS CONNECTION ----------
def connect_google_sheets(sheet_name="AlgoTrading"):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        logging.info("✅ Connected to Google Sheets successfully.")
        return sheet
    except Exception as e:
        logging.error(f"⚠️ Google Sheets connection failed: {e}")
        return None

# --------- FETCH DATA ----------
def fetch_data(ticker, period="6mo"):
    logging.info(f"Fetching data for {ticker}...")
    df = yf.download(ticker + ".NS", period=period, interval="1d")
    df.dropna(inplace=True)
    return df

# --------- ADD INDICATORS ----------
def add_indicators(df):
    df["RSI"] = ta.momentum.RSIIndicator(close=df["Close"].squeeze(), window=14).rsi()
    df["20MA"] = df["Close"].rolling(window=20).mean()
    df["50MA"] = df["Close"].rolling(window=50).mean()
    return df

# --------- GENERATE SIGNALS ----------
def generate_signals(df):
    df["Signal"] = 0
    # Simple strategy: RSI + Trend confirmation
    df["Signal"] = np.where((df["RSI"] < 30) & (df["20MA"] > df["50MA"]), 1,
                    np.where((df["RSI"] > 70) & (df["20MA"] < df["50MA"]), -1, 0))
    return df

# --------- BACKTEST STRATEGY ----------
def backtest(df):
    df["Return"] = df["Close"].pct_change()
    df["StrategyReturn"] = df["Signal"].shift(1) * df["Return"]
    total_return = df["StrategyReturn"].cumsum().iloc[-1] * 100
    # Calculate win ratio for non-zero signal days
    active_trades = df[df["Signal"] != 0]["StrategyReturn"]
    win_ratio = (active_trades > 0).mean() * 100 if not active_trades.empty else 0
    return total_return, win_ratio

# --------- ML PREDICTION ----------
def ml_predict(df):
    df = df.dropna()
    X = df[["RSI", "20MA", "50MA"]]
    y = np.where(df["Close"].shift(-1) > df["Close"], 1, 0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = LogisticRegression()
    model.fit(X_train, y_train.ravel())
    preds = model.predict(X_test)
    acc = accuracy_score(y_test.ravel(), preds) * 100
    return acc

# --------- LOG TO GOOGLE SHEETS ----------
def log_to_sheets(sheet, stock, total_return, win_ratio, acc):
    # --- 1. Trade Log ---
    try:
        trade_ws = sheet.worksheet("TradeLog")
    except WorksheetNotFound:
        trade_ws = sheet.add_worksheet(title="TradeLog", rows="100", cols="10")
        trade_ws.append_row(["Stock", "TotalReturn%", "WinRatio%", "MLAccuracy%", "Timestamp"])
    
    trade_ws.append_row([stock, round(total_return, 2), round(win_ratio, 2), round(acc, 2), str(datetime.now())])

    # --- 2. Summary P&L (Fixed Logic) ---
    try:
        pnl_ws = sheet.worksheet("SummaryPNL")
    except WorksheetNotFound:
        pnl_ws = sheet.add_worksheet(title="SummaryPNL", rows="100", cols="10")
        pnl_ws.append_row(["Stock", "TotalReturn%"])

    pnl_ws.append_row([stock, round(total_return, 2)])

    # Recalculate Total: Filter out 'TOTAL' and headers to prevent exponential sums
    all_rows = pnl_ws.get_all_values()
    stock_returns = [float(row[1]) for row in all_rows[1:] if row[0] != "TOTAL" and row[1] != ""]
    total_sum = round(sum(stock_returns), 2)

    # Delete old TOTAL row if it exists
    try:
        cell = pnl_ws.find("TOTAL")
        pnl_ws.delete_rows(cell.row)
    except:
        pass

    pnl_ws.append_row(["TOTAL", total_sum])

    # --- 3. Win Ratio Summary ---
    try:
        wr_ws = sheet.worksheet("WinRatio")
    except WorksheetNotFound:
        wr_ws = sheet.add_worksheet(title="WinRatio", rows="100", cols="10")
        wr_ws.append_row(["Stock", "WinRatio%"])
    
    wr_ws.append_row([stock, round(win_ratio, 2)])

    logging.info(f"✅ Logged {stock} results across all sheets.")

# --------- MAIN FUNCTION ----------
def run_algo():
    stocks = ["RELIANCE", "TCS", "HDFCBANK"]
    sheet = connect_google_sheets()

    for stock in stocks:
        df = fetch_data(stock)
        df = add_indicators(df)
        df = generate_signals(df)
        total_return, win_ratio = backtest(df)
        acc = ml_predict(df)

        print(f"\n📊 {stock} Results:")
        print(f"Total Return: {total_return:.2f}% | Win Ratio: {win_ratio:.2f}% | ML Accuracy: {acc:.2f}%")

        if sheet:
            log_to_sheets(sheet, stock, total_return, win_ratio, acc)

if __name__ == "__main__":
    run_algo()
