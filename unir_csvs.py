import pandas as pd
import glob
import os
from pathlib import Path


ROOT_DIR = Path(__file__).parent
PATH_DOWNLOADS = ROOT_DIR / "downloads"
PATH_FINAL = ROOT_DIR / "final"

mapa_colunas = {
    os.path.basename(arq): os.path.splitext(os.path.basename(arq))[0]
    for arq in glob.glob(os.path.join(PATH_DOWNLOADS, "*.csv"))
}


df_final = None

for nome_arquivo, nome_coluna in mapa_colunas.items():
    caminho_arquivo = os.path.join(PATH_DOWNLOADS, nome_arquivo)
    
    df = pd.read_csv(caminho_arquivo)
    
    for col in df.columns:
        if col != "data":
            df = df.rename(columns={col: nome_coluna})
    
    if df_final is None:
        df_final = df
    else:
        df_final = pd.merge(df_final, df, on="data", how="outer")

if df_final is not None:
    saida = os.path.join(PATH_FINAL, "dados_unidos.csv")
    df_final.to_csv(saida, index=False, encoding="utf-8-sig")

    print(f"Arquivo salvo em: {saida}")
else:
    print("Nenhum arquivo foi processado.")
