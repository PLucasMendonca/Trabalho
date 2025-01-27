from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import speech_recognition as sr  # pip install SpeechRecognition
import os
from openai import OpenAI

# Configurações do Chrome
chrome_options = Options()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

Acha_Cnpj = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtInscricao1"]'))
)

time.sleep(1)

# Digitar CNPJ
Acha_Cnpj.send_keys('15665964000126')

# Encontrar UF
Acha_UF = driver.find_element(By.XPATH, '//*[@id="mainForm:uf"]')

# Criar uma instância da classe Select
select = Select(Acha_UF)

# Selecionar a opção por texto visível
select.select_by_visible_text("DF")

# Aguardar para garantir que o download começou
time.sleep(5)

# Encontrar o elemento de áudio pelo seu XPath e clicar
element = driver.find_element(By.XPATH, '//*[@id="mainForm"]/div[5]/div[2]/div[3]/a/img').click()


# Configuração da OpenAI
client = OpenAI(
    api_key="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",
)

def generate_answer(text):
    prompt = f"A informação que estou lhe passando é um código de letras e números: {text}. Quero que interprete ele e me informe o código somente nas letras e dos números."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()

print("Reconhecimento de voz ativado com Google Speech Recognition. Fale o código...")

# Capturar áudio
with mic as fonte:
    r.adjust_for_ambient_noise(fonte)
    audio = r.listen(fonte)
    print("Processando o áudio...")

    # Reconhecimento de voz com Google
    try:
        question = r.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        print("Google Speech Recognition não entendeu o áudio")
    except sr.RequestError as e:
        print(f"Erro na solicitação ao Google Speech Recognition; {e}")

if question:
    print("Código recebido:", question)
    # Enviar para a OpenAI e obter resposta
    resposta_openai = generate_answer(question)
    print("Interpretação da OpenAI:", resposta_openai)
else:
    print("Não foi possível entender o áudio ou nenhuma entrada foi fornecida")

print("Programa encerrado")


time.sleep(10)
# Feche o navegador quando terminar

# Acha campo para digitar capctha
Acha_Capctha = driver.find_element(By.XPATH, '//*[@id="mainForm:txtCaptcha"]')
Acha_Capctha.send_keys(f'{resposta_openai}')

time.sleep(10)

driver.quit()


