###### Dashboard - Importing
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np

st.set_page_config(layout="wide")
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60000, key="refresh")  # Atualiza a cada 60 segundos

# Carrega os dados limpos
csv_url = "https://raw.githubusercontent.com/ostherhuspl/weather-data-pipeline-data/main/clean_weather.csv"
df = pd.read_csv(csv_url)

if "datetime" not in df.columns:
    st.error("O arquivo CSV não contém a coluna 'datetime'. Verifique o pipeline.")
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

# ==== LAYOUT: GIF (col1) / SLIDER + TABELA (col2) ====
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ☀️⛅️🌧️ Estado do céu / Sky condition")
    st.image(gif_url, caption=f"{latest['description'].capitalize()} / {latest['description'].capitalize()}")

with col2:
    if len(df) >= 2:
        min_date = pd.to_datetime(df["datetime"].min()).to_pydatetime()
        max_date = pd.to_datetime(df["datetime"].max()).to_pydatetime()
        date_range = st.slider(
            "Selecione o período / Select the period:",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD/MM/YYYY HH:mm"
        )
    else:
        st.warning("Precisa de pelo menos 2 linhas de dados para o filtro de datas.")
        date_range = (None, None)

    if date_range[0] is not None and date_range[1] is not None:
        mask = (df["datetime"] >= date_range[0]) & (df["datetime"] <= date_range[1])
        df_filtered = df.loc[mask].copy()
    else:
        df_filtered = df.copy()

    # TABELA LOGO ABAIXO DO SLIDER
    st.dataframe(
        df_filtered.sort_values("datetime", ascending=False).head(6),
        use_container_width=True
    )

