import requests
from time import sleep

TOKEN = "TOKEN"
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# Faz a requisição para pegar mensagens novas
response = requests.get(URL)
data = response.json()

print(data)  # Mostra tudo que voltou da API

# Se tiver mensagens, pega o chat_id
while True:
    if "result" in data and len(data["result"]) > 0:
        for update in data["result"]:
            chat = update["message"]["chat"]
            print("📌 Chat ID:", chat["id"])
            sleep(2)  # Pausa para evitar muitas requisições rápidas
    else:
        print("Nenhuma mensagem recebida. Envie um 'oi' para o bot no Telegram e rode de novo.")
        sleep(2)
