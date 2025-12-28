<h1><b>Quant-Startegy-Prototype</b></h1>
An end-to-end quantitative research pipeline for market analysis, predictive modeling, and performance monitoring.
This repository contains a modular framework designed to handle the full lifecycle of a quantitative trading strategy: from raw data ingestion and feature engineering to machine learning-based direction prediction and cloud-integrated analytics.

<b>🏗️ System Architecture</b>
The pipeline is architected to ensure a clear separation of concerns, moving beyond simple scripting into a structured research workflow:
<table style="width:100%; border-collapse: collapse; font-family: sans-serif; background-color: #1a1a1a; color: #fff;">
  <thead>
    <tr style="background-color: #00ff88; color: #000;">
      <th style="padding: 12px; border: 1px solid #333;">Layer</th>
      <th style="padding: 12px; border: 1px solid #333;">Responsibility</th>
      <th style="padding: 12px; border: 1px solid #333;">Key Technologies</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #333;"><b>Data Layer</b></td>
      <td style="padding: 10px; border: 1px solid #333;">Historical data ingestion with IPv4 stability hacks</td>
      <td style="padding: 10px; border: 1px solid #333;">yfinance, socket</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #333;"><b>Logic Layer</b></td>
      <td style="padding: 10px; border: 1px solid #333;">Signal generation via technical indicators (RSI, MA)</td>
      <td style="padding: 10px; border: 1px solid #333;">pandas, ta</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #333;"><b>Predictive Layer</b></td>
      <td style="padding: 10px; border: 1px solid #333;">Directional price forecasting via Logistic Regression</td>
      <td style="padding: 10px; border: 1px solid #333;">scikit-learn</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #333;"><b>Logging Layer</b></td>
      <td style="padding: 10px; border: 1px solid #333;">Cloud-based logging for persistent performance tracking across multiple runs.</td>
      <td style="padding: 10px; border: 1px solid #333;">gspread, Google Sheets API</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #333;"><b>View Layer</b></td>
      <td style="padding: 10px; border: 1px solid #333;">Performance visualization and metrics dashboard</td>
      <td style="padding: 10px; border: 1px solid #333;">Streamlit</td>
    </tr>
  </tbody>
</table>

<b>🛠️ Key Technical Features</b>
1. Robust Data PipelineStability: Implements a custom socket wrapper to force IPv4, resolving common API timeout issues with Indian ISPs.Feature Engineering: Automated computation of Mean Reversion (RSI) and Trend-Following (Moving Average) indicators.
2. Predictive Modeling (Experimental)Time-Series Integrity: Uses non-shuffled train-test splits to prevent look-ahead bias and data leakage.Objective Function: Binary classification targeting next-day price direction ($C_{t+1} > C_t$).
   (*This prediction task is exploratory and not directly optimized for trading profitability.)
4. Analytics & PersistenceCloud Integration: Asynchronous logging to Google Sheets for persistent performance tracking across multiple runs.Interactive Dashboard: A dedicated Streamlit interface to monitor "Strategy Returns" vs "ML Accuracy" across experimental runs.

<b>📂 Project Structure</b>

Quant-Strategy-Prototype/

│

├── main.py              # Quantitative pipeline (Data -> Signal -> ML -> Log)

├── dashboard.py         # Streamlit-based performance analytics UI

├── credentials.json     # Google Cloud Service Account Key (Not in Repo)

├── requirements.txt     # Environment dependencies

├── .gitignore           # Security: Protects API keys and local caches

└── README.md            # Technical documentation


<b>⚙️ Deployment & Usage</b>
1. Environment Setup
   # Clone the repository
git clone https://github.com/Padmini-ace/Quant-Strategy-Prototype.git
cd Quant-Strategy-Prototype

# Install dependencies
pip install -r requirements.txt

2. Execution Flow
   a)Research Pipeline: Run python main.py to fetch data, generate signals, and log results to the cloud.
   b)Analytics Dashboard: Run streamlit run dashboard.py to view the performance metrics and equity curve.

<b>🧪 Roadmap & Future Improvements</b>

[ ] Walk-Forward Validation: Implementing rolling-window cross-validation for the ML model.

[ ] Transaction Modeling: Adding slippage and brokerage commission (0.1% per trade) to backtest math.

[ ] Risk Framework: Integrating ATR-based dynamic stop-losses and position sizing.
