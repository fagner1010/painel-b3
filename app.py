
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Oportunidade B3")

st.markdown("<h1 style='text-align: center; color: navy;'>Painel de Oportunidades da B3</h1>", unsafe_allow_html=True)

tickers = {
    "IBOV": "^BVSP",
    "Dólar Futuro": "BRL=X",
    "Mini Índice": "WIN=F",
    "Mini Dólar": "WDON23.SA"
}

col1, col2, col3, col4 = st.columns(4)
for i, (label, symbol) in enumerate(tickers.items()):
    data = yf.Ticker(symbol).history(period="1d", interval="5m")
    last_price = data["Close"].iloc[-1]
    delta = last_price - data["Close"].iloc[-2]
    with [col1, col2, col3, col4][i]:
        st.metric(label, f"R$ {last_price:.2f}", f"{delta:.2f}")

st.markdown("---")

st.subheader("Ações em destaque")

acoes = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "WEGE3.SA", "MGLU3.SA"]
precos = {}
for acao in acoes:
    dados = yf.Ticker(acao).history(period="2d")
    if not dados.empty:
        preco_atual = dados["Close"].iloc[-1]
        preco_anterior = dados["Close"].iloc[-2]
        variacao = (preco_atual - preco_anterior) / preco_anterior * 100
        precos[acao] = round(variacao, 2)

altas = sorted(precos.items(), key=lambda x: x[1], reverse=True)[:3]
baixas = sorted(precos.items(), key=lambda x: x[1])[:3]

col1, col2 = st.columns(2)
with col1:
    st.success("Maiores altas")
    for acao, var in altas:
        st.write(f"**{acao}**: 🔼 {var}%")

with col2:
    st.error("Maiores quedas")
    for acao, var in baixas:
        st.write(f"**{acao}**: 🔽 {var}%")
