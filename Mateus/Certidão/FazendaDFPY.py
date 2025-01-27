import pyautogui
import time

def clicar_botao_impressao():
    # Aguardar um momento para a janela de impressão abrir
    time.sleep(2)

    try:
        botao_impressao = pyautogui.locateCenterOnScreen('Imprimir 2.png', confidence=0.9)
        if botao_impressao:
            pyautogui.click(botao_impressao)
            print("Botão de impressão clicado.")
        else:
            print("Botão de impressão não encontrado.")
    except Exception as e:
        print(f"Erro ao localizar o botão de impressão: {e}")

    # Aguardar um momento para nova janela do Adobe abrir
    time.sleep(3)

    try:
        botao_salvar = pyautogui.locateCenterOnScreen('Salvar.png', confidence=0.8)
        if botao_salvar:
            pyautogui.click(botao_salvar)
            print("Botão de Salvar clicado.")
        else:
            print("Botão de Salvar não encontrado.")
    except Exception as e:
        print(f"Erro ao localizar o botão de Salvar: {e}")

clicar_botao_impressao()
