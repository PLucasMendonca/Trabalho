import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
import glob
import sys
import datetime
from selenium.webdriver.support.ui import Select

DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'

def continuar_automacao_sp(driver):
    global root, cnpj_entry, captcha_entry
    root = tk.Tk()
    root.title("Insira CNPJ e CAPTCHA")

    wait = WebDriverWait(driver, 10)
    selecionar_cnpj = wait.until(EC.element_to_be_clickable(
        (By.ID, "ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_tipoFiltroDropDownList")))
    selecionar = Select(selecionar_cnpj)
    selecionar.select_by_visible_text("CNPJ")
    
    tk.Label(root, text="Insira o CNPJ (apenas números):").pack(pady=10)
    cnpj_entry = tk.Entry(root)
    cnpj_entry.pack(pady=10)

    # Label e entrada para o CAPTCHA
    tk.Label(root, text="Insira o CAPTCHA:").pack(pady=10)
    captcha_entry = tk.Entry(root)
    captcha_entry.pack(pady=10)

    # Botão para continuar a automação
    continuar_button = tk.Button(
    root, text="Continuar Automação", command=lambda: iniciar_automacao(driver, wait))
    continuar_button.pack(pady=20)

    root.mainloop()

def iniciar_automacao(driver, wait):
    global cnpj_entry, captcha_entry

    # Pega os valores inseridos pelo usuário
    cnpj = cnpj_entry.get().replace('.', '').replace('/', '').replace('-', '')
    captcha = captcha_entry.get()

    # Verifica se o CNPJ está correto
    if not cnpj or len(cnpj) != 14:
        messagebox.showerror("Erro", "Por favor, insira o CNPJ correto.")
        return

    try:       
        # Insere o CNPJ no campo correspondente
        cnpj_field = wait.until(EC.visibility_of_element_located(
            (By.ID, "ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_valorFiltroTextBox")))
        cnpj_field.clear()
        cnpj_field.send_keys(cnpj)

        # Insere o CAPTCHA
        captcha_field = driver.find_element(By.ID, 'ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_imagemDinamicaTextBox')
        captcha_field.clear()
        captcha_field.send_keys(captcha)

        # Clica no botão para consultar
        avancar_site = wait.until(EC.element_to_be_clickable(
            (By.ID,"ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_consultaPublicaButton")))
        avancar_site.click()
        time.sleep(4)

        driver.execute_script("window.print();")

        verificar_download(cnpj, driver)

    except NoSuchElementException:
        messagebox.showerror("Erro", "Erro ao emitir certidão. Verifique os dados.")

def verificar_download(cnpj, driver):
    pasta_download = DOWNLOAD_DIR

    data_atual = datetime.datetime.now().strftime("%d%m%y")
    padrao_arquivo = os.path.join(pasta_download, f"Consulta Pública ao Cadesp.pdf")
    nova_data = datetime.datetime.now() + datetime.timedelta(days=30)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"DIF {data_formatada}.pdf"
    nova_pasta = os.path.join(pasta_download, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        arquivo_encontrado = glob.glob(padrao_arquivo)
        if arquivo_encontrado:
            arquivo_download = arquivo_encontrado[0]
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
                driver.quit()
            else:
                root.after(2000, checar_arquivo)

    checar_arquivo()