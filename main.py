# -*- coding: utf-8 -*-
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Importa a função de download simplificada
from get_archive_by_var_request import baixar_arquivo

# --- CONFIGURAÇÃO ---
load_dotenv()

# .env
TOKEN = os.getenv("TOKEN")
VARIAVEIS_PARA_BAIXAR = os.getenv("VARIAVEIS", "").split(",")
ANUAIS = os.getenv("ANUAIS", "").split(",")
ARQUIVO_MUNICIPIOS = "municipios.csv"


# Pega cada código da API e converte diretamente pro CSV, tá muito feio e desorganizado
MAPEAMENTO_VARIAVEIS = {
    # Variáveis Mensais
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
    # Variáveis Anuais
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

# --- FUNÇÃO PRINCIPAL DA AUTOMAÇÃO ---

def main():
    try:
        # Lê o CSV especificando o ponto e vírgula como separador
        df_municipios = pd.read_csv(
            ARQUIVO_MUNICIPIOS, 
            encoding='utf-8-sig',
            sep=';' 
        )
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Ficheiro '{ARQUIVO_MUNICIPIOS}' não encontrado.")
        return
    except Exception as e:
        print(f"ERRO CRÍTICO ao ler o CSV: {e}")
        return

    total_municipios = len(df_municipios)
    print(f"Iniciando automação para {total_municipios} municípios.")

    for index, row in df_municipios.iterrows():
        try:
            municipio_nome = row['municipio']
            # Converte as coordenadas para string, tratando a vírgula como separador decimal(codigo lixo, se quiser der uma limpa, no final o problema era o csv que fiz errado)
            latitude = str(row['latitude']).replace(',', '.')
            longitude = str(row['longitude']).replace(',', '.')
        except KeyError as e:
            print(f"ERRO CRÍTICO: Não foi possível encontrar a coluna {e} no CSV.")
            print(f"Colunas encontradas: {list(df_municipios.columns)}")
            return
        except Exception as e:
            print(f"ERRO ao processar a linha {index + 1} do CSV: {e}")
            continue # Pula para o próximo município
        
        print(f"\n{'='*60}")
        print(f"PROCESSANDO: {municipio_nome.upper()} ({index + 1}/{total_municipios})")
        print(f"{'='*60}")

        pasta_destino = os.path.join("downloads", municipio_nome)

        for var_nome in VARIAVEIS_PARA_BAIXAR:
            if var_nome not in MAPEAMENTO_VARIAVEIS:
                print(f"  [AVISO] Variável '{var_nome}' não reconhecida. A pular.")
                continue

            var_info = MAPEAMENTO_VARIAVEIS[var_nome]
            
            if var_nome in ANUAIS:
                frequencia_str = "Anual"
                frequencia_cod = "FR0001"
            else:
                frequencia_str = "Mensal"
                frequencia_cod = "FR0003"

            # Constrói a URL de download diretamente
            url_final = (
                f"http://4cn-api.cptec.inpe.br/api/v1/public/Ponto/CSV/{frequencia_str}/"
                f"{latitude}/{longitude}/PR0002/MO0003/EX0003/PE0001/CE0007/"
                f"{var_info['codigo']}/{frequencia_cod}/PDT0002/{var_info['nome_curto']}"
            )
            
            nome_ficheiro_csv = f"{var_nome.replace(' ', '_').replace('>', 'maior')}.csv"
            
            print(f"  -> A baixar: {var_nome}")
            baixar_arquivo(url_final, TOKEN, pasta_destino, nome_ficheiro_csv)
            time.sleep(1)

    print("\n\nPROCESSO DE AUTOMAÇÃO CONCLUÍDO!")

if __name__ == "__main__":
    main()

#Acredito que dá pra deixar o codigo mais legivel, tem bastante coisa redundante, talvez façamos depois.
#além disso as libs que tu usou foram bem legais de se aprender, embora eu nao tenha aprendido de fato kkk, mas deu uma xp