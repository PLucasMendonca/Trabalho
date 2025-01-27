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


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

Acha_Cnpj = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtInscricao1"]'))
)

time.sleep(1)

# Digitar Cnpj
Acha_Cnpj.send_keys('15665964000126')

# encontrar UF
Acha_UF = driver.find_element(By.XPATH, '//*[@id="mainForm:uf"]')

# Criar uma instância da classe Select
select = Select(Acha_UF)

# Selecionar a opção por texto visível
select.select_by_visible_text("DF")

# Aguarda para garantir que o download começou
time.sleep(5)

# Encontre o elemento da audio pelo seu XPath e click um screenshot
element = driver.find_element(By.XPATH, '//*[@id="mainForm"]/div[5]/div[2]/div[3]/a/img').click()



# Feche o navegador quando terminar
driver.quit()