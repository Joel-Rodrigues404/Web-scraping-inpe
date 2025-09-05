#Extrator de Dados Climáticos - INPE API
Este projeto contém um script em Python para automatizar a extração de dados climáticos da API do INPE, com foco em gerar arquivos de séries temporais por município.

Foi desenvolvido para apoiar atividades de pesquisa e análise de dados para a UFC(Universidade Federal do Ceará) em forma de resumo simples para apresentação universitária.

##Funcionalidades
* Extração de dados para múltiplos municípios a partir de uma lista em CSV.
* Seleção de múltiplas variáveis climáticas (anuais e mensais) via arquivo de configuração.
* Consolidação automática dos dados de um município em um único arquivo CSV, com as variáveis organizadas em colunas.

##Setup do Ambiente
**Pré-requisitos**
* Python 3.8+
* Git
* Token da API Pclima disponível em [Pclima INPE]([http://pclima.inpe.br/analise/API/](http://pclima.inpe.br/analise/API/cadastro.html))

##Instalação
**1. Clone o Repositório:**
```sh
git clone [https://github.com/Joel-Rodrigues404/Web-scraping-inpe.git](https://github.com/Joel-Rodrigues404/Web-scraping-inpe.git)
cd Web-scraping-inpe
```
**2. Crie e ative um ambiente virtual:**
```sh
python -m venv .venv
.venv\Scripts\activate
```
**3. Instale as depedências:**
```
pip install -r requirements.txt
```
**4. Configure as variáveis de ambiente:**
Copie o arquivo .env-example e renomeie-o para .env
```
copy .env-example .env
```
Abra o arquivo .env e preencha as variáveis com os seus dados, principalmente o token da API.

##Como usar
**1. Configurar Municípios**
Edite o arquivo municipios.csv para definir a lista de localidades desejadas. O formato deve ser mantido: municipio;latitude;longitude.

**2. Configurar Variáveis**

No arquivo .env, edite as seguintes listas:

* VARIAVEIS: Lista separada por vírgulas com os nomes das variáveis a serem baixadas.

* ANUAIS: Subconjunto da lista acima, contendo apenas as variáveis de frequência anual.

**3. Executar o Script**
Com o ambiente virtual ativado, execute o main.py:
```python
python main.py
```
O script irá processar cada município, baixar os dados para a pasta /downloads e salvar os arquivos consolidados na pasta /final.

