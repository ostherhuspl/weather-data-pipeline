
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configurações da página / Page settings
st.set_page_config(layout="wide", page_title="Live Weather Dashboard")

# Atualização automática a cada 60 segundos / Auto-refresh every 60 seconds
st_autorefresh(interval=15000, key="refresh")

# Título do app / App title
st.title("🌤️ Real-Time Weather Dashboard")
st.caption(
    "Este painel atualiza automaticamente com base nos dados mais recentes coletados (pode haver um atraso de alguns minutos dependendo da fila do GitHub Actions). / "
    "This dashboard auto-refreshes based on the latest collected data (there may be a delay of a few minutes depending on GitHub Actions scheduling)."
)

# Carrega os dados limpos / Load cleaned weather data
df = pd.read_csv("data/clean_weather.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

# Exibe a última atualização / Show last data update
latest = df.iloc[-1]
st.markdown(f"**📅 Última atualização / Last Update:** {latest['datetime']} — Cidade / City: {latest['city']}")

# Layout com 3 colunas para os gráficos / Three-column layout for charts
col1, col2, col3 = st.columns(3)

# 🌡️ Temperatura / Temperature chart
# Temperatura: Linha suave + área
with col1:
    st.subheader("🌡️ Temperatura (°C)")
    fig, ax = plt.subplots(figsize=(4, 3))  # tamanho pequeno
    ax.plot(df["datetime"], df["temperature"], color="orangered", marker="o", linewidth=2.5, label="Temperatura")
    ax.fill_between(df["datetime"], df["temperature"], color="orange", alpha=0.2)
    ax.set_title("Temperatura", fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()
    st.pyplot(fig)

# 💧 Umidade / Humidity chart
# Umidade: Barras com sombra
with col2:
    st.subheader("💧 Umidade (%)")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(df["datetime"], df["humidity"], color="#0099FF", edgecolor="#003366", alpha=0.8)
    ax.set_title("Umidade", fontsize=12, fontweight='bold')
    ax.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig)
# 🌬️ Velocidade do Vento / Wind Speed chart
# Vento: Área transparente + linha
with col3:
    st.subheader("🌬️ Velocidade do Vento (m/s)")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(df["datetime"], df["wind_speed"], color="#27ae60", linewidth=2, label="Vento")
    ax.fill_between(df["datetime"], df["wind_speed"], color="#2ecc40", alpha=0.25)
    ax.set_title("Vento", fontsize=12, fontweight='bold')
    ax.grid(alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig)
