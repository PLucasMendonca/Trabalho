import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import re
import time
import datetime
import os
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

def get_assistant_response(prompt, user_input):
    messages = [
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        max_tokens=2,  # Defina um número pequeno para limitar a resposta a poucas palavras
    ).choices[0].message.content.strip()  # Remove espaços em branco

    return response

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
options = webdriver.ChromeOptions()
chrome_options = webdriver.ChromeOptions()

# Caminho desejado para a pasta de download
caminho_do_seu_diretorio = r'C:\Users\Windows 10\Documents\Chatpdf\Buscador\editais'

prefs = {"download.default_directory": caminho_do_seu_diretorio}
chrome_options.add_experimental_option("prefs", prefs)

# Criar uma instância do navegador Chrome com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

usuario = "fernanda@smartsupply.net.br"
senha = "Fer050287"
url = "https://elicitacao.com.br/"

# Use o Selenium para obter o conteúdo HTML da página
driver.get(url)
html = driver.page_source

# Use o BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html, 'html.parser')

# Criação do arquivo
nome_arquivo = 'informacoes_licitacoes.txt'

# Clica no primeiro botão
click_button = driver.find_element(By.CLASS_NAME, "nav-menu-link")
click_button.click()

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "email.form-control")))

# Localiza o campo de entrada de texto do usuário pelo atributo 'class'
usuario_element = driver.find_element(By.CLASS_NAME, "email.form-control")
usuario_element.send_keys(usuario)

# Localiza o campo de entrada de texto da senha pelo atributo 'class'
senha_element = driver.find_element(By.NAME, "nm_usu_senha")  # Substitua "senha" pelo atributo correto da senha
senha_element.send_keys(senha)

# Clica no segundo botão
click_button2 = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-logar")
click_button2.click()

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".menu-elicitacao__li")))

# Encontrar o elemento desejado
elemento = driver.find_element(By.CSS_SELECTOR, 'li.menu-elicitacao__li[name="eLicitaBoletim 4.0"]')

# Criar uma instância de ActionChains
actions = ActionChains(driver)

# Mover o mouse sobre o elemento
actions.move_to_element(elemento)

# Executar as ações
actions.perform()

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Pesquisa de Licitações']")))

# Encontrar e clicar no botão associado ao elemento "Pesquisa de Licitações"
driver.find_element(By.XPATH, "//span[text()='Pesquisa de Licitações']").click()

time.sleep(5)

# Encontrar e clicar no botão associado ao elemento "data de abertura"
data_abertura = driver.find_element(By.XPATH, '//*[@id="dtAbertura"]')

# Limpar o campo
data_abertura.clear()

# Inserir a data como string
data_atual = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%d/%m/%Y')
data_abertura.send_keys(data_atual)

# Encontrar e clicar no botão associado ao elemento "data até"
data_ate = driver.find_element(By.XPATH, '//*[@id="dtAberturaFim"]')

# Limpar o campo
data_ate.clear()

# Inserir a data como string
data_ate.send_keys(data_atual)

time.sleep(2)

# Encontrar o elemento Perfil de oportunidade ----
perfil_oportunidade = driver.find_element(By.XPATH, '//*[@id="sidebar-backdrop"]/div/div/div[7]/div/div/button/div')
perfil_oportunidade.click()

# Encontrar Perfil DO CLIENTE ---- MUDAR CLIENTE AQUI
perfil_oportunidade = driver.find_element(By.XPATH, '//li[@class="selectItem"]/span[text()="26.365.835/0001-39"]')
perfil_oportunidade.click()


# Encontrar o elemento select
select_element = driver.find_element(By.ID, "__BVID__63")

# Criar uma instância da classe Select
select = Select(select_element)

# Selecionar a opção por texto visível
select.select_by_visible_text("Por UF")

# Aguardar um momento para a seleção ser processada (ajuste conforme necessário)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "vfilter__footer__button")))

# Clicar no Botão Aplicar
click_button = driver.find_element(By.CLASS_NAME, "vfilter__footer__button")
click_button.click()

# Aguardar um tempo para a página carregar os resultados (ajuste conforme necessário)
time.sleep(10)

# Iterar sobre todos os estados
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

# Lista para armazenar todas as informações dos cards
# Lista para armazenar todas as informações dos cards
all_cards_info = []

