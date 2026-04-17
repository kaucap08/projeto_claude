import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data import compute_cumulative_return

COLORS = {
    "Petrobras (PETR4)": "#0066CC",
    "Itaú (ITUB4)": "#FF6600",
    "Vale (VALE3)": "#009933",
}


def chart_closing_price(data: dict) -> go.Figure:
    fig = go.Figure()
    for name, df in data.items():
        close = df["Close"].squeeze()
        fig.add_trace(go.Scatter(
            x=close.index,
            y=close.values,
            name=name,
            line=dict(color=COLORS[name], width=2),
        ))
    fig.update_layout(
        title="Preço de Fechamento (R$)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_dark",
    )
    return fig


def chart_cumulative_return(data: dict) -> go.Figure:
    fig = go.Figure()
    for name, df in data.items():
        close = df["Close"].squeeze()
        ret = compute_cumulative_return(close)
        fig.add_trace(go.Scatter(
            x=ret.index,
            y=ret.values,
            name=name,
            line=dict(color=COLORS[name], width=2),
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Retorno Acumulado em 2025 (%)",
        xaxis_title="Data",
        yaxis_title="Retorno (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_dark",
    )
    return fig


def chart_candlestick(df: pd.DataFrame, name: str) -> go.Figure:
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"].squeeze(),
        high=df["High"].squeeze(),
        low=df["Low"].squeeze(),
        close=df["Close"].squeeze(),
        increasing_line_color="#00CC44",
        decreasing_line_color="#FF3333",
        name=name,
    )])
    fig.update_layout(
        title=f"Candlestick — {name}",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )
    return fig


def chart_volume(data: dict) -> go.Figure:
    fig = go.Figure()
    for name, df in data.items():
        volume = df["Volume"].squeeze()
        fig.add_trace(go.Bar(
            x=volume.index,
            y=volume.values,
            name=name,
            marker_color=COLORS[name],
            opacity=0.7,
        ))
    fig.update_layout(
        title="Volume Negociado Diário",
        xaxis_title="Data",
        yaxis_title="Volume",
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_dark",
    )
    return fig
