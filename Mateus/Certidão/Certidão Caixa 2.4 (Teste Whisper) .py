from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
from openai import OpenAI
import sounddevice as sd
import numpy as np
import wavio
import whisper
import os

# Configurações do Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

# Configuração da OpenAI
client = OpenAI(api_key="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")

# Criar uma instância do modelo Whisper
model = whisper.load_model("base")  # Escolha o modelo apropriado: 'tiny', 'base', 'small', 'medium', 'large'


# Encontrar e preencher CNPJ
Acha_Cnpj = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtInscricao1"]'))
)
Acha_Cnpj.send_keys('15665964000126')

# Encontrar e selecionar UF
Acha_UF = driver.find_element(By.XPATH, '//*[@id="mainForm:uf"]')
select = Select(Acha_UF)
select.select_by_visible_text("DF")

# Função para gerar resposta com a OpenAI
def generate_answer(text):
    prompt = f"Transforme a descrição verbal {text} em código alfanumérico. Letras (ex: 'de' como 'd', 'ver ou ve' como 'v') e números, sem espaços ou símbolos. Diferencie maiúsculas de minúsculas."
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.3,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def record_audio(duration=5, filename='audio.wav', device=None):
    fs = 44100  # Taxa de amostragem
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, device=device)
    sd.wait()  # Aguarda a gravação terminar
    wavio.write(filename, myrecording, fs, sampwidth=2)

# Iniciar a gravação do áudio do captcha
print("Gravando o áudio do captcha...")
record_audio()

# Encontrar o elemento de áudio pelo seu XPath e clicar
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm"]/div[5]/div[2]/div[3]/a/img'))
)
element.click()

time.sleep(10)

# Caminho para o arquivo de áudio
path = os.getcwd()
filename = "\\audio.wav"

# Transcrever o áudio com Whisper
print("Processando o áudio com Whisper...")
result = model.transcribe(path + filename, language='pt', fp16=False)

# Acessar a transcrição do áudio
transcription = result["text"] if "text" in result else None

# Checar se a transcrição foi bem-sucedida
if result is not None and 'text' in result:
    question = result['text']
    print("Código recebido:", question)

    # Geração da resposta
    resposta_openai = generate_answer(question)
    print("Interpretação da OpenAI:", resposta_openai)

    # Preencher o captcha
    Acha_Captcha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtCaptcha"]'))
    )
    Acha_Captcha.send_keys(resposta_openai)
else:
    print("Não foi possível entender o áudio ou nenhuma entrada foi fornecida")

# Aguardar e fechar o navegador
time.sleep(5)
driver.quit()
print("Programa encerrado")
