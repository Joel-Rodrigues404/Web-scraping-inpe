# -*- coding: utf-8 -*-
import pandas as pd
import glob
import os

def unir_csvs_por_municipio(pasta_de_downloads, arquivo_de_saida):
  
    caminho_busca = os.path.join(pasta_de_downloads, "*.csv")
    arquivos_csv = glob.glob(caminho_busca)

    if not arquivos_csv:
        print(f"    [AVISO] Nenhum arquivo .csv encontrado em '{pasta_de_downloads}'.")
        return

    lista_dataframes = []
    for caminho_arquivo in arquivos_csv:
        try:
            nome_coluna = os.path.splitext(os.path.basename(caminho_arquivo))[0]
            
            df_temp = pd.read_csv(caminho_arquivo)
            
            df_temp = df_temp.rename(columns={df_temp.columns[1]: nome_coluna})
            
            lista_dataframes.append(df_temp)
        except Exception as e:
            print(f"    [ERRO] Falha ao processar o arquivo {caminho_arquivo}: {e}")
            continue

    if not lista_dataframes:
        print("    [ERRO] Nenhum dataframe foi carregado. A unificação foi cancelada.")
        return

    # Começa com o primeiro dataframe da lista
    df_final = lista_dataframes[0]

    # Junta os dataframes
    for df_para_juntar in lista_dataframes[1:]:
        df_final = pd.merge(df_final, df_para_juntar, on="data", how="outer")

    pasta_saida = os.path.dirname(arquivo_de_saida)
    os.makedirs(pasta_saida, exist_ok=True)
    
    df_final.to_csv(arquivo_de_saida, index=False, encoding="utf-8-sig")
    print(f"    [FINALMENTE] Arquivos unificados com sucesso em: {arquivo_de_saida}")