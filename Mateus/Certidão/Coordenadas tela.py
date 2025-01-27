import pyautogui
import time

print("Press Ctrl-C to quit.")

try:
    while True:
        # Obtém e imprime as coordenadas do mouse em tempo real
        x, y = pyautogui.position()
        positionStr = f'X: {x} Y: {y}'
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nDone.')