for estado in estados:
    # Encontrar todos os elementos span com a classe 'bold-century'
    elementos_span = driver.find_elements(By.CLASS_NAME, 'bold-century')

    estado_encontrado = False  # Flag para indicar se o estado foi encontrado

    # Iterar sobre os elementos span
    for elemento_span in elementos_span:
        # Obter o texto dentro do elemento span
        texto_span = elemento_span.text

        # Verificar se o texto contém o estado atual
        if estado in texto_span:
            # Se encontrado, continue com o processamento
            print(f"Estado {estado} encontrado em: {texto_span}")

            # Tentar extrair o número
            try:
                numero = int(texto_span.split('(')[1].split(')')[0])
                print(f'O número para o estado {estado} é: {numero}')

                # Clicar no elemento span usando JavaScript
                driver.execute_script("arguments[0].click();", elemento_span)

                estado_encontrado = True
                break
            except (IndexError, ValueError):
                print(f'Número não encontrado ou não é um valor inteiro para o estado {estado}. Pulando para o próximo estado.')

    # Se o estado foi encontrado e tem um número associado, continue com o processamento
    if estado_encontrado and 'numero' in locals():
        # Aumentar o tempo de espera, se necessário
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'card-pesquisa-licitacoes')))

        limite_cartoes = numero

        try:
            # Iterar sobre os cards e extrair informações específicas
            # Encontrar todos os elementos 'card-pesquisa-licitacoes'
            elementos_card = driver.find_elements(By.CLASS_NAME, 'card-pesquisa-licitacoes')

            # Iterar sobre os elementos card
            for card in elementos_card:
                try:

                    # Clicar noo botão
                    button_below_id = card.find_element(By.XPATH, './/button[@class="mr-2 rounded"]')
                    driver.execute_script("arguments[0].click();", button_below_id)

                    # Aguardar até que o modal esteja visível após clicar no botão
                    modal_visible = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-content')))


                    achdarid = driver.find_elements(By.CSS_SELECTOR,'.modal-class .p-4')
                    
                    # Encontrar o elemento com a classe 'highlight-text' dentro do elemento card
                    id_elemento = card.find_element(By.XPATH, ".//p/span[@class='highlight-text' and contains(text(), 'ID:')]")
                    
                    # Obter o texto do ID usando expressão regular
                    id_texto = re.search(r'\bID:\s*(\d+)\b', id_elemento.text).group(1)
                    
                    print(f"ID: {id_texto}")
                    
                    # Agora, encontre o elemento span dentro do modal associado ao cartão específico
                    span_element_modal = modal_visible.find_element(By.XPATH, './/p[@class="col-md-12"][2]/span[@class="bold-century"]/following-sibling::span')
                    span_text_modal = span_element_modal.text

                    def check_compatibility(prompt, span_text_modal, id_texto):
                        response = get_assistant_response(prompt, span_text_modal)
                        
                        print(f"Texto do Span dentro do modal: {span_text_modal}")
                        print(f"Resposta do Assistente: {response}")

                        if "sim" in response.lower():
                            # Encontrar o botão para baixar o anexo
                            download_button = modal_visible.find_element(By.XPATH, '//*[@id="modal-pesquisa-de-licitacoes___BV_modal_body_"]/div/div[4]/div/div[1]/div/ul/button')

                            # Verificar se o botão está visível
                            if download_button.is_displayed():
                                download_button.click()

                                print("Conteúdo compatível. Baixando anexo.")

                                safe_filename = os.path.join(os.getcwd(),'editais', f"{id_texto}.txt")
                                with open(safe_filename, "w", encoding="utf-8") as arquivo:
                                    arquivo.write(f"Texto do Span dentro do modal: {span_text_modal}")

                                print(f"Arquivo {safe_filename} salvo com sucesso.")
                                
                                # Aguardar um tempo para o download ser iniciado (ajuste conforme necessário)
                                time.sleep(10)

                            else:
                                # Encontrar o botão para baixar todos os anexos
                                download_all_button = modal_visible.find_element(By.CLASS_NAME, 'download-all')

                                # Verificar se o botão está visível
                                if download_all_button.is_displayed():
                                    # 2ª situação: Abrir uma nova página
                                    link_site_element = modal_visible.find_element(By.XPATH, './/p[contains(text(), "ser redirecionado para o site do órgão")]/following-sibling::a')
                                    link_site = link_site_element.get_attribute("href")
                                    print(f"Não foram encontrados os anexos da licitação. Acesse o site para baixar as informações: {link_site}")
                                    # Salvar a informação no arquivo
                                    info_filename = os.path.join(os.getcwd(), f"info_{id_texto}.txt")
                                    with open(info_filename, "w", encoding="utf-8") as arquivo_info:
                                        arquivo_info.write(f"Não foram encontrados anexos para o ID: {id_texto}. Acesse o site para baixar as informações: {link_site}")
                                        print(f"Informações salvas no arquivo {info_filename}.")

                                        time.sleep(2)
                                else:
                                    # 3ª situação: Solicitar edital
                                    print(f"Edital da licitação não foi encontrado. Solicite o edital para o ID: {id_texto} através do site.")
                                    
                                    # Salvar a informação no arquivo
                                    info_filename = os.path.join(os.getcwd(), f"info_{id_texto}.txt")
                                    with open(info_filename, "w", encoding="utf-8") as arquivo_info:
                                        arquivo_info.write(f"Edital não encontrado para o ID: {id_texto}. Solicite o edital através do site.")
                                        print(f"Informações salvas no arquivo {info_filename}.")
                                        
                                        time.sleep(2)
                        else:
                            print("Conteúdo não compatível, não baixando anexo.")

                    # Verificar compatibilidade e salvar o arquivo se compatível
                    check_compatibility("Verifique se no texto, o serviço apresentado é similar ou tem algo correlacionado a Serviço de engenharia elétrica. Responda somente sim ou não", span_text_modal, id_texto)
                    
                    # Aguardar tempo suficiente para o processamento da resposta do GPT-3.5
                    time.sleep(5)

                    # Se a resposta indicar correlação, salve os dados
                    response = get_assistant_response("Verifique a correlação", span_text_modal)

                    # Voltar para a página anterior
                    # Encontrar o botão "Fechar" dentro do modal
                    botao_fechar = modal_visible.find_element(By.CLASS_NAME, 'cancel')

                    # Clicar no botão "Fechar"
                    botao_fechar.click()

                    time.sleep(5)

                except NoSuchElementException:
                    print("Elemento 'id-grid' ou botão abaixo do ID não encontrado para este card. Ignorando.")
                
                # Se já tiver salvo o número desejado de cards, pare a execução
                if len(all_cards_info) >= limite_cartoes:
                    break

        except TimeoutException:
            print("Tempo limite excedido ao aguardar a visibilidade dos elementos 'card-pesquisa-licitacoes'.")

        # Imprimir a lista de informações de todos os cards
        print(all_cards_info)

        # Limpar a lista para o próximo estado
        all_cards_info = []

    # Se não encontrou o estado, imprima uma mensagem 
    print(f"Estado {estado} não encontrado nos elementos span ou sem número associado. Pulando para o próximo estado.")

# Fechar o navegador após a conclusão
driver.quit()
