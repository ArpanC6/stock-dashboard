# 📈 Stock Data Intelligence Dashboard
### Jarnox Software Internship Assignment

**Author:** Arpan Chakraborty  
**Live Demo:** [https://stock-dashboard-8ovm.onrender.com](https://stock-dashboard-8ovm.onrender.com)  
**API Docs:** [https://stock-dashboard-8ovm.onrender.com/docs](https://stock-dashboard-8ovm.onrender.com/docs)

---

## 🧠 Overview

A mini financial data platform that collects, processes, and visualizes **NSE stock market data** through a REST API and an interactive dark-theme dashboard. Built as a complete, production-ready application with real financial metrics and multi-stock analysis capabilities.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Backend | FastAPI |
| Data Processing | Pandas, NumPy |
| Frontend | HTML + JavaScript + Chart.js |
| API Documentation | Swagger UI (`/docs`) |
| Deployment | Render.com |

---

## 🚀 Setup and Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/ArpanC6/stock-dashboard.git
cd stock-dashboard
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Open in browser**
- Dashboard → http://localhost:8000
- API Docs (Swagger) → http://localhost:8000/docs

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/companies` | List of all NSE companies |
| `GET` | `/data/{symbol}?days=30` | Last N days of stock data |
| `GET` | `/summary/{symbol}` | 52-week high, low, and average |
| `GET` | `/compare?symbol1=INFY&symbol2=TCS` | Side-by-side comparison of two stocks |
| `GET` | `/gainers-losers?days=7` | Top gainers and losers |
| `GET` | `/volatility` | Volatility scores for all stocks |
| `GET` | `/correlation?symbol1=INFY&symbol2=TCS` | Correlation coefficient between two stocks |

> Full interactive API documentation available at `/docs` (Swagger UI)

---

## 📊 Data & Metrics

| Metric | Formula / Description |
|---|---|
| **Daily Return** | `(Close - Open) / Open × 100` |
| **Moving Average** | 7-day and 20-day rolling average |
| **52-week High/Low** | Annual price range per stock |
| **Volatility Score** | 14-day rolling standard deviation of returns |
| **Sentiment Index** | Combination of price momentum and volume trend |

---

## 🖥️ Dashboard Features

**Overview Tab**
- Interactive price chart with MA7 overlay
- Daily return bar chart
- Key stats: 52-week high/low, average, volatility

**Compare Tab**
- Side-by-side price chart of two stocks
- Correlation analysis with score display

**Market View Tab**
- Top gainers and losers (last 7 days)
- Volatility comparison chart across all stocks

---

## 📁 Project Structure

```
stock-dashboard/
├── main.py           # FastAPI app and all API endpoints
├── data_engine.py    # Data processing and metrics computation
├── templates/
│   └── index.html    # Interactive dark-theme dashboard
├── requirements.txt  # Python dependencies
└── README.md
```

---

## 🌐 Deployment

This project is deployed live on **Render.com** (free tier).

> ⚠️ Note: Free instances spin down after inactivity. The first request may take up to 50 seconds to load.

- **Live URL:** https://stock-dashboard-8ovm.onrender.com
- **API Docs:** https://stock-dashboard-8ovm.onrender.com/docs

---

## 📬 Submission

| | |
|---|---|
| **GitHub** | https://github.com/ArpanC6/stock-dashboard |
| **Submitted to** | support@jarnox.com |
| **Author** | Arpan Chakraborty |
