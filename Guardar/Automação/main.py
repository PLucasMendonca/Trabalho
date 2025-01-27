import os
import time
import tkinter as tk
from tkinter import messagebox
from src.federal import iniciar_federal
from src.fgts import iniciar_fgts
from src.trabalhista import iniciar_trabalhista
from src.tcu import iniciar_tcu
from src.SINTEGRA.dif import iniciar_dif
from selenium.webdriver.chrome.service import Service

# Diretórios de download
DOWNLOAD_DIR = '/app/downloads'
HOST_DOWNLOAD_DIR = '/host_downloads'
service = Service('/usr/bin/chromedriver')

def rodar_automacao(tipo):
    """Chama a automação federal ou FGTS com o CNPJ fornecido."""
    cnpj = entry_cnpj.get().replace('.', '').replace('/', '').replace('-', '')
    if not validar_cnpj(cnpj):
        messagebox.showerror("Erro", "Por favor, insira um CNPJ válido.")
        return

    # Fecha a janela principal
    janela.destroy()

    try:
        if tipo == 'federal':
            iniciar_federal(cnpj)
        elif tipo == 'fgts':
            iniciar_fgts(cnpj)
        elif tipo == 'trabalhista':
            iniciar_trabalhista(cnpj)
        elif tipo == 'tcu':
            iniciar_tcu(cnpj)
        elif tipo == 'dif':
            iniciar_dif(cnpj)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar a automação: {e}")
    finally:
        criar_interface()

def validar_cnpj(cnpj):
    """Valida se o CNPJ informado possui 14 dígitos."""
    return len(cnpj) == 14

def get_download_file(filename):
    """Procura um arquivo nos diretórios de download."""
    # Procura primeiro no diretório de downloads do container
    container_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(container_path):
        return container_path
    
    # Se não encontrar, procura no diretório de downloads do host
    host_path = os.path.join(HOST_DOWNLOAD_DIR, filename)
    if os.path.exists(host_path):
        return host_path
    
    return None

def criar_interface():
    """Cria a interface gráfica para a automação."""
    global janela  # Declare a janela como global
    janela = tk.Tk()
    janela.title("Automação")
    janela.geometry("600x400")
    janela.configure(bg='#6F8B3D')  # Cor de fundo verde musgo
    janela.attributes('-topmost', True)

    label = tk.Label(janela, text="Digite o CNPJ para iniciar a automação", bg='#6F8B3D', fg='white')
    label.pack(pady=10)

    global entry_cnpj
    label_cnpj = tk.Label(janela, text="Digite o CNPJ:", bg='#6F8B3D', fg='white')
    label_cnpj.pack(pady=10)

    entry_cnpj = tk.Entry(janela, width=30)
    entry_cnpj.pack(pady=5)

    label_certificado = tk.Label(janela, text="Escolha o Certificado para ser baixado:", bg='#6F8B3D', fg='white')
    label_certificado.pack(pady=10)

    frame_botoes = tk.Frame(janela, bg='#6F8B3D')
    frame_botoes.pack(pady=10)

    # Botão para a automação Federal
    botao_federal = tk.Button(frame_botoes, text="Federal", command=lambda: rodar_automacao('federal'), bg='#4CAF50', fg='white', width=10)
    botao_federal.pack(side=tk.LEFT, padx=5)

    # Botão para a automação FGTS
    botao_fgts = tk.Button(frame_botoes, text="FGTS", command=lambda: rodar_automacao('fgts'), bg='#4CAF50', fg='white', width=10)
    botao_fgts.pack(side=tk.LEFT, padx=5)

    # Botão para a automação Trabalhista
    botao_trabalhista = tk.Button(frame_botoes, text="Trabalhista", command=lambda: rodar_automacao('trabalhista'), bg='#4CAF50', fg='white', width=10)
    botao_trabalhista.pack(side=tk.LEFT, padx=5)

    # Botão para a automação TCU
    botao_tcu = tk.Button(frame_botoes, text="TCU", command=lambda: rodar_automacao('tcu'), bg='#4CAF50', fg='white', width=10)
    botao_tcu.pack(side=tk.LEFT, padx=5)

    # Botão para a automação DIF
    botao_federal = tk.Button(frame_botoes, text="DIF", command=lambda: rodar_automacao('dif'), bg='#4CAF50', fg='white', width=10)
    botao_federal.pack(side=tk.LEFT, padx=5)

    janela.mainloop()

# Executa a criação da interface
if __name__ == "__main__":
    criar_interface()