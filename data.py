import yfinance as yf
import pandas as pd
import streamlit as st

TICKERS = {
    "Petrobras (PETR4)": "PETR4.SA",
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
}

@st.cache_data(ttl=3600)
def get_stock_data(start: str, end: str) -> dict[str, pd.DataFrame]:
    data = {}
    for name, ticker in TICKERS.items():
        df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        if not df.empty:
            df.index = pd.to_datetime(df.index)
            data[name] = df
    return data


def compute_cumulative_return(close_series: pd.Series) -> pd.Series:
    return (close_series / close_series.iloc[0] - 1) * 100
