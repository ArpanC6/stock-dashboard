import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Any, List

COMPANIES = {
    "RELIANCE": "Reliance Industries",
    "TCS": "Tata Consultancy Services",
    "INFY": "Infosys",
    "HDFCBANK": "HDFC Bank",
    "ICICIBANK": "ICICI Bank",
    "WIPRO": "Wipro",
    "SBIN": "State Bank of India",
    "BAJFINANCE": "Bajaj Finance",
    "HINDUNILVR": "Hindustan Unilever",
    "MARUTI": "Maruti Suzuki",
}

BASE_PRICES = {
    "RELIANCE": 2800, "TCS": 3600, "INFY": 1700, "HDFCBANK": 1600,
    "ICICIBANK": 1100, "WIPRO": 480, "SBIN": 750, "BAJFINANCE": 7000,
    "HINDUNILVR": 2400, "MARUTI": 12000,
}

def _generate_ohlcv(symbol: str, days: int = 400) -> pd.DataFrame:
    np.random.seed(hash(symbol) % (2**31))
    base = BASE_PRICES[symbol]
    dates = pd.bdate_range(end=datetime.today(), periods=days)
    n = len(dates)
    returns = np.random.normal(0.0005, 0.015, size=n)
    close = base * np.cumprod(1 + returns)
    high = close * (1 + np.abs(np.random.normal(0, 0.007, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.007, n)))
    open_ = low + np.random.uniform(0, 1, n) * (high - low)
    volume = np.random.randint(500000, 5000000, size=n)
    df = pd.DataFrame({
        "date": dates,
        "open": open_.round(2),
        "high": high.round(2),
        "low": low.round(2),
        "close": close.round(2),
        "volume": volume,
    })
    return df

class StockDataEngine:
    def __init__(self):
        self._data: Dict[str, pd.DataFrame] = {}

    def load_data(self):
        for symbol in COMPANIES:
            df = _generate_ohlcv(symbol)
            df = self._clean(df)
            df = self._add_metrics(df)
            self._data[symbol] = df

    def _clean(self, df):
        df = df.dropna()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
        df = df[df["high"] >= df["low"]]
        return df

    def _add_metrics(self, df):
        df["daily_return"] = ((df["close"] - df["open"]) / df["open"] * 100).round(4)
        df["ma_7"] = df["close"].rolling(window=7).mean().round(2)
        df["ma_20"] = df["close"].rolling(window=20).mean().round(2)
        df["volatility"] = df["daily_return"].rolling(window=14).std().round(4)
        vol_ma = df["volume"].rolling(7).mean()
        momentum = df["close"].pct_change(5) * 100
        df["sentiment"] = ((momentum + (df["volume"] / vol_ma - 1) * 10) / 2).round(2)
        return df

    def get_companies(self):
        return [{"symbol": s, "name": n} for s, n in COMPANIES.items()]

    def get_stock_data(self, symbol, days=30):
        if symbol not in self._data:
            return None
        df = self._data[symbol].tail(days).copy()
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")

    def get_summary(self, symbol):
        if symbol not in self._data:
            return None
        df = self._data[symbol]
        last_year = df.tail(252)
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        return {
            "name": COMPANIES[symbol],
            "current_price": round(float(latest["close"]), 2),
            "change": round(float(latest["close"] - prev["close"]), 2),
            "change_pct": round(float((latest["close"] - prev["close"]) / prev["close"] * 100), 2),
            "week52_high": round(float(last_year["high"].max()), 2),
            "week52_low": round(float(last_year["low"].min()), 2),
            "avg_close": round(float(last_year["close"].mean()), 2),
            "avg_volume": int(last_year["volume"].mean()),
            "volatility_score": round(float(df["volatility"].iloc[-1] or 0), 4),
            "sentiment_index": round(float(df["sentiment"].iloc[-1] or 0), 2),
            "daily_return": round(float(latest["daily_return"]), 4),
        }

    def compare_stocks(self, s1, s2, days=30):
        if s1 not in self._data or s2 not in self._data:
            return None
        def _perf(sym):
            df = self._data[sym].tail(days)
            start = float(df.iloc[0]["close"])
            end = float(df.iloc[-1]["close"])
            return {
                "symbol": sym,
                "name": COMPANIES[sym],
                "start_price": round(start, 2),
                "end_price": round(end, 2),
                "return_pct": round((end - start) / start * 100, 2),
                "avg_volume": int(df["volume"].mean()),
                "volatility": round(float(df["volatility"].mean()), 4),
                "dates": df["date"].dt.strftime("%Y-%m-%d").tolist(),
                "closes": df["close"].round(2).tolist(),
            }
        corr = self.get_correlation(s1, s2)
        return {
            "period_days": days,
            "stock1": _perf(s1),
            "stock2": _perf(s2),
            "correlation": corr["correlation"] if corr else None,
        }

    def get_gainers_losers(self, days=7):
        results = []
        for sym in COMPANIES:
            df = self._data[sym].tail(days)
            start = float(df.iloc[0]["close"])
            end = float(df.iloc[-1]["close"])
            pct = round((end - start) / start * 100, 2)
            results.append({"symbol": sym, "name": COMPANIES[sym], "return_pct": pct, "current_price": round(end, 2)})
        results.sort(key=lambda x: x["return_pct"], reverse=True)
        return {"period_days": days, "top_gainers": results[:3], "top_losers": list(reversed(results[-3:]))}

    def get_volatility_scores(self):
        scores = []
        for sym in COMPANIES:
            df = self._data[sym]
            score = float(df["volatility"].iloc[-1] or 0)
            scores.append({
                "symbol": sym, "name": COMPANIES[sym],
                "volatility_score": round(score, 4),
                "risk_level": "High" if score > 1.5 else ("Medium" if score > 0.8 else "Low"),
            })
        scores.sort(key=lambda x: x["volatility_score"], reverse=True)
        return {"volatility_scores": scores}

    def get_correlation(self, s1, s2):
        if s1 not in self._data or s2 not in self._data:
            return None
        r1 = self._data[s1]["daily_return"].tail(60)
        r2 = self._data[s2]["daily_return"].tail(60)
        corr = round(float(r1.corr(r2)), 4)
        interpretation = (
            "Strong Positive" if corr > 0.7 else
            "Moderate Positive" if corr > 0.3 else
            "Weak/No Correlation" if corr > -0.3 else
            "Moderate Negative" if corr > -0.7 else
            "Strong Negative"
        )
        return {"symbol1": s1, "symbol2": s2, "correlation": corr, "interpretation": interpretation}