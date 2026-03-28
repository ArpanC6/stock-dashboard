from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from data_engine import StockDataEngine

app = FastAPI(title="Stock Data Intelligence Dashboard")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

engine = StockDataEngine()

@app.on_event("startup")
async def startup_event():
    engine.load_data()
    print("✅ Data loaded!")

@app.get("/", response_class=HTMLResponse)
async def root():
    return Path("templates/index.html").read_text()

@app.get("/companies")
async def get_companies():
    return {"companies": engine.get_companies()}

@app.get("/data/{symbol}")
async def get_stock_data(symbol: str, days: int = Query(30)):
    data = engine.get_stock_data(symbol.upper(), days)
    if data is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return {"symbol": symbol.upper(), "days": days, "data": data}

@app.get("/summary/{symbol}")
async def get_summary(symbol: str):
    summary = engine.get_summary(symbol.upper())
    if summary is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return {"symbol": symbol.upper(), "summary": summary}

@app.get("/compare")
async def compare_stocks(symbol1: str, symbol2: str, days: int = Query(30)):
    result = engine.compare_stocks(symbol1.upper(), symbol2.upper(), days)
    if result is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return result

@app.get("/gainers-losers")
async def get_gainers_losers(days: int = Query(7)):
    return engine.get_gainers_losers(days)

@app.get("/volatility")
async def get_volatility():
    return engine.get_volatility_scores()

@app.get("/correlation")
async def get_correlation(symbol1: str, symbol2: str):
    result = engine.get_correlation(symbol1.upper(), symbol2.upper())
    if result is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return result