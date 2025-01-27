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
import speech_recognition as sr

# Inicialize o reconhecedor de voz
recognizer = sr.Recognizer()

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

# Capturar o áudio do sistema
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Ouvindo o áudio...")
    audio = recognizer.listen(source)

# Tente transcrever o áudio usando a API do Google Web Speech
try:
    transcription = recognizer.recognize_google(audio, language='pt-BR')
    print("Transcrição do áudio: ", transcription)
except sr.UnknownValueError:
    print("Não foi possível entender o áudio")
except sr.RequestError as e:
    print("Erro na solicitação ao Google Web Speech API; {0}".format(e))

time.sleep(10)
# Feche o navegador quando terminar
driver.quit()

