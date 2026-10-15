import os
import requests

BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")
CHANNEL_NAME = "al1ss0nl"
PLATFORM = "kick"

try:
    if not JSONBIN_KEY:
        raise RuntimeError("O segredo JSONBIN_SECRET_KEY não está configurado no GitHub.")

    botrix_url = (
        f"https://botrix.live/api/public/leaderboard"
        f"?user={CHANNEL_NAME}&platform={PLATFORM}&mode=points"
    )
    print(f"A consultar o BotRix: {botrix_url}")

    headers_botrix = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    response = requests.get(botrix_url, headers=headers_botrix, timeout=30)
    print(f"Status BotRix: {response.status_code}")
    response.raise_for_status()

    botrix_data = response.json()
    print("DADOS RECEBIDOS DO BOTRIX:")
    print(botrix_data)

    if not isinstance(botrix_data, list):
        raise ValueError(
            "A resposta do BotRix não é uma lista. "
            "O JSONbin não será alterado."
        )

    if not botrix_data:
        raise ValueError(
            "O BotRix devolveu uma lista vazia ([]). "
            "O JSONbin foi preservado para não apagar o ranking existente."
        )

    formatted_list = []
    for index, entry in enumerate(botrix_data[:5], start=1):
        formatted_list.append({
            "rank": index,
            "name": entry.get("name", "Desconhecido"),
            "points": f"{entry.get('points', 0)} Pts",
            "platform": PLATFORM,
        })

    for index in range(len(formatted_list) + 1, 6):
        formatted_list.append({
            "rank": index,
            "name": "A aguardar...",
            "points": "- Pts",
        })

    url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    headers_jsonbin = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY,
    }

    update_res = requests.put(
        url_jsonbin,
        json=formatted_list,
        headers=headers_jsonbin,
        timeout=30,
    )
    print(f"Resposta JSONbin (Status {update_res.status_code}): {update_res.text}")
    update_res.raise_for_status()
    print("JSONbin atualizado com sucesso!")

except Exception as e:
    print(f"Erro crítico na execução: {e}")
    raise
