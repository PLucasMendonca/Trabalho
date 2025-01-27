from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Acesse o site
driver.get('https://certidoes-apf.apps.tcu.gov.br/')

# encontrar campo Cnpj
Acha_Cnpj = driver.find_element(By.ID, 'numero-cnpj')

time.sleep(1)

# Digitar Cnpj
Acha_Cnpj.send_keys('15.665.964/0001-26')

time.sleep(1)

# encontrar botão download
Acha_Botao = driver.find_element(By.ID, 'btn-emitir').click()

# Esperar pela geração da certidão (ajuste o tempo conforme necessário)
time.sleep(5)  # Espera explícita de 10 segundos


botao_baixar_pdf = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-emitir' and contains(text(), 'Baixar PDF')]"))
)

botao_baixar_pdf.click()

# Aguarda para garantir que o download começou
time.sleep(5)


