import os
import time
import json
import glob
import datetime
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'
driver = None
wait = None
root = None

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

def iniciar_fgts(cnpj):
    configurar_chrome()
    iniciar_automacao(cnpj)

def iniciar_automacao(cnpj):
    global driver
    driver.get('https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    criar_janela_captcha(cnpj)

def criar_janela_captcha(cnpj):
    global root
    root = tk.Tk()
    root.title("Insira CAPTCHA")

    tk.Label(root, text="Insira o CAPTCHA ").pack(pady=10)
    captcha_entry = tk.Entry(root)
    captcha_entry.pack(pady=10)

    mensagem = tk.Label(root, text="Após confirmação do captcha clique no botão abaixo", font=("Arial", 14))
    mensagem.pack(pady=20)
    mensagem3 = tk.Label(root, text="ATENÇÃO: o CAPTCHA atualiza a cada 30 segundos", font=("Arial", 14))
    mensagem3.pack(pady=20)

    continuar_button = tk.Button(root, text="Continuar Automação", command=lambda: continuar_automacao(cnpj, captcha_entry.get()))
    continuar_button.pack(pady=20)

    root.mainloop()

def continuar_automacao(cnpj, captcha):
    global root
    try:
        insere_cnpj(cnpj)
        resolve_captcha(captcha)
        emitir_certidao()
        verificar_download(cnpj)
    except NoSuchElementException as e:
        messagebox.showerror("Erro", f"Erro ao emitir certidão: {str(e)}")
    except TimeoutException:
        messagebox.showerror("Erro", "O tempo de espera para a ação foi excedido.")
    finally:
        # Fecha a janela e o driver
        root.destroy()  # Fechar a janela do Tkinter
        driver.quit()   # Fechar o driver do Selenium

def insere_cnpj(cnpj):
    cnpj_field = wait.until(EC.visibility_of_element_located((By.ID, 'mainForm:txtInscricao1')))
    cnpj_field.clear()
    cnpj_field.send_keys(cnpj)

def resolve_captcha(captcha):
    captcha_field = wait.until(EC.visibility_of_element_located((By.ID, 'mainForm:txtCaptcha')))
    captcha_field.clear()
    captcha_field.send_keys(captcha)

    avancar_site = wait.until(EC.element_to_be_clickable((By.ID, 'mainForm:btnConsultar')))
    avancar_site.click()
    time.sleep(1)

def emitir_certidao():
    avancar = wait.until(EC.element_to_be_clickable((By.ID, 'mainForm:j_id51')))
    avancar.click()
    time.sleep(1)

    visualizar_certificado = wait.until(EC.element_to_be_clickable((By.ID, 'mainForm:btnVisualizar')))
    visualizar_certificado.click()
    time.sleep(1)

    emitir_certificado = wait.until(EC.element_to_be_clickable((By.ID, 'mainForm:btImprimir4')))
    emitir_certificado.click()
    time.sleep(1)

def verificar_download(cnpj):
    pasta_download = DOWNLOAD_DIR
    data_atual = datetime.datetime.now().strftime("%d%m%y")
    padrao_arquivo = os.path.join(pasta_download, "Consulta Regularidade do Empregador.pdf")
    nova_data = datetime.datetime.now() + datetime.timedelta(days=30)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"FGTS {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    checar_arquivo(padrao_arquivo, novo_caminho, nova_pasta)

def checar_arquivo(padrao_arquivo, novo_caminho, nova_pasta):
    arquivo_encontrado = glob.glob(padrao_arquivo)
    if arquivo_encontrado:
        arquivo_download = arquivo_encontrado[0]
        if not os.path.exists(arquivo_download + '.crdownload'):
            movendo_arquivo(arquivo_download, novo_caminho, nova_pasta)
        else:
            root.after(2000, checar_arquivo, padrao_arquivo, novo_caminho, nova_pasta)

def movendo_arquivo(arquivo_download, novo_caminho, nova_pasta):
    if not os.path.exists(nova_pasta):
        os.makedirs(nova_pasta)

    if os.path.exists(novo_caminho):
        os.remove(novo_caminho)

    time.sleep(2)
    try:
        print(f"Tentando mover {arquivo_download} para {novo_caminho}")
        os.rename(arquivo_download, novo_caminho)
        messagebox.showinfo("Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
    except Exception as e:
        messagebox.showerror("Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
        print(f"Erro ao mover o arquivo: {e}")