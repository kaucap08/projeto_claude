# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

Three-module structure with clear separation of concerns:

- **`data.py`** — Data layer. Fetches OHLCV data from Yahoo Finance via `yfinance`. `get_stock_data(start, end)` returns a `dict[str, pd.DataFrame]` keyed by stock name. Results are cached for 1 hour via `@st.cache_data(ttl=3600)`. `TICKERS` maps display names to Yahoo Finance symbols.

- **`charts.py`** — Visualization layer. Receives DataFrames from the data layer and returns `plotly.graph_objects.Figure` objects. `COLORS` centralizes brand colors. All charts use the `plotly_dark` theme.

- **`app.py`** — Presentation layer. Streamlit UI: sidebar date filters → calls `get_stock_data()` → passes DataFrames to chart functions → renders via `st.plotly_chart()`.

**Data flow:** User selects dates → `data.get_stock_data()` fetches/returns cached data → chart functions build Plotly figures → Streamlit renders.

## Stocks Tracked

Petrobras (PETR4), Itaú (ITUB4), Vale (VALE3) — Brazilian B3 exchange, data from Jan 2, 2025 onward.

## GitHub Sync

Repository: https://github.com/kaucap08/projeto_claude

A PostToolUse hook in `.claude/settings.local.json` auto-commits and pushes every time a file is written or edited. The hook runs async, commits with message `auto: update <filename>`, and pushes to `origin main`. The GitHub token is embedded in the remote URL — do not expose it in logs or output.
