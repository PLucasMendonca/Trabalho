from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import re
from selenium.webdriver.common.action_chains import ActionChains
import time
from tkinter import Tk, Toplevel, Label, Entry, Button, Listbox, StringVar, Scrollbar, messagebox

def iniciar_driver():
    """Inicia o driver do Selenium com o perfil do Chrome especificado."""
    caminho_perfil = "C:/Users/Windows 11/AppData/Local/Google/Chrome/User Data"
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={caminho_perfil}")
    chrome_options.add_argument("--profile-directory=Profile 3")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def validar_telefone(telefone):
    """Valida se o telefone contém apenas números e tem o DDD."""
    return re.fullmatch(r'\d{10,11}', telefone) is not None

def adicionar_numero_google(nome, telefone):
    """Funcionalidade para adicionar o nome e telefone no Google Contacts."""
    driver = iniciar_driver()
    try:
        driver.get("https://contacts.google.com/new")
        campo_first_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='First name']"))
        )
        campo_first_name.send_keys(nome)
        
        campo_phone = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Phone']"))
        )
        campo_phone.send_keys(telefone)
        
        botao_save = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Save']"))
        )
        botao_save.click()
        
        messagebox.showinfo("Número Adicionado", "Número adicionado ao Google Contacts com sucesso!")
    except (TimeoutException, WebDriverException) as e:
        messagebox.showerror("Erro", f"Erro ao adicionar número: {e}")
    finally:
        driver.quit()

def exibir_janela_adicionar_numero():
    """Exibe uma nova janela para entrada de nome e número."""
    janela_adicionar = Toplevel()
    janela_adicionar.title("Adicionar Número")

    Label(janela_adicionar, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
    campo_nome = Entry(janela_adicionar)
    campo_nome.grid(row=0, column=1, padx=10, pady=5)

    Label(janela_adicionar, text="Telefone (DDD + Número):").grid(row=1, column=0, padx=10, pady=5)
    campo_telefone = Entry(janela_adicionar)
    campo_telefone.grid(row=1, column=1, padx=10, pady=5)

    def continuar():
        nome = campo_nome.get()
        telefone = campo_telefone.get()
        if not nome or not validar_telefone(telefone):
            messagebox.showerror("Erro de Validação", "Por favor, insira um nome e um número de telefone válido com DDD.")
            return
        janela_adicionar.destroy()
        adicionar_numero_google(nome, telefone)

    def cancelar():
        janela_adicionar.destroy()

    Button(janela_adicionar, text="Continuar", command=continuar).grid(row=2, column=0, padx=10, pady=10)
    Button(janela_adicionar, text="Cancelar", command=cancelar).grid(row=2, column=1, padx=10, pady=10)

def criar_comunidade_no_whatsapp(nome, descricao):
    """Automatiza a criação de uma comunidade no WhatsApp Web."""
    driver = iniciar_driver()
    try:
        driver.get("https://web.whatsapp.com/")
        
        # Clica no botão de "Comunidades"
        botao_comunidades = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Comunidades']"))
        )
        botao_comunidades.click()

        # Clica no botão "Criar Nova Comunidade"
        botao_criar_comunidade = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Criar comunidade' and @role='button']"))
        )
        botao_criar_comunidade.click()

        # Clica no botão "Continuar a criação da comunidade"
        botao_continuar_comunidade = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Continuar a criação da comunidade']"))
        )
        botao_continuar_comunidade.click()

        # Limpa e insere o nome da comunidade
        campo_nome_comunidade = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Nome da comunidade' and @role='textbox']"))
        )
        campo_nome_comunidade.clear()
        campo_nome_comunidade.send_keys(nome)

        # Limpa e insere a descrição da comunidade
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox' and @title='Qual o propósito desta comunidade? É importante adicionar regras para os participantes.']"))
        )
        campo_descricao.clear()
        campo_descricao.send_keys(descricao)

        # Clica no botão de confirmação "Criar comunidade" com o ícone de checkmark
        botao_confirmar_criacao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Criar comunidade' and @role='button']//span[@data-icon='checkmark']"))
        )
        botao_confirmar_criacao.click()

        botao_voltar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Voltar']//span[@data-icon='back']"))
        )
        botao_voltar.click()
        
        messagebox.showinfo("Comunidade Criada", "Comunidade criada no WhatsApp com sucesso!")
    except (TimeoutException, WebDriverException) as e:
        messagebox.showerror("Erro", f"Erro ao criar comunidade: {e}")
    finally:
        driver.quit()


