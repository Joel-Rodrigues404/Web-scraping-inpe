from selenium.webdriver.common.by import By
from browser import make_firefox_browser
import time
import json


def busca_elemento_xpath(xpath, driver):
    return driver.find_element(By.XPATH, xpath)

def pegar_texto_redundante(element, driver):
    texto = element.text.strip()
    if not texto:
        texto = driver.execute_script("return arguments[0].textContent;", element).strip()
    return texto

def seleciona_item_desejado(li, texto_li, driver, escolhas):
    try:
        lista = li.find_elements(By.TAG_NAME, "ul")
        for elemento in lista:
            opcoes = elemento.find_elements(By.TAG_NAME, "a")
            for opcao in opcoes:
                if opcao.text.strip() in escolhas:
                    driver.execute_script("arguments[0].scrollIntoView(true);", opcao)
                    opcao.click()
                    time.sleep(0.3)
                    print(f"[OK] Subitem ({pegar_texto_redundante(opcao, driver)}) selecionado com sucesso.")
                    break
    except Exception as e:
        print(f"[WARN] Não conseguiu capturar sublinks de {texto_li}")

def forcar_clique_li(lista, driver):
    try:
        link = lista.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        driver.execute_script("arguments[0].style.display = 'block';", link)
        link.click()
        time.sleep(0.3)

        # print(f"[OK] Item ({link.text}) clicado com sucesso.") 
        # mostra todos os choices dentro do li
        print(f"[OK] Item ({lista.text})clicado com sucesso.") 
    except Exception as e:
        print(f"[WARN] Falha ao tentar clicar no item: {lista.text}")
        print(e)

def seleciona_items_menu(itens, driver, campos, escolhas):
    for i in range(len(itens)):
        sidemenu = driver.find_element(By.ID, "sidemenu")
        itens = sidemenu.find_elements(By.TAG_NAME, "li")
        li = itens[i]
        texto_li = li.text.strip()

        if li.text in campos:
            forcar_clique_li(li, driver)
            seleciona_item_desejado(li, texto_li, driver, escolhas)
    
    print("[OK] itens selecionados")

def seleciona_localizacao(driver, escolhas):
    localizacao = busca_elemento_xpath('//*[@id="LiLocalizacao"]', driver)
    forcar_clique_li(localizacao, driver)
    seleciona_item_desejado(localizacao, "Localização", driver, escolhas)
    print("[OK] Localização selecionada.")

def preencher_inputs(latitude, longitude, token, driver):
    try:
        lat_input = busca_elemento_xpath('//*[@id="lat"]', driver)
        lon_input = busca_elemento_xpath('//*[@id="lon"]', driver)
        token_input = busca_elemento_xpath('//*[@id="info1"]', driver)

        lat_input.clear()
        lat_input.send_keys(latitude)
        lon_input.clear()
        lon_input.send_keys(longitude)
        token_input.clear()
        token_input.send_keys(token)

        print("[OK] Campos de localização e token preenchidos.")
    except Exception as e:
        print(f"[ERRO] Falha ao preencher Latitude/Longitude/Token:")

def clicar_botao_gerar_url(driver):
    try:
        gerar_url_btn = busca_elemento_xpath('//*[@id="btnVisualizar"]' , driver)
        driver.execute_script("arguments[0].scrollIntoView(true);", gerar_url_btn)
        time.sleep(1)

        driver.execute_script('$("#btnVisualizar").trigger("click");')
        
        time.sleep(2)
        print("[OK] Botão de GERAR URL clicado com sucesso.")
    except Exception as e:
        print(f"[WARN] Falha ao clicar no botão GERAR URL:")

def link_gerado(driver):
    xpath_url = busca_elemento_xpath('/html/body/div[2]/div/div/div/div[2]/code', driver)

    print("[OK] Botão de GERAR URL clicado com sucesso.")
    return xpath_url.text.strip()

def adiciona_link_ao_json(driver, nome_variavel, arquivo="dados.json"):
    link = link_gerado(driver)
    chave = nome_variavel.upper()

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}

    dados[chave] = link

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"[OK] Link adicionado como '{chave}' no {arquivo}")

def main(escolhas, campos, token, longitude, latitude, url, anuais):
    driver = make_firefox_browser()
    driver.get(url)
    time.sleep(2)

    sidemenu = driver.find_element(By.ID, "sidemenu")
    itens = sidemenu.find_elements(By.TAG_NAME, "li")
    variavel = escolhas[6]

    if variavel in anuais:
        escolhas[8] = "ANUAL"
        print(f"[INFO] Variável '{variavel}' é anual, ajustando o menu.")

    seleciona_items_menu(itens, driver, campos, escolhas)
    seleciona_localizacao(driver, escolhas)
    preencher_inputs(latitude, longitude, token, driver)
    clicar_botao_gerar_url(driver)
    adiciona_link_ao_json(driver, variavel);

    print("\n[✔] Processo concluído!")

    driver.quit()
