import pytesseract
from PIL import ImageGrab, Image
import cv2
import numpy as np
import pyautogui

def processar_imagem2():
    # Configuração do caminho do Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Captura de tela da área total (ajuste conforme necessário)
    screenshot = ImageGrab.grab()

    # Converter para um formato que o pytesseract possa ler
    img_np = np.array(screenshot)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # Usar OCR para obter dados de texto e caixas delimitadoras
    d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)

    # Palavras que você está procurando
    palavra_procurada = "play"
    coordenadas_encontradas = []

    # Percorrer os dados para encontrar a palavra
    for i in range(len(d['text'])):
        if d['text'][i].lower() == palavra_procurada:
            # Coordenadas da palavra encontrada
            x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
            print(f"Palavra encontrada: {d['text'][i]}")
            print(f"Coordenadas: X: {x}, Y: {y}, Largura: {w}, Altura: {h}")
            coordenadas_encontradas.append((d['text'][i], x, y, w, h))  # Inclua a palavra encontrada
    print(d['text'])
    return coordenadas_encontradas

