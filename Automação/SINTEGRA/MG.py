import os
import glob
import datetime
import pyautogui
import time
import subprocess
import pygetwindow as gw
import tkinter as tk
from tkinter import messagebox

DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'  # Defina o diretório de downloads

def validar_cnpj(cnpj):
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Verifica se o CNPJ tem 14 dígitos
    return len(cnpj) == 14

def abrir_chrome(cnpj):
    # Abre o Google Chrome em modo convidado
    subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--guest'])

    # Aguarda o Chrome abrir
    time.sleep(3)

    # Obtém a janela do Chrome
    chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]

    # Maximiza a janela
    chrome_window.maximize()

    # Acessa o site desejado
    pyautogui.typewrite('https://ww1.receita.fazenda.df.gov.br/cidadao/certidoes/Certidao')
    pyautogui.press('enter')

    # Aguarda o site carregar
    time.sleep(2)

    # Interage com a página
    pyautogui.click(x=553, y=427)
    pyautogui.click(x=421, y=482) 
    pyautogui.click(x=330, y=560)
    time.sleep(2)

    # Escreve diretamente no campo de texto o CNPJ fornecido
    pyautogui.typewrite(cnpj)
    time.sleep(2)  
    pyautogui.scroll(-500)
    time.sleep(2)
    pyautogui.click(x=1206, y=322)
    time.sleep(5)
    pyautogui.click(x=1032, y=654)
    time.sleep(2)
    pyautogui.click(x=180, y=458)
    time.sleep(1)
    pyautogui.typewrite('Steven')
    time.sleep(1)
    pyautogui.click(x=494, y=533)
    time.sleep(2)

    # Aqui você pode chamar a função de verificação do download
    verificar_download(cnpj)

    # Fecha a aba do Chrome
    pyautogui.hotkey('ctrl', 'w')  # Fecha a aba atual do Chrome

def iniciar():
    global entry_cnpj  # Mudei para referenciar o Entry correto
    cnpj = entry_cnpj.get().replace('.', '').replace('/', '').replace('-', '')  # Use entry_cnpj aqui

    if not cnpj or len(cnpj) != 14:
        messagebox.showerror(
            "Erro", "Por favor, insira o CNPJ correto.")
        return
    abrir_chrome(cnpj)  # Chama a função para abrir o Chrome e preencher o CNPJ
    root.destroy()  # Fecha a janela Tkinter

def verificar_download(cnpj):
    pasta_download = DOWNLOAD_DIR
    data_atual = datetime.datetime.now().strftime("%d%m%y")
    padrao_arquivo = os.path.join(pasta_download, "Steven.pdf")
    nova_data = datetime.datetime.now() + datetime.timedelta(days=90)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"FEDERAL {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        print("Checando se o arquivo foi baixado...")  # Mensagem de depuração
        arquivo_encontrado = glob.glob(padrao_arquivo)
        if arquivo_encontrado:
            arquivo_download = arquivo_encontrado[0]
            print(f"Arquivo encontrado: {arquivo_download}")  # Mensagem de depuração
            if not os.path.exists(arquivo_download + '.crdownload'):
                messagebox.showinfo("Download Completo", "O download foi concluído com sucesso!")

                if not os.path.exists(nova_pasta):
                    os.makedirs(nova_pasta)

                if os.path.exists(novo_caminho):
                    os.remove(novo_caminho)
                time.sleep(2)
                try:
                    print(f"Tentando mover {arquivo_download} para {novo_caminho}")
                    os.rename(arquivo_download, novo_caminho)
                    messagebox.showinfo("Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
                    print(f"Arquivo movido para: {novo_caminho}")

                except Exception as e:
                    messagebox.showerror("Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
                    print(f"Erro ao mover o arquivo: {e}")

                root.destroy()
            else:
                print("O download ainda não foi concluído.")  # Mensagem de depuração
                root.after(2000, checar_arquivo)  # Verifica novamente após 2 segundos
        else:
            print("Arquivo não encontrado.")  # Mensagem de depuração
            root.after(2000, checar_arquivo)  # Verifica novamente após 2 segundos

    checar_arquivo()

# Criação da janela Tkinter
root = tk.Tk()
root.title("Preencher CNPJ")
root.geometry("300x150")

# Label e Entry para CNPJ
label_cnpj = tk.Label(root, text="Digite o CNPJ:")
label_cnpj.pack(pady=10)

entry_cnpj = tk.Entry(root)
entry_cnpj.pack(pady=5)

# Botão para abrir o Chrome e preencher o CNPJ
botao_abrir = tk.Button(root, text="Abrir Chrome", command=iniciar)
botao_abrir.pack(pady=20)

# Executa o loop principal da interface
root.mainloop()
