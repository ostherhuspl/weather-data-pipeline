import requests
import json
import os
from datetime import datetime

# Pega a chave da API do ambiente (GitHub Actions vai passar isso) / Gets API key from environment
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("API key is missing! Set the OPENWEATHER_API_KEY environment variable.")

CITY = "Warsaw"  # Você pode mudar para São Paulo, Lisbon, etc.

# URL da API | API URL
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Faz a requisição | Requisition
response = requests.get(url)
data = response.json()

# Garante que a pasta de dados exista | Will make sure the folder exists
os.makedirs("data", exist_ok=True)

# Nome do arquivo com timestamp | file name with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data/raw_weather_{timestamp}.json"

# Salva o JSON com indentação | will save the JSON file
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"✔ Dados salvos com sucesso em {filename}")
