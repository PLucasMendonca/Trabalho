import os
import time
import glob
import json
import datetime
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Diretório de download
DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'
captcha_root = None
wait = None
driver = None

def configurar_chrome():
    global driver, wait
    options = Options()
    options.add_experimental_option("prefs", {
        "printing.print_preview_sticky_settings.appState": json.dumps({
            "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }),
        "savefile.default_directory": DOWNLOAD_DIR,
        "savefile.overwrite_existing_files": True
    })
    options.add_argument('--kiosk-printing')

    service = Service('C:/Users/Windows 11/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

def iniciar_tcu(cnpj):
    """Inicia a automação ao clicar no botão."""
    configurar_chrome()
    url = 'https://contasirregulares.tcu.gov.br/ordsext/f?p=105:21:10861552622151::::P21_TIPO:CNPJ'
    driver.get(url)

    try:
        entrar_site_emissao = wait.until(EC.element_to_be_clickable((By.ID, 'P21_FINS_ELEITORAIS_0')))
        driver.execute_script("arguments[0].click();", entrar_site_emissao)
        criar_janela_captcha(cnpj)  # Passa o CNPJ
    except NoSuchElementException:
        messagebox.showerror("Erro", "Erro ao iniciar a automação. Verifique o site.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def criar_janela_captcha(cnpj):
    global captcha_root
    """Cria a janela para inserção do CAPTCHA e continua a automação."""
    captcha_root = tk.Tk()
    captcha_root.title("Insira CNPJ")

    mensagem = tk.Label(captcha_root, text="Por favor, faça o CAPTCHA abaixo e volte nesta tela\nClique no botão abaixo", font=("Arial", 14))
    mensagem.pack(pady=20)

    continuar_button = tk.Button(captcha_root, text="Continuar Automação", command=lambda: continuar_automacao(cnpj))
    continuar_button.pack(pady=20)

    captcha_root.mainloop()

def continuar_automacao(cnpj):
    global captcha_root
    """Continua a automação após a inserção do CNPJ."""
    try:
        preencher_cnpj(cnpj)
        emitir_certidao()
        baixar_certidao(cnpj)
    except NoSuchElementException:
        messagebox.showerror("Erro", "Erro ao emitir certidão. Verifique os dados.")
    finally:
        driver.quit()
        captcha_root.destroy()

def preencher_cnpj(cnpj):
    """Preenche o campo do CNPJ na página."""
    cnpj_field = wait.until(EC.visibility_of_element_located((By.ID, 'P21_CNPJ_CJI')))
    cnpj_field.clear()
    cnpj_field.send_keys(cnpj)

def emitir_certidao():
    """Emite a certidão clicando no botão correspondente."""
    emitir_certificado = wait.until(EC.element_to_be_clickable((By.ID, 'B55138095812122870')))
    emitir_certificado.click()
    time.sleep(3.5)

def baixar_certidao(cnpj):
    """Clica no link para baixar a certidão."""
    try:
        baixar_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'f?p=105:29:::NO::P29_COD_CONTROLE,P29_TIPO_CERTIDAO')]")))
        driver.execute_script("arguments[0].click();", baixar_link)
        time.sleep(5)  # Aumentar o tempo de espera para garantir que o download comece

        verificar_download(cnpj)
    except (NoSuchElementException, TimeoutException):
        messagebox.showerror("Erro", "Erro ao tentar baixar a certidão. O link pode não estar disponível.")
        driver.quit()

def verificar_download(cnpj):
    """Verifica se o download da certidão foi concluído, renomeia o arquivo e move para uma nova pasta."""
    pasta_download = DOWNLOAD_DIR
    padrao_arquivo = os.path.join(pasta_download, "Certidao *.pdf")
    nova_data = datetime.datetime.now() + datetime.timedelta(days=180)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"TCU {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)  # Nova pasta para o CNPJ
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    checar_arquivo(padrao_arquivo, novo_caminho, nova_pasta)

def checar_arquivo(padrao_arquivo, novo_caminho, nova_pasta):
    arquivo_encontrado = glob.glob(padrao_arquivo)
    if arquivo_encontrado:
        arquivo_download = arquivo_encontrado[0]  # Primeiro arquivo correspondente
        if not os.path.exists(arquivo_download + '.crdownload'):
            movendo_arquivo(arquivo_download, novo_caminho, nova_pasta)
        else:
            captcha_root.after(2000, checar_arquivo, padrao_arquivo, novo_caminho, nova_pasta)

def movendo_arquivo(arquivo_download, novo_caminho, nova_pasta):
    if not os.path.exists(nova_pasta):
        os.makedirs(nova_pasta)

    if os.path.exists(novo_caminho):
        os.remove(novo_caminho)

    time.sleep(2)  # Pode ser retirado ou reduzido com uma verificação mais robusta
    try:
        print(f"Tentando mover {arquivo_download} para {novo_caminho}")
        os.rename(arquivo_download, novo_caminho)
        messagebox.showinfo("Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
    except Exception as e:
        messagebox.showerror("Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
        print(f"Erro ao mover o arquivo: {e}")