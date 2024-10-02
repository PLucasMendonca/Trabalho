
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from tkinter import ttk
from DF import continuar_automacao_df
from SP import continuar_automacao_sp

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

def carregar_urls():
    with open('dif_links.json', 'r') as file:
        return json.load(file)
    
urls = carregar_urls()

def criar_janela_cnpj():
    global root, cnpj_entry, uf_combobox
    root = tk.Tk()
    root.title("Insira CNPJ")

    # Label e entrada para o CNPJ
    tk.Label(root, text="Selecione a UF").pack(pady=10)
    ufs = [
        "DF", "SP"
    ]

    uf_combobox = ttk.Combobox(root, values=ufs)
    uf_combobox.pack(pady=10)

    # Botão para continuar a automação
    continuar_button = tk.Button(
        root, text="Continuar Automação", command=continuar_automacao)
    continuar_button.pack(pady=20)

    root.mainloop()



def continuar_automacao():
    global cnpj_entry, uf_combobox

    uf_selecionada = uf_combobox.get()

    if not uf_selecionada:
        messagebox.showerror("Erro", "Por favor, seleciona uma UF.")

    try:

        url_uf = urls.get(uf_selecionada)
        if not url_uf:
            messagebox.showerror("Erro", f"Nenhuma URL encontrada para a UF: {uf_selecionada}")
            return
        
        root.destroy()

        driver.get(url_uf)

        if uf_selecionada == "DF":
            continuar_automacao_df(driver)
        elif uf_selecionada == "SP":
            continuar_automacao_sp(driver)

    except NoSuchElementException:
        messagebox.showerror(
            "Erro", "Erro ao emitir certidão. Verifique os dados.")
        
        
# Inicia a interface inicial
criar_janela_cnpj()