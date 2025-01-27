import pyautogui
import time

print("Você tem 5 segundos para posicionar o mouse sobre o botão de tarefas (ícone)")
time.sleep(5)

# Captura a posição atual do mouse
x, y = pyautogui.position()

# Captura uma região ao redor dessa posição
screenshot = pyautogui.screenshot(region=(x-20, y-20, 40, 40))
screenshot.save('botao_tarefas.png')
print("Imagem de referência salva como 'botao_tarefas.png'")
