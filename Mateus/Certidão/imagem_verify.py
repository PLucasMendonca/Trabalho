import pytesseract
from PIL import ImageGrab, Image, ImageEnhance
import numpy as np
import cv2
import pyautogui

def processar_imagem2():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Captura apenas a região de interesse (você precisará ajustar as coordenadas)
    # Exemplo: screenshot = ImageGrab.grab(bbox=(x_inicial, y_inicial, x_final, y_final))
    screenshot = ImageGrab.grab()

    # Converter para um formato que o pytesseract possa ler e melhorar a imagem
    img_np = np.array(screenshot)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    
    # Aprimorar a imagem para o OCR
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza
    frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # Binarização

    # Usar OCR para obter dados de texto e caixas delimitadoras
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Whitelist de caracteres
    d = pytesseract.image_to_data(frame, config=custom_config, output_type=pytesseract.Output.DICT)

    palavra_procurada = "VERIFY"
    coordenadas_encontradas = []

    for i in range(len(d['text'])):
        if d['text'][i].upper() == palavra_procurada:
            x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
            coordenadas_encontradas.append((x, y, w, h))

    return coordenadas_encontradas


