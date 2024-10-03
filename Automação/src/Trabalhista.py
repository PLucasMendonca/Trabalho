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

DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'
driver = None
wait = None
root = None

# Configurando o WebDriver do Chrome
service = Service(
    'C:/Users/Windows 11/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 10)


class AutomacaoTrabalhista:
    def __init__(self):
        self.root = None
        self.cnpj_entry = None
        self.captcha_entry = None
        self.cnpj_anterior = ""
        self.iniciar_interface_inicial()

    def iniciar_interface_inicial(self):
        self.root = tk.Tk()
        self.root.title("Iniciar Automação")

        # Label de instrução
        tk.Label(self.root, text="Clique abaixo para iniciar a automação.").pack(
            pady=10)

        # Botão para iniciar a automação
        iniciar_button = tk.Button(
            self.root, text="Iniciar Automação", command=self.iniciar_automacao)
        iniciar_button.pack(pady=20)
        self.root.mainloop()

    def iniciar_automacao(self):
        self.root.destroy()  # Fecha a primeira janela
        url = 'https://cndt-certidao.tst.jus.br/inicio.faces'
        driver.get(url)

        try:
            # Espera até que o botão de entrar no site esteja clicável
            entrar_site_emissao = wait.until(EC.element_to_be_clickable(
                (By.NAME, 'j_id_jsp_992698495_2:j_id_jsp_992698495_3')))
            entrar_site_emissao.click()

            # Exibe a segunda tela para inserir o CNPJ e o CAPTCHA
            self.criar_janela_cnpj_captcha()
        except NoSuchElementException:
            messagebox.showerror(
                "Erro", "Erro ao iniciar a automação. Verifique o site.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def criar_janela_cnpj_captcha(self):
        self.root = tk.Tk()
        self.root.title("Insira CNPJ e CAPTCHA")

        # Label e entrada para o CNPJ
        tk.Label(self.root, text="Insira o CNPJ (apenas números):").pack(pady=10)
        self.cnpj_entry = tk.Entry(self.root)
        self.cnpj_entry.pack(pady=10)

        # Label e entrada para o CAPTCHA
        tk.Label(self.root, text="Insira o CAPTCHA:").pack(pady=10)
        self.captcha_entry = tk.Entry(self.root)
        self.captcha_entry.pack(pady=10)

        # Botão para continuar a automação
        continuar_button = tk.Button(
            self.root, text="Continuar Automação", command=self.continuar_automacao)
        continuar_button.pack(pady=20)

        self.root.mainloop()

    def continuar_automacao(self):
        cnpj = self.cnpj_entry.get().replace('.', '').replace('/', '').replace('-', '')
        captcha = self.captcha_entry.get()
        self.cnpj_anterior = cnpj

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

        except NoSuchElementException:
            messagebox.showerror(
                "Erro", "Erro ao emitir certidão. Verifique os dados.")
        finally:
            self.checar_download(cnpj)

    def checar_download(self, cnpj):
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
                                        "O download foi concluído com sucesso!")

                    if not os.path.exists(nova_pasta):
                        os.makedirs(nova_pasta)

                    if os.path.exists(novo_caminho):
                        os.remove(novo_caminho)
                    time.sleep(2)
                    try:
                        logging.info(f"Tentando mover {
                                     arquivo_download} para {novo_caminho}")
                        os.rename(arquivo_download, novo_caminho)
                        messagebox.showinfo(
                            "Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
                        logging.info(f"Arquivo movido para: {novo_caminho}")

                    except Exception as e:
                        messagebox.showerror(
                            "Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
                        logging.error(f"Erro ao mover o arquivo: {e}")
                    self.root.destroy()
                    driver.quit()
            else:
                self.root.after(1000, checar_arquivo)

        checar_arquivo()


# Inicia a automação
AutomacaoTrabalhista()
