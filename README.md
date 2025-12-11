AlgoTrading Automation

An end-to-end algorithmic trading prototype that integrates technical indicators, machine learning-based market direction prediction, Google Sheets reporting, and a Streamlit dashboard for monitoring performance.

This project demonstrates how to build a complete automated trading analysis system using real market data, feature engineering, backtesting logic, and cloud-based logging.

Key Features:

1. Automated Data Pipeline:

* Fetches market data using Yahoo Finance
* Computes RSI, 20-day MA, 50-day MA
* Generates buy and sell signals based on indicator conditions

2. Machine Learning Prediction:

* Logistic Regression prediction for next-day price direction
* Train-test split preserving time order
* Logs prediction accuracy for every run

3. Strategy Backtesting

* Computes returns based on signal performance
* Calculates win ratio and cumulative strategy profitability
* Generates per-stock performance summaries

4. Cloud-Based Logging (Google Sheets):

* Logs all outputs to Google Sheets through the Google Sheets API
* Maintains:

  * TradeLog
  * SummaryPNL
  * WinRatio

5. Streamlit Dashboard:

* Displays logged trades
* Shows performance summaries
* Visualizes return trends over time
* Provides a simple, interactive interface for reviewing results

Tech Stack:

* Python
* Pandas, NumPy, scikit-learn
* TA indicators (RSI, Moving Averages)
* Yahoo Finance API (yfinance)
* Google Sheets API (gspread, OAuth2)
* Streamlit

Installation and Setup

1. Clone the repository:
git clone https://github.com/Padmini-ace/AlgoTrading-Automation
cd AlgoTrading-Automation

2. Install dependencies:
pip install -r requirements.txt

3. Add Google Sheets credentials

Place your service account file in the root directory as:
credentials.json

Ensure the service account has access to your Google Sheet.

4. Prepare Google Sheets

Create a Google Sheet named:
AlgoTrading

The script will auto-create the necessary worksheets:

* TradeLog
* SummaryPNL
* WinRatio

Running the Algorithm:
python main.py

This will:

1. Fetch market data
2. Compute indicators
3. Generate ML predictions
4. Backtest the strategy
5. Log outputs to Google Sheets
6. Print a summary to the console


Launching the Dashboard:
streamlit run dashboard.py

This will open a browser interface showing:
* Trade logs
* ML accuracy metrics
* Return trends
* Per-stock summaries

Project Structure:

AlgoTrading-Automation/
│
├── main.py                 # Core trading and ML pipeline
├── dashboard.py            # Streamlit dashboard interface
├── credentials.json        # Google API credentials (excluded from git)
├── requirements.txt        # Dependencies
├── .gitattributes
└── README.md

Current Limitations:

* Backtesting logic is simplified
* Machine learning model is basic and does not use walk-forward validation
* Transaction costs and slippage are not modeled
* Logging uses Google Sheets instead of a full database

Future Improvements:

* Advanced backtesting with Sharpe ratio and drawdown analysis
* Walk-forward cross-validation for ML models
* Improved feature engineering (volatility, ATR, momentum factors)
* Risk management and position sizing
* Database backend for scalable logging
* A more advanced dashboard

Purpose of the Project:

This project is intended as a learning-level prototype exploring the complete workflow of:
Data acquisition → Indicator computation → Machine learning → Backtesting → Cloud logging → Visualization
It serves as a starting point for understanding automated trading system design, not as a live trading solution.



