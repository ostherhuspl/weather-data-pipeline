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

# ==== CHECKBOXES E GRÁFICOS ====
col1, col2, col3 = st.columns(3)
with col1:
    show_temp = st.checkbox("🌡️ Temperatura | Temperature", value=True)
    show_feels = st.checkbox("🥵 Sensação Térmica | Thermal Sensation", value=True)
with col2:
    show_humid = st.checkbox("💧 Umidade | Humidity", value=True)
    show_wind = st.checkbox("🌬️ Vento | Wind", value=True)
with col3:
    show_hist = st.checkbox("📊 Histograma Temp. | Time histogram", value=True)
    show_temp_humid = st.checkbox("📈 Temp x Umidade | Temp x Hum", value=True)
    show_heatmap = st.checkbox("🔥 Mapa de Calor (Heatmap)", value=True)

if show_temp:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["datetime"], y=df_filtered["temperature"],
        mode="lines+markers", name="Temperatura (°C)", marker=dict(color='red')
    ))
    if len(df_filtered) > 0:
        idx_max = df_filtered["temperature"].idxmax()
        fig.add_trace(go.Scatter(
            x=[df_filtered["datetime"].loc[idx_max]], y=[df_filtered["temperature"].max()],
            mode="markers+text",
            marker=dict(color='red', size=14, symbol="star"),
            text=[f"Máx: {df_filtered['temperature'].max():.1f}°C"], textposition="top center",
            showlegend=False
        ))
        idx_min = df_filtered["temperature"].idxmin()
        fig.add_trace(go.Scatter(
            x=[df_filtered["datetime"].loc[idx_min]], y=[df_filtered["temperature"].min()],
            mode="markers+text",
            marker=dict(color='blue', size=14, symbol="star"),
            text=[f"Mín: {df_filtered['temperature'].min():.1f}°C"], textposition="bottom center",
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[df_filtered["datetime"].iloc[-1]], y=[df_filtered["temperature"].iloc[-1]],
            mode="markers+text",
            marker=dict(color='orange', size=16, symbol="circle"),
            text=[f"Atual: {df_filtered['temperature'].iloc[-1]:.1f}°C"], textposition="middle right",
            showlegend=False
        ))
    fig.update_layout(
        title="🌡️ Temperatura (°C) / Temperature (°C)",
        xaxis_title="Data/Hora | Date/Time", yaxis_title="°C",
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
        xaxis_title="Data/Hora | Date/Time", yaxis_title="°C",
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
        xaxis_title="Data/Hora | Date/Time", yaxis_title="%",
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
        xaxis_title="Data/Hora | Date/Time", yaxis_title="m/s",
        template="plotly_white", hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# =========== NOVO HISTOGRAMA AVANÇADO ===========
if show_hist:
    fig = go.Figure()

    # Temperatura real
    fig.add_trace(go.Histogram(
        x=df_filtered["temperature"],
        name="Temperatura (°C)",
        nbinsx=18,
        marker=dict(
            color="rgba(255,100,20,0.62)",
            line=dict(color="darkred", width=2)
        ),
        opacity=0.82,
        xbins=dict(size=1.2),
        hovertemplate="Temp: %{x:.1f}°C<br>Freq: %{y}"
    ))

    # Sensação térmica (sobreposição)
    if "feels_like" in df_filtered.columns:
        fig.add_trace(go.Histogram(
            x=df_filtered["feels_like"],
            name="Sensação Térmica (°C)",
            nbinsx=18,
            marker=dict(
                color="rgba(80,90,255,0.44)",
                line=dict(color="midnightblue", width=2)
            ),
            opacity=0.65,
            xbins=dict(size=1.2),
            hovertemplate="Feels Like: %{x:.1f}°C<br>Freq: %{y}"
        ))

    # Linhas de média e mediana (temperatura)
    mean_temp = df_filtered["temperature"].mean()
    median_temp = df_filtered["temperature"].median()
    fig.add_vline(
        x=mean_temp, line_width=2, line_dash="dash", line_color="red",
        annotation_text=f"Média: {mean_temp:.1f}°C", annotation_position="top right"
    )
    fig.add_vline(
        x=median_temp, line_width=2, line_dash="dot", line_color="orange",
        annotation_text=f"Mediana: {median_temp:.1f}°C", annotation_position="top left"
    )

    fig.update_layout(
        title="📊 <b>Histograma de Temperaturas / Temperature Histogram</b>",
        xaxis_title="°C",
        yaxis_title="Frequência / Frequency",
        barmode="overlay",  # Sobrepor barras
        bargap=0.17,
        bargroupgap=0.09,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        font=dict(size=15)
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
        xaxis_title="Data/Hora | Date/Time", yaxis_title="Valor / Value",
        template="plotly_white", hovermode='x unified'
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
