# -*- coding: utf-8 -*-
import pandas as pd
from dotenv import load_dotenv
import os
import time


from get_archive_by_var_request import baixar_arquivo
from unir_csvs import unir_csvs_por_municipio 

# --- CONFIGURAÇÃO ---
load_dotenv()

# .env
TOKEN = os.getenv("TOKEN")

VARIAVEIS_PARA_BAIXAR = os.getenv("VARIAVEIS", "").split(",")
ANUAIS = os.getenv("ANUAIS", "").split(",")
ARQUIVO_MUNICIPIOS = "municipios.csv"

# Constantes para a URL
PROJETO = "PR0002"
MODELO_GLOBAL = "MO0003"
EXPERIMENTO = "EX0003"
PERIODO = "PE0001"
CENARIO = "CE0007"
TIPO_SAIDA_PONTO = "Ponto"
TIPO_SAIDA_CSV = "CSV"
PERIODO_DOWNLOAD = "PDT0002"
FREQ_ANUAL = "FR0001"
FREQ_MENSAL = "FR0003"

# O dicionário retirado a partir do INPE
MAPEAMENTO_VARIAVEIS = {
    "TEMPERATURA MÁXIMA":                   {"codigo": "VR0001", "nome_curto": "tasmax"},
    "TEMPERATURA MÍNIMA":                   {"codigo": "VR0002", "nome_curto": "tasmin"},
    "TEMPERATURA MÉDIA":                    {"codigo": "VR0003", "nome_curto": "tas"},
    "PRECIPITAÇÃO TOTAL":                   {"codigo": "VR0004", "nome_curto": "pr"},
    "UMIDADE ESPECÍFICA":                   {"codigo": "VR0005", "nome_curto": "huss"},
    "UMIDADE RELATIVA":                     {"codigo": "VR0006", "nome_curto": "hurs"},
    "RADIAÇÃO DE ONDA LONGA":               {"codigo": "VR0008", "nome_curto": "rlds"},
    "RADIAÇÃO DE ONDA CURTA":               {"codigo": "VR0009", "nome_curto": "rsds"},
    "COMPONENTE U":                         {"codigo": "VR0010", "nome_curto": "uas"},
    "COMPONENTE V":                         {"codigo": "VR0011", "nome_curto": "vas"},
    "INTENSIDADE DO VENTO":                 {"codigo": "VR0046", "nome_curto": "sfcWind"},
    "PRESSÃO À SUPERFÍCIE":                 {"codigo": "VR0047", "nome_curto": "ps"},
    "Nº MÁX. DE DIAS SECOS CONSECUTIVOS":    {"codigo": "VR0012", "nome_curto": "CDD"},
    "Nº MÁX. DE DIAS CONSECUTIVOS COM CHUVA":{"codigo": "VR0014", "nome_curto": "CWD"},
    "Nº DE DIAS COM CHUVA > 10MM":          {"codigo": "VR0019", "nome_curto": "R10mm"},
    "Nº DE DIAS COM CHUVA > 20MM":          {"codigo": "VR0020", "nome_curto": "R20mm"},
    "PRECIPITAÇÃO TOTAL > PERCENTIL 95":    {"codigo": "VR0022", "nome_curto": "R95p"},
    "PRECIPITAÇÃO TOTAL > PERCENTIL 99":    {"codigo": "VR0023", "nome_curto": "R99p"},
    "QUANT. MÁX. DE CHUVA EM 1 DIA":        {"codigo": "VR0024", "nome_curto": "RX1day"},
    "QUANT. MÁX. DE CHUVA EM 5 DIAS CONSEC.":{"codigo": "VR0025", "nome_curto": "RX5day"},
    "PRECIPITAÇÃO MÉDIA EM DIAS ÚMIDOS":    {"codigo": "VR0026", "nome_curto": "SDII"},
    "% DE DIAS COM TEMP. MÍNIMA < PERCENTIL 10": {"codigo": "VR0028", "nome_curto": "TN10p"},
    "% DE DIAS COM TEMP. MÍNIMA > PERCENTIL 90": {"codigo": "VR0029", "nome_curto": "TN90p"},
    "% DE DIAS COM TEMP. MÁXIMA < PERCENTIL 10": {"codigo": "VR0033", "nome_curto": "TX10p"},
    "% DE DIAS COM TEMP. MÁXIMA > PERCENTIL 90": {"codigo": "VR0034", "nome_curto": "TX90p"},
}

def main():
    try:
        df_municipios = pd.read_csv(ARQUIVO_MUNICIPIOS, encoding='utf-8-sig', sep=';')
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo '{ARQUIVO_MUNICIPIOS}' não encontrado.")
        return
    except Exception as e:
        print(f"ERRO CRÍTICO ao ler o CSV: {e}")
        return

    # Limpeza de dados
    df_municipios['latitude'] = df_municipios['latitude'].astype(str).str.replace(',', '.', regex=False)
    df_municipios['longitude'] = df_municipios['longitude'].astype(str).str.replace(',', '.', regex=False)

    total_municipios = len(df_municipios)
    print(f"Iniciando automação para {total_municipios} municípios.")

    for index, row in df_municipios.iterrows():
        municipio_nome = row['municipio']
        latitude = row['latitude']
        longitude = row['longitude']
        
        print(f"\n{'='*60}")
        print(f"PROCESSANDO: {municipio_nome.upper()} ({index + 1}/{total_municipios})")
        print(f"{'='*60}")

        pasta_destino = os.path.join("downloads", municipio_nome)

        for var_nome in VARIAVEIS_PARA_BAIXAR:
            if var_nome not in MAPEAMENTO_VARIAVEIS:
                print(f"  [AVISO] Variável '{var_nome}' não reconhecida. Pulando.")
                continue

            var_info = MAPEAMENTO_VARIAVEIS[var_nome]
                        
            if var_nome in ANUAIS:
                frequencia_str = "Anual"
                frequencia_cod = FREQ_ANUAL
            else:
                frequencia_str = "Mensal"
                frequencia_cod = FREQ_MENSAL
            
            url_final = (
                f"http://4cn-api.cptec.inpe.br/api/v1/public/{TIPO_SAIDA_PONTO}/{TIPO_SAIDA_CSV}/{frequencia_str}/"
                f"{latitude}/{longitude}/{PROJETO}/{MODELO_GLOBAL}/{EXPERIMENTO}/{PERIODO}/{CENARIO}/"
                f"{var_info['codigo']}/{frequencia_cod}/{PERIODO_DOWNLOAD}/{var_info['nome_curto']}"
            )
            
            nome_arquivo_csv = f"{var_nome.replace(' ', '_').replace('>', 'maior')}.csv"
            
            print(f"  -> Baixando: {var_nome}")
            baixar_arquivo(url_final, TOKEN, pasta_destino, nome_arquivo_csv)
            time.sleep(1)

        # Chamada final para unificação dos CSVs, it's done 
        print(f"\n  -> Unificando dados para {municipio_nome}...")
        arquivo_final = os.path.join("final", f"{municipio_nome}.csv")
        unir_csvs_por_municipio(pasta_destino, arquivo_final)

    print("\n\nPROCESSO DE AUTOMAÇÃO CONCLUÍDO!")

if __name__ == "__main__":
    main()