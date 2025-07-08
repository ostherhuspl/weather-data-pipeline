import requests
import json
import os
from datetime import datetime

# Substitua pela sua própria chave
API_KEY = ${{ secrets.OPENWEATHER_API_KEY }}
CITY = "Warsaw"  # Você pode mudar para São Paulo, Lisbon, etc.

# URL da API
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Faz a requisição
response = requests.get(url)
data = response.json()

# Garante que a pasta de dados exista
os.makedirs("data", exist_ok=True)

# Nome do arquivo com timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data/raw_weather_{timestamp}.json"

# Salva o JSON com indentação
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"✔ Dados salvos com sucesso em {filename}")
