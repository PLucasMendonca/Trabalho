from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import speech_recognition as sr
import time
from dicionario import traducao
from script_pyautogui import clicar_botao_impressao
import threading

# Configurações do Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

CNPJ = '15665964000126'

# Digitar CNPJ
Acha_Cnpj = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtInscricao1"]')))
Acha_Cnpj.send_keys(CNPJ)



# Função para processar a descrição verbal
def processar_descricao(texto):
    texto = texto.lower()
    palavras = texto.split(" ")
    descricao_processada = ""
    i = 0

    while i < len(palavras):
        if palavras[i] in ["letra", "número"]:
            if i + 1 < len(palavras):
                if i + 2 < len(palavras) and palavras[i + 2] in ["letra", "número"]:
                    descricao_processada += palavras[i] + " " + palavras[i + 1] + ", "
                    i += 2
                else:
                    descricao_processada += palavras[i] + " " + palavras[i + 1] + " "
                    i += 2
            else:
                descricao_processada += palavras[i] + ", "
                i += 1
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
            codigo += "?"
    return codigo

# Configuração do reconhecedor de voz
r = sr.Recognizer()
mic = sr.Microphone()

def capturar_e_processar_audio():
    with mic as fonte:
        r.adjust_for_ambient_noise(fonte)
        print("Reconhecimento de voz ativado com Google Speech Recognition. Aguarde o código...")
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm"]/div[5]/div[2]/div[3]/a/img')))
        element.click()
        audio = r.listen(fonte, timeout=35, phrase_time_limit=35)
        print("Processando o áudio...")

        try:
            question = r.recognize_google(audio, language="pt-BR")
            if question:
                descricao_processada = processar_descricao(question)
                print(descricao_processada)
                return descricao_processada, converter_para_codigo(descricao_processada)
        except (sr.UnknownValueError, sr.RequestError) as e:
            print(f"Erro no reconhecimento de voz: {e}")

        return None, None

# Iniciar o processo
descricao_processada, codigo_alfanumerico = capturar_e_processar_audio()

# Definindo a variável código alfanumérico com um valor padrão para evitar erro
codigo_alfanumerico = codigo_alfanumerico if codigo_alfanumerico is not None else ''

def tentar_novamente(descricao_processada):
    with open("descricao_invalida.txt", "a") as arquivo:
        arquivo.write(f"Descrição processada: {descricao_processada}\n")

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:j_id61"]/img'))).click()
    time.sleep(5)

    return capturar_e_processar_audio()

def verificar_captcha_invalido():
    try:
        captcha_invalido = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="mainForm"]/div[1]/span'))
        ).text
        return "Código Captcha Inválido" in captcha_invalido
    except Exception:
        return False
    
while True:
    descricao_processada, codigo_alfanumerico = capturar_e_processar_audio()

    if not codigo_alfanumerico or '?' in codigo_alfanumerico:
        print("Código alfanumérico inválido. Tentando novamente...")
        descricao_processada, codigo_alfanumerico = tentar_novamente(descricao_processada)
        continue  # Retorna ao início do loop para tentar novamente

    Acha_Captcha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtCaptcha"]'))
    )
    Acha_Captcha.clear()  # Limpa o campo do captcha
    Acha_Captcha.send_keys(codigo_alfanumerico)
    botao_consultar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:btnConsultar"]'))
    )
    botao_consultar.click()

    if verificar_captcha_invalido():
        print("Captcha inválido detectado. Tentando novamente...")
        descricao_processada, codigo_alfanumerico = tentar_novamente(descricao_processada)
        continue  # Retorna ao início do loop para capturar e processar o áudio novamente

    texto_regularidade = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//span[@class="feedback-text"]'))
    ).text

    if "A EMPRESA abaixo identificada está REGULAR perante o FGTS:" in texto_regularidade:
            botao_consultar = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:j_id51"]')))
            botao_consultar.click()
            print("Empresa regular.")
            botao_visualizar = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:btnVisualizar"]')))
            botao_visualizar.click()
            # Inicia a thread para executar a função de impressão com PyAutoGUI
            thread_impressao = threading.Thread(target=clicar_botao_impressao)
            thread_impressao.start()
            botao_imprimir = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:btImprimir4"]')))
            botao_imprimir.click()
            
            # Aguardar um pouco para garantir que a janela de impressão esteja aberta
            time.sleep(5)
            break
    else:
        print("A empresa não está regular perante o FGTS.")
        with open("empresas_irregulares.txt", "a") as arquivo:
            arquivo.write(f"CNPJ: {CNPJ} - Empresa não regular.\n")
        break
     
# Aguardar e fechar o navegador
time.sleep(10)
driver.quit()
print("Programa encerrado")
