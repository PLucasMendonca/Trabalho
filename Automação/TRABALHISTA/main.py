import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
import sys
import datetime


DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'

# Configurando o WebDriver do Chrome
service = Service(
    'C:/Users/Windows 11/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

cnpj_anterior = ""

# Função para iniciar a automação


def iniciar_automacao():
    root.destroy()  # Fecha a primeira janela
    url = 'https://cndt-certidao.tst.jus.br/inicio.faces'
    driver.get(url)

    try:
        # Espera até que o botão de entrar no site esteja clicável
        entrar_site_emissao = wait.until(EC.element_to_be_clickable(
            (By.NAME, 'j_id_jsp_992698495_2:j_id_jsp_992698495_3')))
        entrar_site_emissao.click()

        # Exibe a segunda tela para inserir o CNPJ e o CAPTCHA
        criar_janela_cnpj_captcha()
    except NoSuchElementException:
        messagebox.showerror(
            "Erro", "Erro ao iniciar a automação. Verifique o site.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para criar a interface inicial que apenas inicia a automação


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


# Função para criar a janela de inserção do CNPJ e CAPTCHA
def criar_janela_cnpj_captcha():
    global root, cnpj_entry, captcha_entry
    root = tk.Tk()
    root.title("Insira CNPJ e CAPTCHA")

    # Label e entrada para o CNPJ
    tk.Label(root, text="Insira o CNPJ (apenas números):").pack(pady=10)
    cnpj_entry = tk.Entry(root)
    cnpj_entry.pack(pady=10)

    # Label e entrada para o CAPTCHA
    tk.Label(root, text="Insira o CAPTCHA:").pack(pady=10)
    captcha_entry = tk.Entry(root)
    captcha_entry.pack(pady=10)

    # Botão para continuar a automação
    continuar_button = tk.Button(
        root, text="Continuar Automação", command=continuar_automacao)
    continuar_button.pack(pady=20)

    root.mainloop()


# Função para continuar a automação após a entrada do CNPJ e CAPTCHA
def continuar_automacao():
    global cnpj_entry, captcha_entry, cnpj_anterior

    cnpj = cnpj_entry.get().replace('.', '').replace('/', '').replace('-', '')
    captcha = captcha_entry.get()
    cnpj_anterior = cnpj

    if not cnpj or len(cnpj) != 14 or not captcha:
        messagebox.showerror(
            "Erro", "Por favor, insira o CNPJ correto e o CAPTCHA.")
        return

    try:
        # Insere o CNPJ no campo correspondente
        cnpj_field = wait.until(EC.visibility_of_element_located(
            (By.ID, 'gerarCertidaoForm:cpfCnpj')))
        cnpj_field.clear()
        cnpj_field.send_keys(cnpj)

        # Insere o CAPTCHA no campo correspondente
        captcha_field = driver.find_element(By.ID, 'idCampoResposta')
        captcha_field.clear()
        captcha_field.send_keys(captcha)

        # Clica no botão para emitir a certidão
        emitir_certificado = wait.until(EC.element_to_be_clickable(
            (By.ID, 'gerarCertidaoForm:btnEmitirCertidao')))
        emitir_certificado.click()

        try:
            erro_captcha = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH,
                     "//div[@id='mensagens']//ul[@class='erros']//li[contains(text(), 'Código de validação inválido')]")
                )
            )
        except:
            pass
        try:
            erro_cnpj = driver.find_elements(
                By.ID, 'gerarCertidaoForm:areMensagemErro')
        except:
            pass

        if erro_captcha:
            messagebox.showerror("Erro", "CAPTCHA incorreto. Tente novamente.")
            root.destroy()
            segunda_tentativa()
        elif erro_cnpj:
            messagebox.showerror("Erro", "CNPJ inválido. Tente novamente.")
            root.destroy()
            segunda_tentativa()
        else:
            # Verifica se a certidão foi emitida com sucesso
            confirmacao_download = wait.until(EC.visibility_of_element_located(
                (By.ID, 'mensagemSucessoCertidaoEmitida')))

            if confirmacao_download.is_displayed():
                messagebox.showinfo("Sucesso", "Certidão emitida com sucesso!")
                verificar_download(cnpj)
            else:
                messagebox.showerror("Erro", "Erro ao emitir certidão.")
    except NoSuchElementException:
        messagebox.showerror(
            "Erro", "Erro ao emitir certidão. Verifique os dados.")
    finally:
        confirmacao_download = wait.until(EC.visibility_of_element_located(
                (By.ID, 'mensagemSucessoCertidaoEmitida')))
        if confirmacao_download.is_displayed():
            root.destroy()
            driver.quit()


def segunda_tentativa():
    global cnpj_anterior

    voltar = wait.until(EC.element_to_be_clickable(
        (By.NAME, 'gerarCertidaoForm:j_id_jsp_216541370_9')))
    voltar.click()

    time.sleep(2)
    cnpj_field = wait.until(EC.visibility_of_element_located(
        (By.ID, 'gerarCertidaoForm:cpfCnpj')))
    cnpj_field.clear()
    cnpj_field.send_keys(cnpj_anterior)

    root = tk.Tk()
    root.title("Insira o CAPTCHA")

    continuar_button = tk.Button(
        root, text="Continuar Automação", command=continuar_automacao)
    continuar_button.pack(pady=20)


def continuacao_tentativa():
    global cnpj_anterior
    root.destroy()

    emitir_certificado = wait.until(EC.element_to_be_clickable(
        (By.ID, 'gerarCertidaoForm:btnEmitirCertidao')))
    emitir_certificado.click()
    verificar_download(cnpj_anterior)


def verificar_download(cnpj):
    pasta_download = DOWNLOAD_DIR
    arquivo_download = os.path.join(pasta_download, f"certidao_{cnpj}.pdf")

    nova_data = datetime.datetime.now() + datetime.timedelta(days=180)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"TRABALHISTA {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        if os.path.exists(arquivo_download):
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
            root.after(1000, checar_arquivo)

    checar_arquivo()


# Inicia a interface inicial
criar_interface_inicial()
