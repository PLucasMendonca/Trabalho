from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import io

# Configuração do caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Inicialize o driver do Selenium
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Acesse o site
driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')

# Espere até que o CNPJ seja clicável e insira o número
Acha_Cnpj = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm:txtInscricao1"]'))
)
Acha_Cnpj.send_keys('15665964000126')

# Selecionar a UF
Acha_UF = driver.find_element(By.XPATH, '//*[@id="mainForm:uf"]')
select = Select(Acha_UF)
select.select_by_visible_text("DF")

# Aguarde para garantir que o CAPTCHA seja carregado
time.sleep(5)

# Encontre o elemento da imagem CAPTCHA pelo seu XPath e tire um screenshot
element = driver.find_element(By.XPATH, '//*[@id="captchaImg_N2"]')
png = element.screenshot_as_png  # Isso captura apenas o elemento da imagem

# Carregue essa imagem diretamente em um objeto Image do PIL
image = Image.open(io.BytesIO(png))

# Pré-processamento da imagem para melhorar a detecção de OCR
image = image.convert('L')  # Converter para escala de cinza
image = ImageOps.invert(image)  # Inverte a imagem
image = image.point(lambda x: 0 if x < 140 else 255)  # Aplica threshold
image = image.filter(ImageFilter.MedianFilter())  # Aplica filtro mediano para reduzir o ruído

# Tente remover qualquer ruído remanescente e melhorar a nitidez
image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

# Salvar a imagem processada temporariamente, se necessário
image.save('captcha_processado.png')

# Use o Tesseract para fazer OCR na imagem processada
text = pytesseract.image_to_string(image, lang='por', config='--psm 8')

print('Texto OCR:', text)

# Feche o navegador quando terminar
driver.quit()
