import os
import requests

BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")
CHANNEL_NAME = "al1ss0nl"
PLATFORM = "kick"

try:
    botrix_url = f"https://botrix.live/api/public/leaderboard?user={CHANNEL_NAME}&platform={PLATFORM}&mode=points"
    print(f"A consultar o BotRix: {botrix_url}")
    
    response = requests.get(botrix_url)
    response.raise_for_status()
    botrix_data = response.json()
    
    if isinstance(botrix_data, list) and len(botrix_data) > 0:
        formatted_list = []
        for index, entry in enumerate(botrix_data[:5], start=1):
            formatted_list.append({
                "rank": index,
                "name": entry.get("name", "Desconhecido"),
                "points": f"{entry.get('points', 0)} Pts"
            })
        
        url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": JSONBIN_KEY
        }
        
        update_res = requests.put(url_jsonbin, json=formatted_list, headers=headers)
        print(f"Resposta JSONbin (Status {update_res.status_code}): {update_res.text}")
        update_res.raise_for_status()
        print("JSONbin atualizado com sucesso!")
    else:
        print(f"Aviso: A API do BotRix devolveu dados inválidos ou vazios: {botrix_data}")

except Exception as e:
    print(f"Erro crítico na execução: {e}")
