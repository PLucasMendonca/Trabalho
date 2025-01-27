import pytesseract
from PIL import ImageGrab, Image
import cv2
import numpy as np

def processar_imagem():
    # Configuração do caminho do Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Captura de tela da área total (ajuste conforme necessário)
    screenshot = ImageGrab.grab()

    # Converter para um formato que o pytesseract possa ler
    img_np = np.array(screenshot)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # Usar OCR para obter dados de texto e caixas delimitadoras
    d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)

    # Palavra que você está procurando

    palavras_procuradas = ("Nao", "robot")
    # Percorrer os dados para encontrar a palavra
    for i in range(len(d['text'])):
            if d['text'][i].lower() in palavras_procuradas:
                # Coordenadas da palavra encontrada
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                palavra_encontrada = d['text'][i]
                print(f"Palavra encontrada: {palavra_encontrada}")
                print(f"Coordenadas: X: {x}, Y: {y}, Largura: {w}, Altura: {h}")
                return x, y, w, h
        
    print(d['text'])
    
    return None  # Retorne None se a palavra não for encontrad    
    
