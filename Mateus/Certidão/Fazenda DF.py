from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
from encontrar_palavra import processar_imagem

# Configurações do Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Acesse o site
driver.get('https://ww1.receita.fazenda.df.gov.br/cidadao/certidoes/Certidao')

CNPJ = '15665964000126'

# Digitar CNPJ
Abre_opcoes = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-expansion-panel-header-0"]/span[1]/mat-panel-title'))).click()
Acha_Cnpj = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-radio-8"]/label/div[2]'))).click()
Cnpj = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="documento"]')))
Cnpj.send_keys(CNPJ)

# Rolar a página para baixo usando a tecla "Page Down"
pyautogui.press('pagedown')

time.sleep(5)

coordenadas = processar_imagem()

if coordenadas:
    x, y, w, h = coordenadas
    pyautogui.click(x + w/2, y + h/2)
else:
    print("Palavra não encontrada.")

time.sleep(120)