def exibir_janela_criar_comunidade():
    """Exibe uma nova janela para entrada do nome e descrição da comunidade."""
    janela_criar_comunidade = Toplevel()
    janela_criar_comunidade.title("Criar Nova Comunidade")

    Label(janela_criar_comunidade, text="Nome da Comunidade:").grid(row=0, column=0, padx=10, pady=5)
    campo_nome_comunidade = Entry(janela_criar_comunidade)
    campo_nome_comunidade.grid(row=0, column=1, padx=10, pady=5)

    Label(janela_criar_comunidade, text="Descrição:").grid(row=1, column=0, padx=10, pady=5)
    campo_descricao_comunidade = Entry(janela_criar_comunidade)
    campo_descricao_comunidade.grid(row=1, column=1, padx=10, pady=5)

    def continuar():
        nome = campo_nome_comunidade.get()
        descricao = campo_descricao_comunidade.get()
        if not nome or not descricao:
            messagebox.showerror("Erro de Validação", "Por favor, insira o nome e a descrição da comunidade.")
            return
        janela_criar_comunidade.destroy()
        criar_comunidade_no_whatsapp(nome, descricao)

    def cancelar():
        janela_criar_comunidade.destroy()

    Button(janela_criar_comunidade, text="Continuar", command=continuar).grid(row=2, column=0, padx=10, pady=10)
    Button(janela_criar_comunidade, text="Cancelar", command=cancelar).grid(row=2, column=1, padx=10, pady=10)

def selecionar_comunidade():
    driver = iniciar_driver()
    driver.get("https://web.whatsapp.com/")
    
    botao_comunidades = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Comunidades']"))
    )
    botao_comunidades.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[aria-label^="Comunidade: "]'))
    )

    comunidades = driver.find_elements(By.CSS_SELECTOR, '[aria-label^="Comunidade: "]')
    comunidades_nomes = [comunidade.get_attribute('aria-label').replace('Comunidade: ', '') for comunidade in comunidades]

    def abrir_janela_comunidades():
        janela_comunidades = Toplevel()
        janela_comunidades.title("Selecione uma Comunidade")

        Label(janela_comunidades, text="Pesquisar Comunidade:").pack(pady=5)

        pesquisa_var = StringVar()
        pesquisa_entry = Entry(janela_comunidades, textvariable=pesquisa_var)
        pesquisa_entry.pack(pady=5)

        listbox = Listbox(janela_comunidades, selectmode="single", width=50)
        scrollbar = Scrollbar(janela_comunidades)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(pady=5)

        for nome in comunidades_nomes:
            listbox.insert("end", nome)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def filtrar_comunidades(*args):
            termo_pesquisa = pesquisa_var.get().lower()
            listbox.delete(0, "end")
            for nome in comunidades_nomes:
                if termo_pesquisa in nome.lower():
                    listbox.insert("end", nome)

        pesquisa_var.trace("w", filtrar_comunidades)

        def confirmar_selecao():
            selecao = listbox.curselection()
            if not selecao:
                messagebox.showerror("Erro", "Selecione uma comunidade!")
                return

            comunidade_escolhida = listbox.get(selecao)
            index = comunidades_nomes.index(comunidade_escolhida)
            comunidade_elemento = comunidades[index]

            actions = ActionChains(driver)
            actions.move_to_element(comunidade_elemento).click().perform()

            messagebox.showinfo("Comunidade Selecionada", f"Você entrou na comunidade: {comunidade_escolhida}")
            janela_comunidades.destroy()
            abrir_janela_acoes_comunidade(comunidade_escolhida)

        Button(janela_comunidades, text="Confirmar", command=confirmar_selecao).pack(pady=10)
        Button(janela_comunidades, text="Cancelar", command=janela_comunidades.destroy).pack(pady=5)

    abrir_janela_comunidades()

def abrir_janela_acoes_comunidade(nome_comunidade):
    janela_acoes = Toplevel()
    janela_acoes.title(f"Ações para a Comunidade: {nome_comunidade}")

    Label(janela_acoes, text=f"Comunidade Selecionada: {nome_comunidade}").pack(pady=10)

    Button(janela_acoes, text="Criar Grupo", command=lambda: criar_grupo(driver)).pack(pady=5)
    Button(janela_acoes, text="Entrar no Grupo", command=lambda: entrar_grupo(driver)).pack(pady=5)
    Button(janela_acoes, text="Avisos", command=lambda: avisos(driver)).pack(pady=5)
    Button(janela_acoes, text="Adicionar Membro", command=lambda: adicionar_membro(driver)).pack(pady=5)

def criar_grupo(driver):
    # Função que cria um novo grupo na comunidade no WhatsApp
    pass

def entrar_grupo(driver):
    # Função que entra em um grupo específico na comunidade no WhatsApp
    pass

def avisos(driver):
    # Função que acessa a seção de avisos da comunidade no WhatsApp
    pass

def adicionar_membro(driver):
    # Função que adiciona um novo membro à comunidade ou a um grupo específico
    pass


def exibir_janela_opcoes():
    """Exibe a janela principal com as opções iniciais."""
    janela_opcoes = Tk()
    janela_opcoes.title("Opções de Comunidade")

    Label(janela_opcoes, text="Escolha uma opção:").pack(pady=10)

    botao_adicionar_numero = Button(janela_opcoes, text="Adicionar Número", command=exibir_janela_adicionar_numero)
    botao_adicionar_numero.pack(pady=5)

    botao_criar_comunidade = Button(janela_opcoes, text="Criar Nova Comunidade", command=exibir_janela_criar_comunidade)
    botao_criar_comunidade.pack(pady=5)

    botao_entrar_comunidade = Button(janela_opcoes, text="Entrar na Comunidade", command=selecionar_comunidade)
    botao_entrar_comunidade.pack(pady=5)
    

    janela_opcoes.mainloop()

# Inicia o programa exibindo a janela de opções
exibir_janela_opcoes()