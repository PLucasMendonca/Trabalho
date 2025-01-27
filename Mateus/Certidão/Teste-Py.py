import pyautogui
import time


pyautogui.moveTo(100, 100)
# Aguarde um momento para a janela de impressão abrir
time.sleep(5)

# Localize e clique no botão de impressão
botao_impressao = pyautogui.locateCenterOnScreen('Imprimir 2.png', confidence=0.9)
if botao_impressao:
    pyautogui.click(botao_impressao)
else:
    print("Botão de impressão não encontrado")