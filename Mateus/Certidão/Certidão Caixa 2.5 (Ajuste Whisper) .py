from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
from openai import OpenAI
import speech_recognition as sr
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
model = whisper.load_model("medium")

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
  
    prompt = f"Converta a descrição verbal em uma sequência alfanumérica de 5 caracteres. Siga estas regras: - 'número X' deve ser transcrito como o dígito 'X'. - 'letra maiúscula Y' ou 'letra minúscula y' deve ser transcrito como 'Y' ou 'y'. - Ignore palavras que não representem números ou letras. - Palavras comuns que soam como letras (ex: 'de' para 'D') devem ser tratadas como as letras correspondentes.  Descrição: {text} "
    

    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Configuração do reconhecedor de voz e do modelo Whisper
r = sr.Recognizer()
mic = sr.Microphone()

# Encontrar o elemento de áudio pelo seu XPath e clicar
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm"]/div[5]/div[2]/div[3]/a/img'))
)
element.click()

# Função para salvar o arquivo de áudio
def save_file(dados, filename='audio.wav'):
    with open(filename, "wb") as f:
        f.write(dados)

# Capturar áudio usando SpeechRecognition
with mic as fonte:
    print("Fale algo...")
    audio = r.listen(fonte)
    print("Processando o áudio...")

    # Salvar o áudio capturado
    save_file(audio.get_wav_data())

    # Transcrever o áudio com Whisper
    result = model.transcribe('audio.wav', language='pt', fp16=False)
    transcription = result["text"] if "text" in result else None

if transcription:
    print("Transcrição:", transcription)

    # Geração da resposta
    resposta_openai = generate_answer(transcription)
    print("Interpretação da OpenAI:", resposta_openai)

    # Preencher o captcha
    Acha_Captcha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtCaptcha"]'))
    )
    Acha_Captcha.send_keys(resposta_openai)

else:
    print("Áudio não compreendido.")

# Aguardar e fechar o navegador
time.sleep(5)
driver.quit()
print("Programa encerrado")
