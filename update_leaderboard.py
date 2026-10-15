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
    print(f"Dados recebidos ({plataforma}): {dados}")

    if not isinstance(dados, list):
        raise ValueError(
            f"A resposta do BotRix para {plataforma} não é uma lista. "
            "O JSONbin não será alterado."
        )

    return dados


def main():
    if not JSONBIN_KEY:
        raise RuntimeError(
            "O segredo JSONBIN_SECRET_KEY não está configurado no GitHub."
        )

    todos = []
    erros = []

    # Consulta as duas plataformas separadamente para que uma falha não
    # impeça o uso dos dados válidos da outra.
    for plataforma, canal in CHANNELS.items():
        try:
            entradas = buscar_ranking(plataforma, canal)
            for entrada in entradas:
                try:
                    pontos = int(entrada.get("points", 0))
                except (TypeError, ValueError):
                    pontos = 0

                todos.append({
                    "name": str(entrada.get("name", "Desconhecido")),
                    "points_value": pontos,
                    "points": f"{pontos} Pts",
                    "platform": plataforma,
                })
        except Exception as erro:
            erros.append(f"{plataforma}: {erro}")
            print(f"ERRO ao consultar {plataforma}: {erro}")

    if not todos:
        raise RuntimeError(
            "Nenhum jogador foi recebido de Kick ou Twitch. "
            "O JSONbin foi preservado para não apagar o ranking atual. "
            + " | ".join(erros)
        )

    # Ordena os pontos de forma decrescente; em caso de empate, mantém
    # uma ordenação estável com base na ordem de consulta (Kick, depois Twitch).
    todos.sort(key=lambda jogador: jogador["points_value"], reverse=True)

    ranking = []
    for posicao, jogador in enumerate(todos[:5], start=1):
        ranking.append({
            "rank": posicao,
            "name": jogador["name"],
            "points": jogador["points"],
            "platform": jogador["platform"],
        })

    for posicao in range(len(ranking) + 1, 6):
        ranking.append({
            "rank": posicao,
            "name": "A aguardar...",
            "points": "- Pts",
        })

    print("TOP 5 UNIFICADO:")
    print(ranking)

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
    print(f"Resposta JSONbin (Status {resposta.status_code}): {resposta.text}")
    resposta.raise_for_status()
    print("JSONbin atualizado com sucesso!")


if __name__ == "__main__":
    main()
