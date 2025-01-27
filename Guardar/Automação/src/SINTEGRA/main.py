import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from DF import continuar_automacao_df
from SP import continuar_automacao_sp
from MG import continuar_automacao_mg

# Definindo o diretório de download
DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'

def carregar_urls():
    with open('dif_links.json', 'r') as file:
        return json.load(file)


# Carrega as URLs do arquivo JSON
urls = carregar_urls()


def criar_janela_cnpj():
    global root, uf_combobox
    root = tk.Tk()
    root.title("Insira CNPJ")

    # Label e entrada para o CNPJ
    tk.Label(root, text="Selecione a UF").pack(pady=10)
    ufs = ["DF", "SP", "MG"]

    uf_combobox = ttk.Combobox(root, values=ufs)
    uf_combobox.pack(pady=10)

    # Botão para continuar a automação
    continuar_button = tk.Button(
        root, text="Continuar Automação", command=continuar_automacao)
    continuar_button.pack(pady=20)

    root.mainloop()


def continuar_automacao():
    global uf_combobox

    uf_selecionada = uf_combobox.get()

    if not uf_selecionada:
        messagebox.showerror("Erro", "Por favor, selecione uma UF.")
        return

    url_uf = urls.get(uf_selecionada)
    if not url_uf:
        messagebox.showerror(
            "Erro", f"Nenhuma URL encontrada para a UF: {uf_selecionada}")
        return

    root.destroy()  # Fecha a janela do Tkinter

        
        # Chama a função de automação apropriada com o driver
    if uf_selecionada == "DF":
        continuar_automacao_df(url_uf)
    elif uf_selecionada == "SP":
        continuar_automacao_sp(url_uf)
    elif uf_selecionada == "MG":
        continuar_automacao_mg()  # Apenas chama a automação para MG sem abrir o navegador

# Inicia a interface inicial
criar_janela_cnpj()
