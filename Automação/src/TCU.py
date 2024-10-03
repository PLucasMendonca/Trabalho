import os
import time
import glob
import datetime
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

DOWNLOAD_DIR = 'C:/Users/Windows 11/Downloads'
service = Service('C:/Users/Windows 11/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
root = None

def criar_interface_inicial():
    """Cria a interface inicial da aplicação."""
    global root
    root = tk.Tk()
    root.title("Iniciar Automação")

    tk.Label(root, text="Clique abaixo para iniciar a automação.").pack(pady=10)
    iniciar_button = tk.Button(root, text="Iniciar Automação", command=iniciar_automacao)
    iniciar_button.pack(pady=20)
    root.mainloop()

def iniciar_automacao():
    """Inicia a automação ao clicar no botão."""
    global root
    root.destroy()
    url = 'https://contasirregulares.tcu.gov.br/ordsext/f?p=105:21:10861552622151::::P21_TIPO:CNPJ'
    driver.get(url)

    try:
        entrar_site_emissao = wait.until(EC.element_to_be_clickable((By.ID, 'P21_FINS_ELEITORAIS_0')))
        driver.execute_script("arguments[0].click();", entrar_site_emissao)
        criar_janela_cnpj()
    except NoSuchElementException:
        mostrar_erro("Erro ao iniciar a automação. Verifique o site.")
    except Exception as e:
        mostrar_erro(f"Ocorreu um erro: {e}")

def criar_janela_cnpj():
    """Cria a janela para inserção do CNPJ."""
    cnpj_root = tk.Tk()
    cnpj_root.title("Insira CNPJ")

    tk.Label(cnpj_root, text="Insira o CNPJ (apenas números):").pack(pady=10)
    cnpj_entry = tk.Entry(cnpj_root)
    cnpj_entry.pack(pady=10)

    mensagem = tk.Label(cnpj_root, text="Após confirmação do captcha clique no botão abaixo", font=("Arial", 14))
    mensagem.pack(pady=20)

    continuar_button = tk.Button(cnpj_root, text="Continuar Automação", command=lambda: continuar_automacao(cnpj_entry, cnpj_root))
    continuar_button.pack(pady=20)

    cnpj_root.mainloop()

def continuar_automacao(cnpj_entry, cnpj_root):
    """Continua a automação após a inserção do CNPJ."""
    cnpj = cnpj_entry.get().replace('.', '').replace('/', '').replace('-', '')

    if not cnpj or len(cnpj) != 14:
        mostrar_erro("Por favor, insira o CNPJ correto.")
        return

    try:
        preencher_cnpj(cnpj)
        emitir_certidao()
        baixar_certidao()
        # Passa a referência da janela CNPJ para a função verificar_download
        root.after(5000, verificar_download, cnpj, cnpj_root)
    except NoSuchElementException:
        mostrar_erro("Erro ao emitir certidão. Verifique os dados.")

def preencher_cnpj(cnpj):
    """Preenche o campo do CNPJ na página."""
    cnpj_field = wait.until(EC.visibility_of_element_located((By.ID, 'P21_CNPJ_CJI')))
    cnpj_field.clear()
    cnpj_field.send_keys(cnpj)

def emitir_certidao():
    """Emite a certidão clicando no botão correspondente."""
    emitir_certificado = wait.until(EC.element_to_be_clickable((By.ID, 'B55138095812122870')))
    emitir_certificado.click()
    time.sleep(4)  # Aguardar a página carregar

def baixar_certidao():
    """Clica no link para baixar a certidão."""
    try:
        baixar_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'f?p=105:29:::NO::P29_COD_CONTROLE,P29_TIPO_CERTIDAO')]")))

        driver.execute_script("arguments[0].click();", baixar_link)
        time.sleep(2)  # Espera o download começar
    except (NoSuchElementException, TimeoutException):
        mostrar_erro("Erro ao tentar baixar a certidão. O link pode não estar disponível.")

def verificar_download(cnpj, cnpj_root):
    """Verifica se o download da certidão foi concluído e renomeia o arquivo."""
    data_atual = datetime.datetime.now().strftime("%d%m%y")
    padrao_arquivo = os.path.join(DOWNLOAD_DIR, f"Certidao *{data_atual}*.pdf")
    nova_data = datetime.datetime.now() + datetime.timedelta(days=30)
    data_formatada = nova_data.strftime("%d.%m.%Y")
    novo_nome = f"TCU {data_formatada}.pdf"
    nova_pasta = os.path.join(DOWNLOAD_DIR, cnpj)
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    def checar_arquivo():
        arquivo_encontrado = glob.glob(padrao_arquivo)
        if arquivo_encontrado:
            arquivo_download = arquivo_encontrado[0]    
            if not os.path.exists(arquivo_download + '.crdownload'):
                if not os.path.exists(nova_pasta):
                    os.makedirs(nova_pasta)

                if os.path.exists(novo_caminho):
                    os.remove(novo_caminho)
                time.sleep(2)

                try:
                    os.rename(arquivo_download, novo_caminho)
                    messagebox.showinfo("Arquivo Renomeado", f"Arquivo renomeado e movido para: {novo_caminho}")
                except Exception as e:
                    mostrar_erro(f"Erro ao mover o arquivo: {e}")

                # Fecha a janela do Tkinter e o driver do navegador aqui, após o download
                cnpj_root.destroy()  # Fecha a janela CNPJ
                driver.quit()
            else:
                # Se o download não estiver completo, chama a função novamente após 2 segundos
                root.after(2000, checar_arquivo)
        else:
            # Se nenhum arquivo foi encontrado, verifica novamente após 2 segundos
            root.after(2000, checar_arquivo)
    checar_arquivo()

def mostrar_erro(mensagem):
    messagebox.showerror("Erro", mensagem)

criar_interface_inicial()