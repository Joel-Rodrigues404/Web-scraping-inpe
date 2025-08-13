import re
import requests
import os
import json


def baixar_arquivo(arquivo_json, variavel, token, pasta_destino="downloads", nome_arquivo=""):
    with open(arquivo_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    comando_curl = dados[variavel]
    print(f"para > {variavel}: {comando_curl}")

    url_match = re.search(r"(https?://\S+)", comando_curl)
    if not url_match:
        raise ValueError("Não foi possível encontrar a URL no texto")
    url = url_match.group(1)

    url_mod = re.sub(r"(?i)\bjson\b", "CSV", url)

    headers = {"Authorization": "Token " + token}

    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    response = requests.get(url_mod, headers=headers)

    if response.status_code == 200:
        with open(caminho_arquivo, "wb") as f:
            f.write(response.content)
        print(f"Arquivo salvo em: {caminho_arquivo}")
    else:
        try:
            with open("erros.json", "r", encoding="utf-8") as f:
                erros = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            erros = {}

        erros[variavel] = url

        with open("erros.json", "w", encoding="utf-8") as f:
            json.dump(erros, f, indent=4, ensure_ascii=False)
