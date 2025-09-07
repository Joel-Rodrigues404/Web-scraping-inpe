import pandas as pd
import os

# --- CONFIGURAÇÃO ---
# Coloque aqui o nome EXATO do arquivo com a sua tabela de médias por município.
# Pelo nosso histórico, o nome provavelmente é 'ANALISE_COMPARATIVA_MUNICIPIOS.csv'
ARQUIVO_DE_ENTRADA = 'ESTATISTICAS_TOTAIS_CEARA_184_MUNICIPIOS.csv'

# Nome do arquivo de saída com a tabela final de Z-scores.
ARQUIVO_DE_SAIDA = 'TABELA_FINAL_ZSCORES_POR_MUNICIPIO.csv'


# ---------------------------------

def padronizar_tabela_de_medias(arquivo_entrada):
    """
    Lê uma tabela de médias por município e padroniza cada coluna
    (variável) usando o Escore-Z.
    """
    print(f"--- Padronizando a Tabela de Resultados ---")

    # --- 1. Carregar a Tabela de Médias ---
    if not os.path.exists(arquivo_entrada):
        print(f" ERRO: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return

    try:
        # Define a coluna 'municipio' como o índice da tabela.
        df_medias = pd.read_csv(arquivo_entrada, index_col='municipio')
        print(f" Tabela de médias '{arquivo_entrada}' carregada com sucesso.")
    except Exception as e:
        print(f" ERRO ao carregar o arquivo CSV: {e}")
        return

    # --- 2. Padronizar cada coluna da tabela ---
    print("🔬 Aplicando o Z-score em cada coluna...")

    # Seleciona apenas as colunas numéricas para a padronização.
    # O script vai ignorar automaticamente as colunas de Z-score que já existiam.
    colunas_para_padronizar = [
        'INTENSIDADE_DO_VENTO',
        'PRECIPITAÇÃO_TOTAL',
        'TEMPERATURA_MÉDIA',
        'UMIDADE_RELATIVA'
    ]

    # Cria um novo DataFrame para os resultados do Z-score
    df_zscores = df_medias[colunas_para_padronizar].copy()

    for coluna in colunas_para_padronizar:
        media_da_coluna = df_zscores[coluna].mean()
        desvio_padrao_da_coluna = df_zscores[coluna].std()

        # Aplica a fórmula do Z-score na coluna inteira
        df_zscores[coluna] = (df_zscores[coluna] - media_da_coluna) / desvio_padrao_da_coluna

    print("✔️ Todas as colunas foram padronizadas.")

    # --- 3. Salvar a tabela final de Z-scores ---
    try:
        df_zscores.to_csv(ARQUIVO_DE_SAIDA, float_format='%.4f')
        print(f"\n SUCESSO! A tabela final de Z-scores foi salva em '{ARQUIVO_DE_SAIDA}'.")

        print("\nPrévia da tabela final de Z-scores:")
        print(df_zscores.head())

    except Exception as e:
        print(f"\n ERRO ao salvar o arquivo final: {e}")


if __name__ == '__main__':
    padronizar_tabela_de_medias(ARQUIVO_DE_ENTRADA)