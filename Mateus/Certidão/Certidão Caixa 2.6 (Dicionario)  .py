from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import speech_recognition as sr
import time
from dicionario import traducao

# Configurações do Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

Acha_Cnpj = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtInscricao1"]'))
)

CNPJ = '15665964000126'
time.sleep(1)

# Digitar CNPJ
Acha_Cnpj.send_keys(CNPJ)

# Função para processar a descrição verbal
def processar_descricao(texto):
    texto = texto.lower()
    palavras = texto.split(" ")
    descricao_processada = ""
    i = 0

    while i < len(palavras):
        if palavras[i] in ["letra", "número"]:
            if i + 2 < len(palavras) and palavras[i + 2] in ["letra", "número"]:
                descricao_processada += palavras[i] + " " + palavras[i + 1] + ", "
            else:
                descricao_processada += palavras[i] + " " + palavras[i + 1] + " "
            i += 2
        else:
            descricao_processada += palavras[i] + ", "
            i += 1

    return descricao_processada.strip(", ")



# Função para converter a descrição em código alfanumérico
def converter_para_codigo(descricao_processada):
    elementos = descricao_processada.split(", ")
    codigo = ""
    for elem in elementos:
        if elem in traducao:
            codigo += traducao[elem]
        else:
            # Adiciona um placeholder caso o elemento não esteja no dicionário
            codigo += "?"
    return codigo
    

# Configuração do reconhecedor de voz
r = sr.Recognizer()
mic = sr.Microphone()

# Iniciar a gravação antes de clicar no elemento de áudio
with mic as fonte:
    r.adjust_for_ambient_noise(fonte)
    print("Reconhecimento de voz ativado com Google Speech Recognition. Aguarde o código...")
    
    # Encontrar o elemento de áudio pelo seu XPath e clicar
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm"]/div[5]/div[2]/div[3]/a/img'))
    )
    element.click()

    # Capturar áudio
    audio = r.listen(fonte, timeout=30, phrase_time_limit=30)
    print("Processando o áudio...")

# Reconhecimento de voz com Google
try:
    question = r.recognize_google(audio, language="pt-BR")
except sr.UnknownValueError:
    print("Google Speech Recognition não entendeu o áudio")
except sr.RequestError as e:
    print(f"Erro na solicitação ao Google Speech Recognition; {e}")

# Processamento do código
if question:
    print("Código recebido:", question)
    descricao_processada = processar_descricao(question)
    codigo_alfanumerico = converter_para_codigo(descricao_processada)
    print("Código alfanumérico:", codigo_alfanumerico)
    print(descricao_processada)

    # Preencher o captcha
    Acha_Captcha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtCaptcha"]'))
    )
    Acha_Captcha.send_keys(codigo_alfanumerico)
else:
    print("Não foi possível entender o áudio ou nenhuma entrada foi fornecida")

# Encontrar o botão consultar pelo seu XPath e clicar
botao_consultar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:btnConsultar"]'))
)

botao_consultar.click()


texto_regularidade = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.XPATH, '//span[@class="feedback-text"]'))
).text

# Verificar se a empresa está regular
if "A EMPRESA abaixo identificada está REGULAR perante o FGTS:" in texto_regularidade:
    # Encontrar o link certificado de regularidade pelo seu XPath e clicar
    botao_consultar = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:j_id51"]'))
    )
    botao_consultar.click()
    print("Empresa regular.")
else:
    # Empresa não está regular
    print("A empresa não está regular perante o FGTS.")
    # Abrir um arquivo txt e salvar o CNPJ da empresa
    with open("empresas_irregulares.txt", "a") as arquivo:
        arquivo.write("CNPJ: " + CNPJ + " - Empresa não regular.\n")

# botão para visualizar - //*[@id="mainForm:btnVisualizar"]
# botão imprimir -  //*[@id="mainForm:btImprimir4"]
# Aguardar e fechar o navegador
time.sleep(10)
driver.quit()
print("Programa encerrado")
