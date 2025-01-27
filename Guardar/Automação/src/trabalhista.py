import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
import datetime

# Diretório de download
DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'

# Configurando o WebDriver do Chrome
service = Service('C:/Users/Windows 11/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

cnpj_anterior = ""

def iniciar_trabalhista(cnpj):
    """Inicia a automação e abre o site"""
    url = 'https://cndt-certidao.tst.jus.br/inicio.faces'
    driver.get(url)

    try:
        # Espera até que o botão de entrar no site esteja clicável
        entrar_site_emissao = wait.until(EC.element_to_be_clickable(
            (By.NAME, 'j_id_jsp_992698495_2:j_id_jsp_992698495_3')))
        entrar_site_emissao.click()

        criar_janela_cnpj_captcha(cnpj)
    except NoSuchElementException:
        messagebox.showerror("Erro", "Erro ao iniciar a automação. Verifique o site.")
        logging.error("Erro ao iniciar a automação: elemento não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        logging.error(f"Ocorreu um erro ao iniciar a automação: {e}")

def criar_janela_cnpj_captcha(cnpj):
    """Cria a segunda tela para inserir CNPJ e CAPTCHA"""
    root = tk.Tk()
    root.title("Insira o CAPTCHA")
    root.geometry(f"200x200+400+100")

    # Label e entrada para o CAPTCHA
    tk.Label(root, text="Insira o CAPTCHA:").pack(pady=10)
    captcha_entry = tk.Entry(root)
    captcha_entry.pack(pady=10)

    # Botão para continuar a automação
    continuar_button = tk.Button(root, text="Continuar Automação", command=lambda: continuar_automacao(root, cnpj, captcha_entry))
    continuar_button.pack(pady=20)
    

    root.mainloop()

def continuar_automacao(root, cnpj, captcha_entry):
    """Continua a automação inserindo o CNPJ e o CAPTCHA no site"""
    global cnpj_anterior
    captcha = captcha_entry.get()
    cnpj_anterior = cnpj

    try:
        # Insere o CNPJ no campo correspondente
        cnpj_field = wait.until(EC.visibility_of_element_located((By.ID, 'gerarCertidaoForm:cpfCnpj')))
        cnpj_field.clear()
        cnpj_field.send_keys(cnpj)

        # Insere o CAPTCHA no campo correspondente
        captcha_field = driver.find_element(By.ID, 'idCampoResposta')
        captcha_field.clear()
        captcha_field.send_keys(captcha)

        # Clica no botão para emitir a certidão
        emitir_certificado = wait.until(EC.element_to_be_clickable((By.ID, 'gerarCertidaoForm:btnEmitirCertidao')))
        emitir_certificado.click()

    except NoSuchElementException:
        messagebox.showerror("Erro", "Erro ao emitir certidão. Verifique os dados.")
        logging.error("Erro ao emitir a certidão: elemento não encontrado.")
    finally:
        verificar_download(cnpj, root)


def verificar_download(cnpj, root):
    """ Checa se o arquivo foi baixado e realiza o renomeio e movimentação """
    pasta_download = DOWNLOAD_DIR
    arquivo_download = os.path.join(pasta_download, f"certidao_{cnpj}.pdf")
    time.sleep(4)
    nova_data = datetime.datetime.now() + datetime.timedelta(days=180)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"TRABALHISTA {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        if os.path.exists(arquivo_download):
            if not os.path.exists(arquivo_download + '.crdownload'):
                driver.quit()
                root.destroy()
                if not os.path.exists(nova_pasta):
                    os.makedirs(nova_pasta)

                if os.path.exists(novo_caminho):
                    os.remove(novo_caminho)

                time.sleep(2)
                try:
                    logging.info(f"Movendo {arquivo_download} para {novo_caminho}")
                    os.rename(arquivo_download, novo_caminho)
                    messagebox.showinfo("Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
                    logging.info(f"Arquivo movido para: {novo_caminho}")
                except Exception as e:
                    messagebox.showerror("Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
                    logging.error(f"Erro ao mover o arquivo: {e}")
            
        else:
            print('Erro, não foi achado o arquivo')

    checar_arquivo()
