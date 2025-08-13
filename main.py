from dotenv import load_dotenv
import os
from get_vars import main
from get_archive_by_var_request import baixar_arquivo

load_dotenv()


ESCOLHAS = os.getenv("ESCOLHAS", "").split(",")
CAMPOS = os.getenv("CAMPOS", "").split(",")
VARIAVEIS = os.getenv("VARIAVEIS", "").split(",")
ANUAIS = os.getenv("ANUAIS", "").split(",")
TOKEN = str(os.environ.get("TOKEN")) 
LONGITUDE = str(os.environ.get("LONGITUDE"))
LATITUDE = str(os.environ.get("LATITUDE"))
URL = str(os.environ.get("URL"))

# print("ESCOLHAS:", ESCOLHAS)
# print("VARIAVEIS:", VARIAVEIS)

# for var in VARIAVEIS:
#     ESCOLHAS[6] = var
#     main(ESCOLHAS, CAMPOS, TOKEN, LONGITUDE, LATITUDE, URL, ANUAIS)


ESCOLHAS[6] = VARIAVEIS[-1]
# main(ESCOLHAS, CAMPOS, TOKEN, LONGITUDE, LATITUDE, URL, ANUAIS)


# arquivo_json = "dados.json"
# var = ESCOLHAS[6]
# variavel = var
# nome_arquivo = var + ".json"
# baixar_arquivo(arquivo_json, variavel, TOKEN, nome_arquivo=nome_arquivo)

arquivo_json = "dados.json"
for var in VARIAVEIS:
    variavel = var
    nome_arquivo = var + ".csv"
    baixar_arquivo(arquivo_json, variavel, TOKEN, nome_arquivo=nome_arquivo)
