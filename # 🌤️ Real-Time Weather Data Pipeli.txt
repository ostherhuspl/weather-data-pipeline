# 🌤️ Real-Time Weather Data Pipeline with Streamlit

This project demonstrates a **complete mini data engineering pipeline**, from real-time data ingestion to a live dashboard. It uses open APIs to simulate sensor data, processes it using Python, and visualizes it interactively with Streamlit.

---

## 🚀 Overview

| Step            | Tool/Language            | Description                           |
| --------------- | ------------------------ | ------------------------------------- |
| Data Collection | Python + OpenWeather API | Pulls real-time weather data via HTTP |
| Storage         | JSON / CSV               | Saves raw and clean data files        |
| Transformation  | pandas                   | Normalizes and extracts fields        |
| Visualization   | Streamlit                | Interactive dashboard and metrics     |

---

## 📦 File Structure

```bash
weather_pipeline/
├── weather_collector.py         # Collects and stores weather JSON data
├── transform_weather.py         # Transforms and cleans the data to CSV
├── dashboard.py                 # Streamlit app for live dashboard
├── data/
│   ├── raw_weather_*.json       # Raw weather data from API
│   └── clean_weather.csv        # Cleaned weather log for analysis
└── weather_snapshot_bars.png    # Snapshot of chart output
```

---

## 🧪 How to Run It

### Step 1: Collect Data

```bash
python weather_collector.py
```

This pulls the current weather from OpenWeatherMap and saves it in `/data/raw_weather_<timestamp>.json`

### Step 2: Transform the Data

```bash
python transform_weather.py
```

Extracts fields like temperature, humidity, wind, and stores in `clean_weather.csv`

### Step 3: Run the Dashboard

```bash
streamlit run dashboard.py
```

Your browser will open a live dashboard with real-time metrics and graphs.

---

## 📊 Preview

---

## 🌍 Technology Stack

* Python 3.11+
* requests
* pandas
* matplotlib
* Streamlit

---

## 💡 Why this project?

This simulates IoT-like sensor collection using public APIs — ideal for:

* Practicing real-time ingestion and processing
* Creating dashboards for reporting
* Simulating embedded devices with zero cost

---

## 📌 Author

**Daniel Hernandes Gomes**
🔗 [LinkedIn](https://www.linkedin.com/in/daniel-hernandes-gomes-9b87b77a/)

Feel free to fork or reuse for your own pipelines!

---

*This project was built as part of my transition into Data Engineering and showcases skills in data ingestion, transformation, and visualization.*
