import pyautogui
import time

print("Você tem 5 segundos para posicionar o mouse sobre o texto 'Unidade compradora'")
time.sleep(5)

# Captura a posição atual do mouse
x, y = pyautogui.position()

# Captura uma região ao redor dessa posição
screenshot = pyautogui.screenshot(region=(x-100, y-10, 200, 20))
screenshot.save('unidade_compradora.png')
print("Imagem de referência salva como 'unidade_compradora.png'")
