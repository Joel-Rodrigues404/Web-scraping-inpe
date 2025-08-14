# -*- coding: utf-8 -*-
import requests
import os

def baixar_arquivo(url, token, pasta_destino, nome_ficheiro):
    
    #Achei melhor simplificar, fiquei com medo do teu codigo
    
    headers = {"Authorization": f"Token {token}"}
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_ficheiro = os.path.join(pasta_destino, nome_ficheiro)

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Lança um erro para códigos de status HTTP ruins

        with open(caminho_ficheiro, "wb") as f:
            f.write(response.content)
        print(f"    ✓ Ficheiro salvo em: {caminho_ficheiro}")

    except requests.exceptions.RequestException as e:
        print(f"    [ERRO] Falha na requisição para {nome_ficheiro}: {e}")
