
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
with col1:
    st.subheader("🌡️ Temperatura (°C) / Temperature (°C)")
    fig, ax = plt.subplots()
    ax.plot(df["datetime"], df["temperature"], color="tab:red", marker="o")
    ax.set_ylabel("°C")
    ax.set_xlabel("Hora / Time")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

# 💧 Umidade / Humidity chart
with col2:
    st.subheader("💧 Umidade (%) / Humidity (%)")
    fig, ax = plt.subplots()
    ax.plot(df["datetime"], df["humidity"], color="tab:blue", marker="o")
    ax.set_ylabel("%")
    ax.set_xlabel("Hora / Time")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

# 🌬️ Velocidade do Vento / Wind Speed chart
with col3:
    st.subheader("🌬️ Vel.Vento (m/s) / Wind Speed (m/s)")
    fig, ax = plt.subplots()
    ax.plot(df["datetime"], df["wind_speed"], color="tab:green", marker="o")
    ax.set_ylabel("m/s")
    ax.set_xlabel("Hora / Time")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
