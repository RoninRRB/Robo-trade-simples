import ccxt
import streamlit as st
import pandas as pd
import time

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="Robô de Trade", layout="centered")

st.title("🤖 Robô de Trade Simples")
st.markdown("Monitoramento de mercado em tempo real")

# =========================
# SIDEBAR (CONFIGURAÇÕES)
# =========================
st.sidebar.header("⚙️ Configurações")

symbol = st.sidebar.selectbox("Par de moedas", ["BTC/USDT", "ETH/USDT"])

preco_compra = st.sidebar.number_input("Preço para COMPRAR", value=60000)
preco_venda = st.sidebar.number_input("Preço para VENDER", value=65000)

intervalo = st.sidebar.slider("Atualização (segundos)", 5, 60, 10)

# =========================
# CONEXÃO COM BINANCE
# =========================
exchange = ccxt.binance()

# =========================
# FUNÇÃO PARA PEGAR DADOS
# =========================
def pegar_preco():
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

# =========================
# LOOP CONTROLADO
# =========================
placeholder = st.empty()

while True:
    try:
        preco = pegar_preco()

        with placeholder.container():

            st.subheader(f"📊 {symbol}")
            st.metric(label="Preço Atual", value=f"{preco}")

            # =========================
            # LÓGICA DE DECISÃO
            # =========================
            if preco < preco_compra:
                st.success("🟢 SINAL: COMPRAR")

            elif preco > preco_venda:
                st.error("🔴 SINAL: VENDER")

            else:
                st.warning("🟡 SINAL: AGUARDAR")

            # =========================
            # HISTÓRICO SIMPLES
            # =========================
            if "historico" not in st.session_state:
                st.session_state.historico = []

            st.session_state.historico.append(preco)

            df = pd.DataFrame(st.session_state.historico, columns=["Preço"])

            st.line_chart(df)

        time.sleep(intervalo)

    except Exception as e:
        st.error(f"Erro: {e}")
        time.sleep(intervalo)