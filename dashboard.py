import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st_autorefresh(interval=60000, key="refresh")

# ======== DADOS ======== DATA
csv_url = "https://raw.githubusercontent.com/ostherhuspl/weather-data-pipeline-data/main/clean_weather.csv"
df = pd.read_csv(csv_url)

if "datetime" not in df.columns:
    st.error("O arquivo CSV não contém a coluna 'datetime'. Verifique o pipeline. / CSV file missing 'datetime' column. Check the pipeline.")
    st.stop()

df["datetime"] = pd.to_datetime(df["datetime"], errors='coerce')
df = df.dropna(subset=["datetime"])

if df.empty:
    st.warning("Nenhum dado disponível ainda. / No data available yet.")
    st.stop()

# ====== GIFs ======
weather_gifs = {
    "clear": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExajZrazN1cHh6Z3F2a3dnZG1nZmoyZXhwejZ1c2ZmdXh5Z252d3BucCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FQQNs0UIOIMsU/giphy.gif",
    "rain": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2E4Z3A2YnNneXkzZWlpamFmYXZlbmR0dHo2bWtwMjZjZXJqZXJ6bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/udU9ZCWcTGpLq/giphy.gif",
    "cloud": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNm00MTdsbnkxbnMydTY2YWp3M3htZjlkczRkYWhyMWF5empneTc5bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lOkbL3MJnEtHi/giphy.gif",
    "snow": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXJkbGhvbDdvanl4bzE5anBkcnR1azJyaHJ2eWQyN2pxZXIydnc4YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RfNLGpBdysTllfljNY/giphy.gif",
    "fog": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDU0ZWgxOGdobjJhb3BqM2FpZ3FpODV5emxuemhpazJ0ZXdlNHJncSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bfZy3DHuJUc12/giphy.gif",
    "drizzle": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmJ6a2JocHIzdnkyaWZ6ajBrNHRrd2RsdnRha2NpZmtuN2NpeXdyZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/o6ijBdTg64Vu2pyNFb/giphy.gif",
    "storm": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHAxeDF0cHg3aHd6bjB3bHcwMDcwd2Q1ejMyNmo4cWM5NWR6dWM0ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LGY967AFmrueY/giphy.gif",
}

def get_weather_gif(description):
    desc = str(description).lower()
    if "clear" in desc or "céu limpo" in desc or "sun" in desc or "ensolarado" in desc:
        return weather_gifs["clear"]
    elif "rain" in desc or "chuva" in desc:
        return weather_gifs["rain"]
    elif "cloud" in desc or "nuvem" in desc or "nublado" in desc:
        return weather_gifs["cloud"]
    elif "snow" in desc or "neve" in desc:
        return weather_gifs["snow"]
    elif "fog" in desc or "névoa" in desc or "mist" in desc:
        return weather_gifs["fog"]
    elif "drizzle" in desc or "garoa" in desc:
        return weather_gifs["drizzle"]
    elif "storm" in desc or "tempestade" in desc or "thunder" in desc:
        return weather_gifs["storm"]
    return weather_gifs["clear"]

latest = df.iloc[-1]
gif_url = get_weather_gif(str(latest["description"]))

# LAYOUT DO GIF
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### ☀️⛅️🌧️ Estado do céu / Sky condition")
    st.image(gif_url, caption=f"{latest['description'].capitalize()} / {latest['description'].capitalize()}")

with col2:
    st.write("Última atualização: / Last update:", latest["datetime"])

# ================= GRÁFICO 1: Temperatura | Temperature =================
if st.checkbox("🌡️ Temperatura | Temperature", value=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["temperature"],
        mode="lines+markers",
        name="Temperatura (°C) | Temperature (°C)",
        marker=dict(color="#FF5733"),
        line=dict(width=2)
    ))

    fig.update_layout(
        title="🌡️ Temperatura (°C) | Temperature (°C)",
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="°C",
        template="plotly_white",
        hovermode='x unified',
        margin=dict(t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= GRÁFICO 2: Sensação Térmica | Feels Like =================
if st.checkbox("🥵 Sensação Térmica | Thermal Sensation", value=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["feels_like"],
        mode="lines+markers",
        name="Sensação Térmica | Feels Like",
        marker=dict(color="#9C27B0"),
        line=dict(width=2)
    ))

    fig.update_layout(
        title="🥵 Sensação Térmica (°C) | Feels Like (°C)",
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="°C",
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= GRÁFICO 3: Umidade | Humidity =================
if st.checkbox("💧 Umidade | Humidity", value=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["humidity"],
        mode="lines+markers",
        name="Umidade | Humidity",
        marker=dict(color="#03A9F4"),
        line=dict(width=2)
    ))

    fig.update_layout(
        title="💧 Umidade (%) | Humidity (%)",
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="%",
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= GRÁFICO 4: Vento | Wind Speed =================
if st.checkbox("🌬️ Vento | Wind", value=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["wind_speed"],
        mode="lines+markers",
        name="Vento | Wind",
        marker=dict(color="#4CAF50"),
        line=dict(width=2)
    ))

    fig.update_layout(
        title="🌬️ Velocidade do Vento (m/s) | Wind Speed (m/s)",
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="m/s",
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)