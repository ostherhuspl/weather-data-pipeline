# transform_weather.py
# Transforma os dados brutos JSON em CSV limpo
# Transforms raw weather JSON data into clean CSV format

import os
import json
import pandas as pd
from datetime import datetime
import pytz

data_dir = "data"
json_files = sorted([f for f in os.listdir(data_dir) if f.startswith("raw_weather") and f.endswith(".json")])

if not json_files:
    print("❌ Nenhum arquivo encontrado. / No files found.")
    exit()

latest_file = os.path.join(data_dir, json_files[-1])

# Define timezone da cidade
warsaw_tz = pytz.timezone('Europe/Warsaw')
now_warsaw = datetime.now(warsaw_tz).strftime("%Y-%m-%d %H:%M:%S")

with open(latest_file, "r", encoding="utf-8") as f:
    raw = json.load(f)

entry = {
    "city": raw["name"],
    "datetime": now_warsaw,  # Horário local de Warsaw!
    "temperature": raw["main"]["temp"],
    "feels_like": raw["main"]["feels_like"],
    "humidity": raw["main"]["humidity"],
    "wind_speed": raw["wind"]["speed"],
    "description": raw["weather"][0]["description"]
}

df = pd.DataFrame([entry])

csv_path = os.path.join(data_dir, "clean_weather.csv")

# Append new data without overwriting
if os.path.exists(csv_path):
    df.to_csv(csv_path, mode='a', header=False, index=False)
else:
    df.to_csv(csv_path, index=False)

print("✔ Dados limpos adicionados ao clean_weather.csv / Clean data appended.")
