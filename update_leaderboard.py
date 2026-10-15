import os
import requests

BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")
CHANNEL_NAME = "al1ss0nl"
PLATFORM = "kick"

if not JSONBIN_KEY:
    print("ERRO: A variável JSONBIN_SECRET_KEY não está definida nas Secrets do GitHub!")
    exit(1)

try:
    # 1. Obter dados do BotRix
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
        
        # 2. Enviar para o JSONbin.io
        url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": JSONBIN_KEY
        }
        
        update_res = requests.put(url_jsonbin, json=formatted_list, headers=headers)
        if update_res.status_code == 200:
            print("JSONbin atualizado com sucesso com os dados do BotRix!")
        else:
            print(f"Erro ao atualizar o JSONbin: {update_res.status_code} - {update_res.text}")
    else:
        print("A API do BotRix devolveu uma lista vazia ou o canal está offline.")

except Exception as e:
    print(f"Ocorreu um erro crítico: {e}")
