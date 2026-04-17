import streamlit as st
import pandas as pd
from datetime import date
from data import get_stock_data, compute_cumulative_return
from charts import (
    chart_closing_price,
    chart_cumulative_return,
    chart_candlestick,
    chart_volume,
)

st.set_page_config(
    page_title="Performance de Ações 2025",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Performance de Ações Brasileiras — 2025")
st.caption("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

# --- Sidebar ---
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input("Data inicial", value=date(2025, 1, 2), min_value=date(2025, 1, 2), max_value=date.today())
end_date = st.sidebar.date_input("Data final", value=date.today(), min_value=date(2025, 1, 2), max_value=date.today())

if start_date >= end_date:
    st.sidebar.error("A data inicial deve ser anterior à data final.")
    st.stop()

# --- Carregar dados ---
with st.spinner("Buscando dados do Yahoo Finance..."):
    data = get_stock_data(str(start_date), str(end_date))

if not data:
    st.error("Não foi possível carregar os dados. Verifique sua conexão.")
    st.stop()

# --- Métricas resumo ---
cols = st.columns(len(data))
for col, (name, df) in zip(cols, data.items()):
    close = df["Close"].squeeze()
    ret = compute_cumulative_return(close)
    preco_atual = close.iloc[-1]
    retorno = ret.iloc[-1]
    variacao_dia = ((close.iloc[-1] / close.iloc[-2]) - 1) * 100 if len(close) > 1 else 0.0
    col.metric(
        label=name,
        value=f"R$ {preco_atual:.2f}",
        delta=f"{retorno:+.2f}% desde jan/2025",
    )

st.divider()

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Candlestick", "Volume"])

with tab1:
    st.plotly_chart(chart_closing_price(data), use_container_width=True)
    st.plotly_chart(chart_cumulative_return(data), use_container_width=True)

with tab2:
    selected = st.selectbox("Selecione a ação:", list(data.keys()))
    st.plotly_chart(chart_candlestick(data[selected], selected), use_container_width=True)

with tab3:
    st.plotly_chart(chart_volume(data), use_container_width=True)
