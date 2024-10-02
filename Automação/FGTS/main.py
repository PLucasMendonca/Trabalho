import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
import glob
import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

"""
Caso de Leitura do PDF para validar qual nome será utilizado,
"""
DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'

def configurar_chrome():
    opcao_chrome = Options()
    opcao_chrome.add_experimental_option("prefs", {
        "printing.print_preview_sticky_settings.appState": json.dumps({
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }),
        "savefile.default_directory": DOWNLOAD_DIR,
        "savefile.overwrite_existing_files": True
    })
    opcao_chrome.add_argument('--kiosk-printing')  # Configura para evitar a janela de diálogo

    return opcao_chrome

service = Service(
    'C:/Users/Windows 11/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe')
opcao_chrome = configurar_chrome()
driver = webdriver.Chrome(service=service, options=opcao_chrome)
driver.maximize_window()

wait = WebDriverWait(driver, 10)


def criar_interface_inicial():
    global root
    root = tk.Tk()
    root.title("Iniciar Automação")

    # Label de instrução
    tk.Label(root, text="Clique abaixo para iniciar a automação.").pack(pady=10)

    # Botão para iniciar a automação
    iniciar_button = tk.Button(
        root, text="Iniciar Automação", command=iniciar_automacao)
    iniciar_button.pack(pady=20)

    root.mainloop()


def iniciar_automacao():
    root.destroy()  # Fecha a primeira janela
    url = 'https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf'
    driver.get(url)
    criar_janela_cnpj()


def criar_janela_cnpj():
    global root, cnpj_entry
    root = tk.Tk()
    root.title("Insira CNPJ")

    # Label e entrada para o CNPJ
    tk.Label(root, text="Insira o CNPJ (apenas números):").pack(pady=10)
    cnpj_entry = tk.Entry(root)
    cnpj_entry.pack(pady=10)

    mensagem = tk.Label(root, text="Após confirmação do captcha clique no botão a baixo", font=("Arial", 14))
    mensagem.pack(pady=20)
    mensagem3 = tk.Label(root, text="ATENÇÃO, o CAPTCHA atualiza a cada 30 segundos", font=("Arial", 14))
    mensagem3.pack(pady=20)

    # Botão para continuar a automação
    continuar_button = tk.Button(
        root, text="Continuar Automação", command=continuar_automacao)
    continuar_button.pack(pady=20)

    root.mainloop()



def continuar_automacao():
    global cnpj_entry

    cnpj = cnpj_entry.get().replace('.', '').replace('/', '').replace('-', '')

    if not cnpj or len(cnpj) != 14:
        messagebox.showerror(
            "Erro", "Por favor, insira o CNPJ correto.")
        return

    try:
        # Insere o CNPJ no campo correspondente
        cnpj_field = wait.until(EC.visibility_of_element_located(
            (By.ID, 'mainForm:txtInscricao1')))
        cnpj_field.clear()
        cnpj_field.send_keys(cnpj)

        # Clica no botão para emitir a certidão
        avancar_site = wait.until(EC.element_to_be_clickable(
            (By.ID, 'mainForm:btnConsultar')))
        avancar_site.click()
        time.sleep(4)

        avançar = wait.until(EC.element_to_be_clickable(
            (By.ID, 'mainForm:j_id51')))
        avançar.click()
        time.sleep(4)

        visualizar_certificado = wait.until(EC.element_to_be_clickable(
            (By.ID, 'mainForm:btnVisualizar')))
        visualizar_certificado.click()
        time.sleep(4)

        emitir_certificado = wait.until(EC.element_to_be_clickable(
            (By.ID, 'mainForm:btImprimir4')))
        emitir_certificado.click()
        time.sleep(4)        
        
        verificar_download(cnpj)
        
    except NoSuchElementException:
        messagebox.showerror(
            "Erro", "Erro ao emitir certidão. Verifique os dados.")

def verificar_download(cnpj):
    pasta_download = DOWNLOAD_DIR

    data_atual = datetime.datetime.now().strftime("%d%m%y")
    padrao_arquivo = os.path.join(pasta_download, f"Consulta Regularidade do Empregador.pdf")   
    nova_data = datetime.datetime.now() + datetime.timedelta(days=30)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"FGTS {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        arquivo_encontrado = glob.glob(padrao_arquivo)
        if arquivo_encontrado:
            arquivo_download = arquivo_encontrado[0]    
            if not os.path.exists(arquivo_download + '.crdownload'):
                messagebox.showinfo("Download Completo",
                                    "O download foi concluido com sucesso!")

                if not os.path.exists(nova_pasta):
                    os.makedirs(nova_pasta)

                if os.path.exists(novo_caminho):
                    os.remove(novo_caminho)
                time.sleep(2)
                try:
                    print(f"Tentando mover {arquivo_download} para {novo_caminho}")
                    os.rename(arquivo_download, novo_caminho)
                    messagebox.showinfo(
                        "Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
                    # Mensagem de depuração
                    print(f"Arquivo movido para: {novo_caminho}")

                except Exception as e:
                    messagebox.showerror(
                        "Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
                    # Mensagem de depuraçã
                    print(f"Erro ao mover o arquivo: {e}")
                root.destroy()
                driver.quit()
            else:
                root.after(2000,checar_arquivo)
    checar_arquivo()

# Inicia a interface inicial
criar_interface_inicial()