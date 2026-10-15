import os
import requests

# Configurações
CHANNEL = "al1ss0nl"
PLATFORM = "kick"
BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")

try:
    # SIMULAÇÃO TEMPORÁRIA (para testar se o site atualiza)
    leaderboard_list = [
        {"rank": 1, "name": "Ekkoxd", "points": "1.000 Pts"},
        {"rank": 2, "name": "Membro 2", "points": "500 Pts"}
    ]

    # 2. Enviar os dados atualizados para o JSONbin.io
    url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY
    }
    
    update_res = requests.put(url_jsonbin, json=leaderboard_list, headers=headers)
    if update_res.status_code == 200:
        print("JSONbin atualizado com sucesso com os dados de teste!")
    else:
        print(f"Erro ao atualizar JSONbin: {update_res.text}")

except Exception as e:
    print(f"Ocorreu um erro durante a atualização: {e}")
