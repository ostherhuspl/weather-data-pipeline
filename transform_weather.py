# transform_weather.py
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

# Protege para não sobrescrever arquivo em caso de erro na API
if "main" not in raw or "name" not in raw or "wind" not in raw or "weather" not in raw:
    print("❌ JSON recebido não tem os campos esperados. Veja abaixo:")
    print(json.dumps(raw, indent=2, ensure_ascii=False))
    exit(1)

entry = {
    "city": raw["name"],
    "datetime": now_warsaw,  # Horário local de Warsaw!
    "temperature": raw["main"]["temp"],
    "feels_like": raw["main"]["feels_like"],
    "humidity": raw["main"]["humidity"],
    "wind_speed": raw["wind"]["speed"],
    "description": raw["weather"][0]["description"]
}

csv_path = os.path.join(data_dir, "clean_weather.csv")

# Garantir que não duplica por erro: só append se não for o mesmo timestamp da última linha
if os.path.exists(csv_path):
    df_existing = pd.read_csv(csv_path)
    # Se já tem uma linha igual (mesmo datetime), não duplica
    if not (df_existing['datetime'].astype(str) == entry["datetime"]).any():
        df_new = pd.DataFrame([entry])
        df_new.to_csv(csv_path, mode='a', header=False, index=False)
else:
    df_new = pd.DataFrame([entry])
    df_new.to_csv(csv_path, index=False)

print("✔ Dados limpos adicionados ao clean_weather.csv / Clean data appended.")
