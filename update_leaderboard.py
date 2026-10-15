import os
import requests

CHANNEL = "al1ss0nl"
PLATFORM = "kick"
BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")

url_botrix = f"https://botrix.live/api/public/leaderboard?user={CHANNEL}&platform={PLATFORM}&mode=points"

try:
    response = requests.get(url_botrix)
    response.raise_for_status()
    raw_data = response.json()

    leaderboard_list = []
    entries = raw_data if isinstance(raw_data, list) else raw_data.get("data", [])

    for index, user in enumerate(entries[:5], start=1):
        leaderboard_list.append({
            "rank": index,
            "name": user.get("name", "Desconhecido"),
            "points": f"{user.get('points', 0):,} Pts".replace(",", ".")
        })

    if not leaderboard_list:
        print("Aviso: Nenhum dado retornado pelo BotRix.")
        exit(0)

    url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY
    }

    update_res = requests.put(url_jsonbin, json=leaderboard_list, headers=headers)
    if update_res.status_code == 200:
        print("JSONbin atualizado com sucesso com os dados do BotRix!")
    else:
        print(f"Erro ao atualizar JSONbin: {update_res.text}")

except Exception as e:
    print(f"Ocorreu um erro durante a atualização: {e}")
