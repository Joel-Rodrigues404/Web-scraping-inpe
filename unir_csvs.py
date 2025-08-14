# -*- coding: utf-8 -*-
import pandas as pd
import glob
import os
from pathlib import Path

def unir_csvs_de_uma_pasta(pasta_de_entrada, arquivo_de_saida):
    
    #nao tenho a minima ideia do que fazer aqui pra unificar direito, isso aqui é praticamente só codigo lixo de outras tentativas, me salva aí joel
    os.makedirs(os.path.dirname(arquivo_de_saida), exist_ok=True)

    
    arquivos_csv = glob.glob(os.path.join(pasta_de_entrada, "*.csv"))

    if not arquivos_csv:
        print(f"    [AVISO] Nenhum arquivo .csv encontrado em '{pasta_de_entrada}'.")
        return

    df_final = None

    
    mapa_colunas = {
        os.path.basename(arq): os.path.splitext(os.path.basename(arq))[0]
        for arq in arquivos_csv
    }

    for nome_arquivo, nome_coluna in mapa_colunas.items():
        caminho_arquivo = os.path.join(pasta_de_entrada, nome_arquivo)
        
        try:
            df = pd.read_csv(caminho_arquivo)
        except Exception as e:
            print(f"    [ERRO] Não foi possível ler o arquivo {caminho_arquivo}: {e}")
            continue
        
        for col in df.columns:
            if col != "data":
                df = df.rename(columns={col: nome_coluna})
        
        if df_final is None:
            df_final = df
        else:
            df_final = pd.merge(df_final, df, on="data", how="outer")

    if df_final is not None:
        df_final.to_csv(arquivo_de_saida, index=False, encoding="utf-8-sig")
        print(f"    ✓ Dados unificados salvos em: {arquivo_de_saida}")
    else:
        print("    [ERRO] Não foi possível criar o arquivo unificado.")

if __name__ == '__main__':
    print("Este script agora é chamado pelo main.py com pastas específicas.")
