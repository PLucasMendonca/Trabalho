import pyautogui
import time
from encontrar_palavra import processar_imagem
from imagem_play import processar_imagem2
from audio_texto import capturar_e_transcrever_audio

# Pressionando Ctrl + Alt + C
pyautogui.hotkey('ctrl', 'alt', 'c')

time.sleep(5)  # Espera para garantir que o Chrome está aberto e pronto

# Assegurar que o foco está na barra de endereços (usando atalho de teclado)
pyautogui.hotkey('ctrl', 'l')

pyautogui.write('https://ww1.receita.fazenda.df.gov.br/cidadao/certidoes/Certidao')
pyautogui.press('enter')


time.sleep(2)

emissao = pyautogui.locateCenterOnScreen('emissaocertidao2.PNG', confidence=0.9)
pyautogui.click(emissao)

time.sleep(1)

cnpj = pyautogui.locateCenterOnScreen('PJ.PNG', confidence=0.8)
pyautogui.click(cnpj)

time.sleep(1)

cnpj = pyautogui.locateCenterOnScreen('CNPJ 2.PNG', confidence=0.8)
pyautogui.click(cnpj)

time.sleep(1)

pyautogui.write('15.665.964/0001-26')

time.sleep(1)

#Rolar a página para baixo usando a tecla "Page Down"
pyautogui.press('pagedown')

time.sleep(1)

coordenadas = processar_imagem()

if coordenadas:
    x, y, w, h = coordenadas
    pyautogui.click(x + w/2, y + h/2)
else:
    print("Palavra não encontrada.")

time.sleep(3)

ouvir = pyautogui.locateCenterOnScreen('ouvir captcha.PNG', confidence=0.8)


if ouvir is not None:
    pyautogui.click(ouvir)

    time.sleep(2)

    todas_coordenadas = processar_imagem2()
    coordenadas_segundo_play = None
    contador_play = 0

    for palavra, x, y, w, h in todas_coordenadas:
        if palavra.lower() == "play":
            contador_play += 1
            if contador_play == 2:
                coordenadas_segundo_play = (x, y, w, h)
                break

    if coordenadas_segundo_play:
        # Se a segunda ocorrência de 'play' for encontrada, use as coordenadas
        x, y, w, h = coordenadas_segundo_play
        pyautogui.click(x + w/2, y + h/2)
    else:
        print("A segunda ocorrência de 'play' não foi encontrada.")

    # Chamada da função para testar
    texto_transcrito = capturar_e_transcrever_audio()

    #ajustar o codigo para se o speed não reconhecer o audio ele repetir a ação e de apertar o botão novamente e rodar a gravação do audio de novo.

    
    texto = pyautogui.locateCenterOnScreen('localtexto.PNG', confidence=0.8)
    pyautogui.click(texto)

    pyautogui.write(texto_transcrito)
    
    time.sleep(3)
    
    verify = pyautogui.locateCenterOnScreen('verific.PNG', confidence=0.9)
    pyautogui.click(verify)

    time.sleep(2)
    
    gerarpdf = pyautogui.locateCenterOnScreen('gerarpdf.PNG', confidence=0.8)
    pyautogui.click(gerarpdf)

    time.sleep(3)

    imprimir = pyautogui.locateCenterOnScreen('imprimirfazenda.PNG', confidence=0.8)
    pyautogui.click(imprimir)

    time.sleep(2)

    pyautogui.write('20.721.183-0001-41')

    salvar = pyautogui.locateCenterOnScreen('salvarfazenda.PNG', confidence=0.8)
    pyautogui.click(salvar)

    time.sleep(2)

    botao_fechar = pyautogui.locateCenterOnScreen('fechar.PNG', confidence=0.8)
    pyautogui.click(botao_fechar)

else:

    gerarodf = pyautogui.locateCenterOnScreen('gerarpdf.PNG', confidence=0.8)
    pyautogui.click(gerarodf)

    time.sleep(2)

    imprimir = pyautogui.locateCenterOnScreen('imprimirfazenda.PNG', confidence=0.8)
    pyautogui.click(imprimir)

    pyautogui.write('20.721.183-0001-41')

    salvar = pyautogui.locateCenterOnScreen('salvarfazenda.PNG', confidence=0.8)
    pyautogui.click(salvar)

    time.sleep(1)

    botao_fechar = pyautogui.locateCenterOnScreen('fechar.PNG', confidence=0.8)
    pyautogui.click(botao_fechar)


# # Pressionando Ctrl + Alt + C
# pyautogui.hotkey('ctrl', 'f')

# time.sleep(1)

# pyautogui.write('o de certid')

# time.sleep(1)