import json
import urllib.request
import os

# Podes futuramente adaptar este script para ler da API ou raspar a página do BotRix
# Por agora, vamos garantir que o ficheiro JSON é gerado automaticamente pela action:

leaderboard_data = [
    {"rank": 1, "name": "Alisson (Exemplo)", "points": "18.900 Pts"},
    {"rank": 2, "name": "Membro 2", "points": "12.450 Pts"},
    {"rank": 3, "name": "Membro 3", "points": "9.800 Pts"},
    {"rank": 4, "name": "Membro 4", "points": "7.500 Pts"},
    {"rank": 5, "name": "Membro 5", "points": "6.200 Pts"}
]

with open('leaderboard.json', 'w', encoding='utf-8') as f:
    json.dump(leaderboard_data, f, ensure_ascii=False, indent=2)

print("Leaderboard atualizado com sucesso!")