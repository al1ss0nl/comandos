import os
import requests

BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")
CHANNEL_NAME = "al1ss0nl"
PLATFORM = "kick"

try:
    botrix_url = f"https://botrix.live/api/public/leaderboard?user={CHANNEL_NAME}&platform={PLATFORM}&mode=points"
    print(f"A consultar o BotRix: {botrix_url}")
    
    # Adicionamos headers de navegador para evitar o erro 403 Forbidden
    headers_botrix = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(botrix_url, headers=headers_botrix)
    response.raise_for_status()
    botrix_data = response.json()
    print("DADOS RECEBIDOS DO BOTRIX:")
    print (botrix_data)
    
    if isinstance(botrix_data, list):
        formatted_list = []
        # Preenche com os dados reais do BotRix
        for index, entry in enumerate(botrix_data[:5], start=1):
            formatted_list.append({
                "rank": index,
                "name": entry.get("name", "Desconhecido"),
                "points": f"{entry.get('points', 0)} Pts"
            })
        
        # Se houver menos de 5 utilizadores, preenche o resto automaticamente para o site não bugar
        for index in range(len(formatted_list) + 1, 6):
            formatted_list.append({
                "rank": index,
                "name": "A aguardar...",
                "points": "- Pts"
            })
        
        url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
        headers_jsonbin = {
            "Content-Type": "application/json",
            "X-Master-Key": JSONBIN_KEY
        }
        
        update_res = requests.put(url_jsonbin, json=formatted_list, headers=headers_jsonbin)
        print(f"Resposta JSONbin (Status {update_res.status_code}): {update_res.text}")
        update_res.raise_for_status()
        print("JSONbin atualizado com sucesso!")
    else:
        print(f"Aviso: A API do BotRix devolveu dados vazios: {botrix_data}")

except Exception as e:
    print(f"Erro crítico na execução: {e}")
