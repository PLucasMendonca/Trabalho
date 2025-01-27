import os
import glob
import datetime
import pyautogui
import time
import subprocess
import pygetwindow as gw
import pyperclip
from tkinter import messagebox

DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'

root = None
def continuar_automacao_mg(cnpj):
    # Abre o Google Chrome em modo convidado
    subprocess.Popen(
        ['C:/Program Files/Google/Chrome/Application/chrome.exe', '--guest'])
    time.sleep(3)
    chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]
    chrome_window.maximize()

    url = 'https://www2.fazenda.mg.gov.br/sol/ctrl/SOL/CDT/SERVICO_829?ACAO=INICIAR#'
    pyperclip.copy(url)

    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

    time.sleep(6)

    # Interage com a página
    pyautogui.click(x=494, y=319) #Tipo de Identificação 
    time.sleep(2)
    pyautogui.click(x=430, y=380) #seleciona CNPJ
    time.sleep(1.5)
    pyautogui.click(x=426, y=336) #Identificação
    time.sleep(1.5)
    # Escreve diretamente no campo de texto o CNPJ fornecido
    pyautogui.typewrite(cnpj)
    time.sleep(1.5)
    pyautogui.click(x=883, y=450) #Confirmar
    time.sleep(3)
    pyautogui.click(x=870, y=616) #Botão para confirmar
    time.sleep(8)
    pyautogui.click(x=494, y=331) #botão de Imprimir Certidão 
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(2.5)
    pyautogui.press('enter')

    pyautogui.click(x=494, y=457) #Nome do Arquivo
    time.sleep(1.5)

    pyautogui.typewrite('DIF_MG')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(1.5)

    verificar_download(cnpj)

    # Fecha a aba do Chrome
    pyautogui.hotkey('ctrl', 'w')
    pyautogui.hotkey('ctrl', 'w')


def verificar_download(cnpj):
    pasta_download = DOWNLOAD_DIR
    data_atual = datetime.datetime.now().strftime("%d%m%y")
    padrao_arquivo = os.path.join(pasta_download, "DIF_MG.pdf")
    nova_data = datetime.datetime.now() + datetime.timedelta(days=90)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"DIF {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        print("Checando se o arquivo foi baixado...")
        arquivo_encontrado = glob.glob(padrao_arquivo)
        if arquivo_encontrado:
            arquivo_download = arquivo_encontrado[0]
            if not os.path.exists(arquivo_download + '.crdownload'):
                
                if not os.path.exists(nova_pasta):
                    os.makedirs(nova_pasta)

                if os.path.exists(novo_caminho):
                    os.remove(novo_caminho)
                time.sleep(2)
                try:
                    print(f"Tentando mover {
                          arquivo_download} para {novo_caminho}")
                    os.rename(arquivo_download, novo_caminho)
                    messagebox.showinfo(
                        "Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
                    print(f"Arquivo movido para: {novo_caminho}")

                except Exception as e:
                    messagebox.showerror(
                        "Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
                    print(f"Erro ao mover o arquivo: {e}")

            else:
                root.after(2000, checar_arquivo)
        else:
            root.after(2000, checar_arquivo)

    checar_arquivo()