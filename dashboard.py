import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd

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
    "cloud":"https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNm00MTdsbnkxbnMydTY2YWp3M3htZjlkczRkYWhyMWF5empneTc5bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lOkbL3MJnEtHi/giphy.gif",
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

# Umidade: Barras com sombra
with col2:
    st.subheader("💧 Umidade (%)")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(df["datetime"], df["humidity"], color="#0099FF", edgecolor="#003366", alpha=0.8)
    ax.set_title("Umidade", fontsize=12, fontweight='bold')
    ax.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig)

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