# ================= GRÁFICO 1: Temperatura | Temperature =================
if st.checkbox("🌡️ Temperatura | Temperature", value=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["temperature"],
        mode="lines+markers",
        name="Temperatura (°C) | Temperature (°C)",
        marker=dict(color="#FF5733", size=6, symbol="circle"),
        line=dict(width=3)
    ))

    fig.update_layout(
        title={"text": "🌡️ Temperatura (°C) | Temperature (°C)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="°C",
        template="plotly_white",
        hovermode='x unified',
        margin=dict(t=40, b=40),
        plot_bgcolor='rgba(250,250,250,1)'
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
        marker=dict(color="#9C27B0", size=6),
        line=dict(width=3)
    ))

    fig.update_layout(
        title={"text": "🥵 Sensação Térmica (°C) | Feels Like (°C)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="°C",
        template="plotly_white",
        hovermode='x unified',
        margin=dict(t=40, b=40),
        plot_bgcolor='rgba(250,250,255,1)'
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
        marker=dict(color="#03A9F4", size=6),
        line=dict(width=3)
    ))

    fig.update_layout(
        title={"text": "💧 Umidade (%) | Humidity (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="%",
        template="plotly_white",
        hovermode='x unified',
        margin=dict(t=40, b=40),
        plot_bgcolor='rgba(240,248,255,1)'
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
        marker=dict(color="#4CAF50", size=6),
        line=dict(width=3)
    ))

    fig.update_layout(
        title={"text": "🌬️ Velocidade do Vento (m/s) | Wind Speed (m/s)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="m/s",
        template="plotly_white",
        hovermode='x unified',
        margin=dict(t=40, b=40),
        plot_bgcolor='rgba(240,255,240,1)'
    )
    st.plotly_chart(fig, use_container_width=True)

# =========== GRÁFICO DE ÍNDICE DE CONFORTO CLIMÁTICO | CLIMATE COMFORT INDEX CHART ===========
if show_hist:
    st.subheader("🧠 Índice de Conforto Climático / Climate Comfort Index")

    df_comfort = df_filtered.copy()

    if all(col in df_comfort.columns for col in ["temperature", "feels_like", "humidity"]):
        df_comfort["comfort_index"] = (
            df_comfort["feels_like"] + df_comfort["temperature"] + (100 - df_comfort["humidity"])
        ) / 3

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_comfort["datetime"],
            y=df_comfort["comfort_index"],
            marker=dict(
                color=df_comfort["comfort_index"],
                colorscale='RdYlGn',
                colorbar=dict(title="Índice")
            ),
            name="Conforto Climático"
        ))

        fig.update_layout(
            title="🧠 Índice de Conforto Climático / Climate Comfort Index (quanto mais alto, mais agradável | the higher, the more pleasant)",
            xaxis_title="Data/Hora | Date/Time",
            yaxis_title="Índice de Conforto | Comfort Index",
            template="plotly_white",
            hovermode="x unified",
            margin=dict(t=40, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Dados insuficientes para calcular o índice de conforto. / Not enough data to compute comfort index.")

# =========== GRÁFICO DE UMIDADE x TEMPERATURA | HUMIDITY x TEMPERATURE ===========
if show_temp_humid:
    st.subheader("💧📉 Relação Umidade x Temperatura com Destaques / Humidity vs Temperature with Highlights")

    fig = go.Figure()

    # --- Área sombreada representando a umidade | Shaded area for humidity ---
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"],
        y=df_filtered["humidity"],
        mode="lines",
        fill='tozeroy',
        name="Umidade (%) | Humidity (%)",
        line=dict(color="#297FFF", width=2),
        fillcolor="rgba(41,127,255,0.2)",
        hoverinfo="x+y"
    ))

    # --- Linha representando a temperatura | Line for dry-bulb temperature ---
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"],
        y=df_filtered["temperature"],
        mode="lines+markers",
        name="Temp. Bulbo Seco (°C) | Dry-Bulb Temp. (°C)",
        line=dict(color="crimson", width=3),
        marker=dict(size=6),
        hoverinfo="x+y"
    ))

    # --- Destaques para valores extremos | Highlighting max and min temps ---
    if not df_filtered.empty:
        idx_max = df_filtered["temperature"].idxmax()
        idx_min = df_filtered["temperature"].idxmin()

        fig.add_trace(go.Scatter(
            x=[df_filtered.loc[idx_max, "datetime"]],
            y=[df_filtered.loc[idx_max, "temperature"]],
            mode="markers+text",
            marker=dict(color='red', size=14, symbol="star"),
            text=[f"Máx: {df_filtered['temperature'].max():.1f}°C"],
            textposition="top center",
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[df_filtered.loc[idx_min, "datetime"]],
            y=[df_filtered.loc[idx_min, "temperature"]],
            mode="markers+text",
            marker=dict(color='blue', size=14, symbol="star"),
            text=[f"Mín: {df_filtered['temperature'].min():.1f}°C"],
            textposition="bottom center",
            showlegend=False
        ))

    fig.update_layout(
        title="💧📉 Umidade x Temperatura com Destaques de Extremos / Humidity vs Temperature with Extremes",
        xaxis_title="Data/Hora | Date/Time",
        yaxis_title="Valor | Value",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# ===== HEATMAP (MAPA DE CALOR) DE TEMPERATURA POR HORA E DIA =====
if show_heatmap:
    df_filtered["day"] = df_filtered["datetime"].dt.date
    df_filtered["hour"] = df_filtered["datetime"].dt.hour

    heatmap_data = pd.pivot_table(
        df_filtered,
        values="temperature",
        index="hour",
        columns="day",
        aggfunc=np.mean
    )

    # Cores customizadas estilo "Inferno"
    colorscale = [
        [0, "#220466"], [0.10, "#2741B7"], [0.33, "#19B7F6"], [0.50, "#B4F6FF"],
        [0.66, "#F1D302"], [0.85, "#F95D06"], [1, "#D7263D"]
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=[str(c) for c in heatmap_data.columns],
            y=heatmap_data.index,
            colorscale=colorscale,
            colorbar=dict(title="°C"),
            hovertemplate='Dia: %{x}<br>Hora: %{y}h<br>Temp: %{z:.1f}°C<extra></extra>'
        )
    )
    fig.update_layout(
        title="🔥 Mapa de Calor - Temperatura (hora x dia) / Heatmap Temperature (Hour x Day)",
        xaxis_title="Dia / Day",
        yaxis_title="Hora / Hour",
        template="plotly_white",
        margin=dict(l=40, r=30, t=60, b=30),
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig, use_container_width=True)

