import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd

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

# Função para anotar máximos, mínimos e último ponto
def annotate_extremes(ax, x, y, unidade=""):
    # Máximo
    idx_max = y.idxmax()
    ax.annotate(f'Máx: {y[idx_max]:.1f}{unidade}',
                (x[idx_max], y[idx_max]),
                xytext=(0, 12), textcoords='offset points',
                ha='center', va='bottom', color='red',
                fontsize=9, fontweight='bold',
                arrowprops=dict(facecolor='red', shrink=0.06, width=1, headwidth=8))
    # Mínimo
    idx_min = y.idxmin()
    ax.annotate(f'Mín: {y[idx_min]:.1f}{unidade}',
                (x[idx_min], y[idx_min]),
                xytext=(0, -16), textcoords='offset points',
                ha='center', va='top', color='blue',
                fontsize=9, fontweight='bold',
                arrowprops=dict(facecolor='blue', shrink=0.06, width=1, headwidth=8))
    # Último
    idx_last = y.index[-1]
    ax.annotate(f'Atual: {y[idx_last]:.1f}{unidade}',
                (x[idx_last], y[idx_last]),
                xytext=(10, 0), textcoords='offset points',
                ha='left', va='center', color='black',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.13", fc="yellow", ec="gray", alpha=0.6))

# PRIMEIRA LINHA: Temperatura, Sensação Térmica, Umidade
row1 = st.columns(3)
with row1[0]:
    st.markdown('<span style="font-size:15px;font-weight:600">🌡️ Temperatura (°C) / Temperature (°C)</span>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df["datetime"], df["temperature"], color="orangered", marker="o", linewidth=2.5)
    ax.fill_between(df["datetime"], df["temperature"], color="orange", alpha=0.2)
    ax.set_title("Temperatura / Temperature", fontsize=10, fontweight='bold')
    ax.set_ylabel("°C")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.grid(alpha=0.3, linestyle="--")
    annotate_extremes(ax, df["datetime"], df["temperature"], unidade="°C")
    plt.tight_layout()
    st.pyplot(fig)

with row1[1]:
    st.markdown('<span style="font-size:15px;font-weight:600">🥵 Sensação Térmica (°C) / Feels Like (°C)</span>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df["datetime"], df["feels_like"], color="#7e3ff2", marker="s", linewidth=2)
    ax.fill_between(df["datetime"], df["feels_like"], color="#d1b3ff", alpha=0.4)
    ax.set_title("Sensação Térmica / Feels Like", fontsize=10, fontweight='bold')
    ax.set_ylabel("°C")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.grid(alpha=0.25, linestyle="--")
    annotate_extremes(ax, df["datetime"], df["feels_like"], unidade="°C")
    plt.tight_layout()
    st.pyplot(fig)

with row1[2]:
    st.markdown('<span style="font-size:15px;font-weight:600">💧 Umidade (%) / Humidity (%)</span>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df["datetime"], df["humidity"], color="#297FFF", marker="o", linewidth=2, linestyle='dotted')
    ax.set_title("Umidade / Humidity", fontsize=10, fontweight='bold')
    ax.set_ylabel("%")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.grid(axis="y", alpha=0.18)
    annotate_extremes(ax, df["datetime"], df["humidity"], unidade="%")
    plt.tight_layout()
    st.pyplot(fig)

# SEGUNDA LINHA: Velocidade do Vento, Histograma Temperatura, Umidade x Temperatura (tons de vermelho para temperatura)
row2 = st.columns(3)
with row2[0]:
    st.markdown('<span style="font-size:15px;font-weight:600">🌬️ Velocidade do Vento (m/s) / Wind Speed (m/s)</span>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df["datetime"], df["wind_speed"], color="#27ae60", linewidth=2)
    ax.fill_between(df["datetime"], df["wind_speed"], color="#2ecc40", alpha=0.28)
    ax.set_title("Vento / Wind", fontsize=10, fontweight='bold')
    ax.set_ylabel("m/s")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.grid(alpha=0.18)
    annotate_extremes(ax, df["datetime"], df["wind_speed"], unidade=" m/s")
    plt.tight_layout()
    st.pyplot(fig)

with row2[1]:
    st.markdown('<span style="font-size:15px;font-weight:600">📊 Histograma Temperatura / Temp Histogram</span>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.hist(df["temperature"], bins=12, color="tomato", edgecolor="darkred", alpha=0.7)
    ax.set_title("Histograma Temperatura / Histogram Temperature", fontsize=10, fontweight='bold')
    ax.set_xlabel("°C")
    ax.set_ylabel("Frequência / Frequency")
    plt.tight_layout()
    st.pyplot(fig)

with row2[2]:
    st.markdown('<span style="font-size:15px;font-weight:600">📈 Umidade x Temperatura / Humidity x Temperature</span>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3))
    # Umidade: linha azul clara, Temperatura: linha vermelha "dry bulb"
    ax.plot(df["datetime"], df["humidity"], label="Umidade (%)", color="#297FFF", marker="o", linestyle='dotted', linewidth=2)
    ax.plot(df["datetime"], df["temperature"], label="Temp Bulbo Seco (°C)", color="#ff4d4d", marker="s", linewidth=2.5)
    ax.set_title("Umidade x Temperatura", fontsize=10, fontweight='bold')
    ax.set_ylabel("Valor / Value")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.grid(alpha=0.20)
    ax.legend()
    # Adiciona extrema da temperatura
    annotate_extremes(ax, df["datetime"], df["temperature"], unidade="°C")
    plt.tight_layout()
    st.pyplot(fig)
