
import os
import requests

# Configuração dos canais
BIN_ID = "6ad0da85ac6210605a33fee6"
JSONBIN_KEY = os.environ.get("JSONBIN_SECRET_KEY")

CHANNELS = {
    "kick": "al1ss0nl",
    "twitch": "al1ss0nl",
}

API_BASE = "https://botrix.live/api/public/leaderboard"


def buscar_ranking(plataforma, canal):
    url = f"{API_BASE}?user={canal}&platform={plataforma}&mode=points"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    print(f"Consultando BotRix ({plataforma}): {url}")

    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status BotRix ({plataforma}): {response.status_code}")
    response.raise_for_status()

    dados = response.json()

    if not isinstance(dados, list):
        raise ValueError(
            f"Resposta inválida do BotRix para {plataforma}."
        )

    print(f"Jogadores recebidos ({plataforma}): {len(dados)}")

    return dados


def main():
    if not JSONBIN_KEY:
        raise RuntimeError(
            "JSONBIN_SECRET_KEY não está configurado no GitHub."
        )

    todos = []

    # As duas plataformas precisam responder corretamente.
    # Assim, uma falha não apaga parte do ranking atual.
    for plataforma, canal in CHANNELS.items():
        entradas = buscar_ranking(plataforma, canal)

        for entrada in entradas:
            if not isinstance(entrada, dict):
                raise ValueError(
                    f"Entrada inválida no ranking de {plataforma}."
                )

            nome = str(entrada.get("name", "")).strip()

            if not nome:
                continue

            try:
                pontos = int(entrada.get("points", 0))
            except (TypeError, ValueError):
                pontos = 0

            todos.append({
                "name": nome,
                "points_value": pontos,
                "points": f"{pontos} Pts",
                "platform": plataforma,
            })

    if not todos:
        raise RuntimeError(
            "Nenhum jogador encontrado. JSONbin não foi alterado."
        )

    # Top 5 global, mantendo cada plataforma separada.
    todos.sort(
        key=lambda jogador: jogador["points_value"],
        reverse=True,
    )

    ranking = []

    for posicao, jogador in enumerate(todos[:5], start=1):
        ranking.append({
            "rank": posicao,
            "name": jogador["name"],
            "points": jogador["points"],
            "platform": jogador["platform"],
        })

    # Completa posições vazias sem inventar jogadores.
    for posicao in range(len(ranking) + 1, 6):
        ranking.append({
            "rank": posicao,
            "name": "A aguardar...",
            "points": "- Pts",
            "platform": None,
        })

    print("TOP 5 GLOBAL:")
    for jogador in ranking:
        print(jogador)

    # Só grava depois de validar as duas consultas.
    url_jsonbin = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

    headers_jsonbin = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY,
    }

    resposta = requests.put(
        url_jsonbin,
        json=ranking,
        headers=headers_jsonbin,
        timeout=30,
    )

    print(
        f"Resposta JSONbin ({resposta.status_code}): "
        f"{resposta.text}"
    )
    resposta.raise_for_status()

    print("JSONbin atualizado com sucesso!")


if __name__ == "__main__":
    main()
