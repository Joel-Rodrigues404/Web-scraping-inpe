import pandas as pd
import os

# --- CONFIGURAÇÃO ---
# Nome da sua pasta final com os dados prontos.
PASTA_FINAL_COM_DADOS = 'final'

# --- NÃO MUDE MAIS NADA ABAIXO ---
ARQUIVO_LISTA_MUNICIPIOS = 'municipios.csv'
ARQUIVO_DE_SAIDA = 'ESTATISTICAS_TOTAIS_CEARA_184_MUNICIPIOS.csv'


# ---------------------------------

def gerar_analise_total(pasta_dados, arquivo_lista):
    """
    Junta os dados de TODOS os municípios em um único conjunto e calcula
    as estatísticas descritivas para o total geral.
    """
    print(f"--- Iniciando Análise Total do Ceará (184 Municípios) ---")
    print(f"Pasta de dados: '{pasta_dados}'")

    try:
        df_lista = pd.read_csv(arquivo_lista, sep=';')
        nomes_municipios = df_lista['municipio'].tolist()
        print(f"Lista de {len(nomes_municipios)} municípios carregada.")
    except Exception as e:
        print(f"ERRO: Não foi possível ler o arquivo '{arquivo_lista}'. Detalhes: {e}")
        return

    lista_de_dfs = []
    print("\n🔎 Lendo e juntando os arquivos de todos os municípios...")

    for nome_municipio in nomes_municipios:
        caminho_arquivo = os.path.join(pasta_dados, f"{nome_municipio}.csv")

        if os.path.exists(caminho_arquivo):
            try:
                df_temp = pd.read_csv(caminho_arquivo)
                lista_de_dfs.append(df_temp)
            except Exception as e:
                print(f"   ERRO ao ler '{nome_municipio}.csv': {e}")
        else:
            print(f"  ⚠AVISO: Arquivo '{nome_municipio}.csv' não encontrado.")

    if not lista_de_dfs:
        print("\n Nenhum dado foi carregado. A pasta de dados está correta?")
        return

    # Junta TUDO em um único DataFrame
    df_consolidado = pd.concat(lista_de_dfs, ignore_index=True)
    print(f"\n✔ {len(lista_de_dfs)} arquivos foram consolidados com sucesso.")

    # Calcula as estatísticas para o conjunto de dados GERAL
    print("Calculando as estatísticas gerais do estado...")
    estatisticas_gerais = df_consolidado.describe()

    # Adiciona a contagem total de municípios na análise
    estatisticas_gerais['total_municipios_analisados'] = len(lista_de_dfs)

    try:
        estatisticas_gerais.to_csv(ARQUIVO_DE_SAIDA)
        print(f"\nSUCESSO! Análise completa salva em '{ARQUIVO_DE_SAIDA}'.")
    except Exception as e:
        print(f"\n ERRO ao salvar o arquivo final: {e}")


if __name__ == '__main__':
    gerar_analise_total(PASTA_FINAL_COM_DADOS, ARQUIVO_LISTA_MUNICIPIOS)