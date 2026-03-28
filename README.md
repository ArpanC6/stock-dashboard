Stock Data Intelligence Dashboard

Jarnox Software Internship Assignment
Author: Arpan Chakraborty

A mini financial data platform that collects, processes, and visualizes NSE stock market data through a REST API and interactive dashboard.

Tech Stack

Language: Python 3.11+
Backend: FastAPI
Data Processing: Pandas, NumPy
Frontend: HTML + JavaScript + Chart.js
API Docs: Swagger UI at /docs

Setup and Run

Clone the repository:
git clone https://github.com/ArpanC8/stock-dashboard.git
cd stock-dashboard

Create virtual environment:
python -m venv venv
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run the server:
uvicorn main:app --reload

Open in browser:
Dashboard: http://localhost:8000
API Docs: http://localhost:8000/docs

API Endpoints

GET /companies - List of all NSE companies
GET /data/{symbol}?days=30 - Last N days of stock data
GET /summary/{symbol} - 52-week high, low, and average
GET /compare?symbol1=INFY&symbol2=TCS - Compare two stocks
GET /gainers-losers?days=7 - Top gainers and losers
GET /volatility - Volatility scores for all stocks
GET /correlation?symbol1=INFY&symbol2=TCS - Correlation between two stocks

Data and Metrics

Daily Return = (Close - Open) / Open x 100
7-day and 20-day Moving Average
52-week High and Low
Volatility Score: 14-day rolling standard deviation of returns
Sentiment Index: combination of price momentum and volume trend

Dashboard Features

Overview Tab: Price chart with MA7 overlay, daily return bars, key stats
Compare Tab: Side by side chart of two stocks with correlation analysis
Market View Tab: Top gainers and losers, volatility comparison chart

Submission

GitHub: https://github.com/ArpanC8/stock-dashboard
Email: support@jarnox.com