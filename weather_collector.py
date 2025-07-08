import requests
import json
import os
from datetime import datetime

# Substitua pela sua própria chave | Here you put your API key
API_KEY = ${{ secrets.OPENWEATHER_API_KEY }}
CITY = "Warsaw"  # Você pode mudar para São Paulo, Lisbon, etc. #You can set the cit you want. 

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
