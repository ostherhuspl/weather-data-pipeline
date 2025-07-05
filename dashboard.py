import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(layout="wide")

# Carrega os dados limpos
df = pd.read_csv("data/clean_weather.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

# Proteção para DataFrame vazio
if df.empty:
    st.warning("Nenhum dado disponível ainda. / No data available yet.")
    st.stop()

# GIFs de tempo
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
    desc = description.lower()
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

# Painel do GIF com o estado do céu
latest = df.iloc[-1]
gif_url = get_weather_gif(str(latest["description"]))
st.markdown("### ☀️⛅️🌧️ Estado do céu / Sky condition")
st.image(gif_url, caption=f"{latest['description'].capitalize()} / {latest['description'].capitalize()}")

# === INTERATIVIDADE ===
# Seletor de datas (crossfilter para todos os gráficos)
min_date, max_date = df["datetime"].min(), df["datetime"].max()
date_range = st.slider(
    "Selecione o período / Select the period:",
    min_value=min_date, max_value=max_date,
    value=(min_date, max_date),
    format="DD/MM/YYYY HH:mm"
)
mask = (df["datetime"] >= date_range[0]) & (df["datetime"] <= date_range[1])
df_filtered = df.loc[mask].copy()

st.dataframe(df_filtered, use_container_width=True)

# Checkboxes para escolher quais gráficos mostrar
col1, col2, col3 = st.columns(3)
with col1:
    show_temp = st.checkbox("🌡️ Temperatura", value=True)
    show_feels = st.checkbox("🥵 Sensação Térmica", value=True)
with col2:
    show_humid = st.checkbox("💧 Umidade", value=True)
    show_wind = st.checkbox("🌬️ Vento", value=True)
with col3:
    show_hist = st.checkbox("📊 Histograma Temp.", value=True)
    show_temp_humid = st.checkbox("📈 Temp x Umidade", value=True)

# === GRÁFICOS PLOTLY ===

if show_temp:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["temperature"],
        mode="lines+markers", name="Temperatura (°C)", marker=dict(color='red')
    ))
    # Máximo
    idx_max = df_filtered["temperature"].idxmax()
    fig.add_trace(go.Scatter(
        x=[df_filtered["datetime"].loc[idx_max]], y=[df_filtered["temperature"].max()],
        mode="markers+text",
        marker=dict(color='red', size=14, symbol="star"),
        text=[f"Máx: {df_filtered['temperature'].max():.1f}°C"], textposition="top center",
        showlegend=False
    ))
    # Mínimo
    idx_min = df_filtered["temperature"].idxmin()
    fig.add_trace(go.Scatter(
        x=[df_filtered["datetime"].loc[idx_min]], y=[df_filtered["temperature"].min()],
        mode="markers+text",
        marker=dict(color='blue', size=14, symbol="star"),
        text=[f"Mín: {df_filtered['temperature'].min():.1f}°C"], textposition="bottom center",
        showlegend=False
    ))
    # Último
    fig.add_trace(go.Scatter(
        x=[df_filtered["datetime"].iloc[-1]], y=[df_filtered["temperature"].iloc[-1]],
        mode="markers+text",
        marker=dict(color='orange', size=16, symbol="circle"),
        text=[f"Atual: {df_filtered['temperature'].iloc[-1]:.1f}°C"], textposition="middle right",
        showlegend=False
    ))
    fig.update_layout(
        title="🌡️ Temperatura (°C) / Temperature (°C)",
        xaxis_title="Data/Hora", yaxis_title="°C",
        template="plotly_white", hovermode='x unified', margin=dict(t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

if show_feels:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["feels_like"],
        mode="lines+markers", name="Feels Like (°C)", marker=dict(color='#7e3ff2')
    ))
    fig.update_layout(
        title="🥵 Sensação Térmica (°C) / Feels Like (°C)",
        xaxis_title="Data/Hora", yaxis_title="°C",
        template="plotly_white", hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

if show_humid:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["humidity"],
        mode="lines+markers", name="Umidade (%)", marker=dict(color="#297FFF")
    ))
    fig.update_layout(
        title="💧 Umidade (%) / Humidity (%)",
        xaxis_title="Data/Hora", yaxis_title="%",
        template="plotly_white", hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

if show_wind:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["wind_speed"],
        mode="lines+markers", name="Vento (m/s)", marker=dict(color="#27ae60")
    ))
    fig.update_layout(
        title="🌬️ Velocidade do Vento (m/s) / Wind Speed (m/s)",
        xaxis_title="Data/Hora", yaxis_title="m/s",
        template="plotly_white", hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

if show_hist:
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df_filtered["temperature"], nbinsx=15, name="Temperatura (°C)",
        marker=dict(color="tomato", line=dict(color="darkred", width=1.5))
    ))
    fig.update_layout(
        title="📊 Histograma Temperatura / Temp Histogram",
        xaxis_title="°C", yaxis_title="Frequência / Frequency",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

if show_temp_humid:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["humidity"],
        mode="lines+markers", name="Umidade (%)", marker=dict(color="#297FFF")
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["temperature"],
        mode="lines+markers", name="Temp Bulbo Seco (°C)", marker=dict(color="red")
    ))
    fig.update_layout(
        title="📈 Umidade x Temperatura / Humidity x Temperature",
        xaxis_title="Data/Hora", yaxis_title="Valor / Value",
        template="plotly_white", hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
