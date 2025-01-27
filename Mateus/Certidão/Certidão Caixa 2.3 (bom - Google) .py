from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import speech_recognition as sr
import time
from openai import OpenAI

# Configurações do Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

# Configuração da OpenAI
client = OpenAI(api_key="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")

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

def processar_descricao(texto):
    partes = texto.split(", ")
    descricao_processada = ", ".join([parte + "," if "letra" in parte or "número" in parte else parte for parte in partes])
    return descricao_processada

# Função para gerar resposta com a OpenAI
def generate_answer(text):
    descricao_processada = processar_descricao(text)
    prompt = f"Converta a seguinte descrição verbal em um código alfanumérico de 5 caracteres. Siga estas orientações: - 'letra maiúscula [Letra]' deve ser transcrita como a letra maiúscula correspondente. - 'letra minúscula [letra]' deve ser transcrita como a letra minúscula correspondente. - 'número [X]' deve ser transcrito como o dígito correspondente. - Palavras comuns que soam como letras ou números devem ser interpretadas como tais (ex: 'de' para 'D', 'eme' para 'M'). - Cada elemento da descrição (letra ou número) corresponde a apenas um caractere no código final. Descrição: {text}"
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

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
    audio = r.listen(fonte, timeout=20, phrase_time_limit=20)
    print("Processando o áudio...")

# Reconhecimento de voz com Google
try:
    question = r.recognize_google(audio, language="pt-BR")
except sr.UnknownValueError:
    print("Google Speech Recognition não entendeu o áudio")
except sr.RequestError as e:
    print(f"Erro na solicitação ao Google Speech Recognition; {e}")

# Processamento com a OpenAI
if question:
    print("Código recebido:", question)
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
