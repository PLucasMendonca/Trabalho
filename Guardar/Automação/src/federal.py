import os
import glob
import datetime
import pyautogui
import time
import subprocess
import pygetwindow as gw

# Configurações
DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'
CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
TARGET_URL = 'https://ww1.receita.fazenda.df.gov.br/cidadao/certidoes/Certidao'
DOWNLOAD_FILE_PATTERN = "Federal.pdf"

def validar_cnpj(cnpj):
    """Valida se o CNPJ informado possui 14 dígitos."""
    cnpj = ''.join(filter(str.isdigit, cnpj))
    return len(cnpj) == 14

def abrir_chrome():
    """Abre o Google Chrome em modo convidado e maximiza a janela."""
    subprocess.Popen([CHROME_PATH, '--guest'])
    time.sleep(3)  # Aguarda o Chrome abrir
    chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]
    chrome_window.maximize()

def navegar_para_site(cnpj):
    """Navega para o site e preenche o CNPJ."""
    pyautogui.typewrite(TARGET_URL)
    pyautogui.press('enter')
    time.sleep(2)

    # Interações com a página
    pyautogui.click(x=553, y=427)  # Clique nos elementos necessários para emissão de certidão
    pyautogui.click(x=421, y=482)  # pessoa jurídica
    pyautogui.click(x=330, y=560)  # label para escrever
    time.sleep(1)

    pyautogui.typewrite(cnpj)  # escreve o CNPJ
    pyautogui.scroll(-500)  # rolagem da página
    time.sleep(5)

    # Preencher o restante do formulário
    pyautogui.click(x=1206, y=322)  # Gerar 
    time.sleep(4)
    pyautogui.click(x=1032, y=654)  # Imprimir
    time.sleep(1.5)
    pyautogui.click(x=180, y=458)  # clique para escrever
    time.sleep(1.5)
    pyautogui.typewrite('Federal')  # escreve 
    pyautogui.press('enter')
    time.sleep(2)

    # Fecha a aba do Chrome
    pyautogui.hotkey('ctrl', 'w')
    verificar_download(cnpj)

def iniciar_federal(cnpj):
    """Inicia o processo de automação com o CNPJ fornecido."""
    if not validar_cnpj(cnpj):
        raise ValueError("CNPJ inválido.")
    abrir_chrome()
    navegar_para_site(cnpj)

def verificar_download(cnpj):
    """Verifica se o arquivo foi baixado e o renomeia."""
    pasta_download = DOWNLOAD_DIR
    padrao_arquivo = os.path.join(pasta_download, DOWNLOAD_FILE_PATTERN)
    nova_data = datetime.datetime.now() + datetime.timedelta(days=90)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"FEDERAL {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        print("Checando se o arquivo foi baixado...")
        arquivo_encontrado = glob.glob(padrao_arquivo)

        if arquivo_encontrado:
            arquivo_download = arquivo_encontrado[0]
            print(f"Arquivo encontrado: {arquivo_download}")
            if not os.path.exists(arquivo_download + '.crdownload'):
                if not os.path.exists(nova_pasta):
                    os.makedirs(nova_pasta)

                if os.path.exists(novo_caminho):
                    os.remove(novo_caminho)

                time.sleep(2)
                try:
                    print(f"Tentando mover {arquivo_download} para {novo_caminho}")
                    os.rename(arquivo_download, novo_caminho)
                    print(f"Arquivo renomeado e movido para: {novo_caminho}")
                except Exception as e:
                    print(f"Ocorreu um erro ao mover o arquivo: {e}")
            else:
                print("O download ainda não foi concluído.")
                root.after(2000, checar_arquivo)
        else:
            print("Arquivo não encontrado.")
            root.after(2000, checar_arquivo)

    checar_arquivo()