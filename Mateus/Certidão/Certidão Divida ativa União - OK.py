import pyautogui
import time

# Pressionando Ctrl + Alt + C
pyautogui.hotkey('ctrl', 'alt', 'c')

time.sleep(5)  # Espera para garantir que o Chrome está aberto e pronto

# Assegurar que o foco está na barra de endereços (usando atalho de teclado)
pyautogui.hotkey('ctrl', 'l')

pyautogui.write('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Emitir')
pyautogui.press('enter')


time.sleep(2)

# Rolar a página para baixo usando a tecla "Page Down"
pyautogui.press('pagedown')

time.sleep(1)

cnpj = pyautogui.locateCenterOnScreen('campocnpj.PNG', confidence=0.7)
pyautogui.click(cnpj)

time.sleep(1)

pyautogui.write('20.721.183/0001-41')
time.sleep(1)

botao_consultar = pyautogui.locateCenterOnScreen('Consultar 3.PNG', confidence=0.8)
pyautogui.click(botao_consultar)

time.sleep(2)

# Rolar a página para baixo usando a tecla "Page Down"
pyautogui.press('pagedown')

time.sleep(1)

# Pressionando Ctrl + Alt + C
pyautogui.hotkey('ctrl', 'f')

time.sleep(1)

pyautogui.write('Consulta de certid')

time.sleep(1)

botao_2via = pyautogui.locateCenterOnScreen('2.PNG', confidence=0.8)
pyautogui.click(botao_2via)

time.sleep(1)

# Rolar a página para baixo usando a tecla "Page Down"
pyautogui.press('pagedown')

time.sleep(1)

botao_consultar4 = pyautogui.locateCenterOnScreen('Consultar 3.PNG', confidence=0.8)
pyautogui.click(botao_consultar4)

time.sleep(1)

botao_pastinha = pyautogui.locateCenterOnScreen('Pastinha.PNG', confidence=0.9)
pyautogui.click(botao_pastinha)

time.sleep(1)

botao_fechar = pyautogui.locateCenterOnScreen('fechar.PNG', confidence=0.8)
pyautogui.click(botao_fechar)

