from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import re
import time
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import Tk, Toplevel, Label, Entry, Button, Listbox, StringVar, Scrollbar, messagebox
import tkinter as tk
import csv
import tempfile
import os
from selenium.webdriver.common.keys import Keys

'''
Para o funcionamento é preciso fechar TODAS sas janelas do gooogle Chrome
'''


class WhatsAppAutomation:
    def __init__(self):
        self.driver = self.iniciar_driver()
        self.comunidades_nomes = []
        self.selecionar_comunidade()

    def iniciar_driver(self):
        caminho_perfil = "C:/Users/Windows 11/AppData/Local/Google/Chrome/User Data"
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={caminho_perfil}")
        chrome_options.add_argument("--profile-directory=Profile 3")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def selecionar_comunidade(self):
        """Abre WhatsApp Web, rola a lista de comunidades e carrega todos os nomes."""
        self.driver.get("https://web.whatsapp.com/")
        try:
            # Aguardar botão de 'Comunidades' ficar clicável
            btn_comunidades = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Comunidades']"))
            )
            btn_comunidades.click()

            # Localizar o container da lista de comunidades
            community_list = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "x1n2onr6.x1n2onr6.xyw6214"))
            )

            comunidades_nomes_set = set()  # Usar set para evitar duplicatas
            last_count = 0
            scroll_pause_time = 1.5  # Ajuste o tempo conforme necessário

            while True:
                # Capturar todas as comunidades visíveis no momento
                comunidades = self.driver.find_elements(By.XPATH, "//div[@aria-label and starts-with(@aria-label, 'Comunidade:')]")

                # Adicionar os nomes das comunidades ao conjunto
                for comunidade in comunidades:
                    comunidades_nomes_set.add(comunidade.get_attribute('aria-label').replace('Comunidade: ', ''))

                # Verificar se mais comunidades foram carregadas
                if len(comunidades_nomes_set) == last_count:  # Nenhuma nova comunidade
                    break

                # Atualizar o contador
                last_count = len(comunidades_nomes_set)

                # Scrollar o container
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", community_list)
                time.sleep(scroll_pause_time)

            # Salvar os nomes das comunidades no atributo da classe
            self.comunidades_nomes = list(comunidades_nomes_set)
            print(f"Comunidades carregadas: {self.comunidades_nomes}")

        except TimeoutException as e:
            messagebox.showerror("Erro", f"Erro ao carregar comunidades: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

    def exibir_janela_comunidades(self):
        """Tela para exibir e selecionar comunidades."""
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

        for nome in self.comunidades_nomes:
            listbox.insert("end", nome)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def filtrar_comunidades(*args):
            termo_pesquisa = pesquisa_var.get().lower()
            listbox.delete(0, "end")
            for nome in self.comunidades_nomes:
                if termo_pesquisa in nome.lower():
                    listbox.insert("end", nome)

        pesquisa_var.trace("w", filtrar_comunidades)

        def confirmar_selecao():
            selecao = listbox.curselection()
            if not selecao:
                messagebox.showerror("Erro", "Selecione uma comunidade!")
                return
            comunidade_escolhida = listbox.get(selecao)
            self.comunidade_selecionada = comunidade_escolhida
            janela_comunidades.destroy()
            self.abrir_janela_acoes_comunidade(comunidade_escolhida)

        def criar_nova_comunidade():
            janela_comunidades.destroy()
            self.exibir_janela_criar_comunidade()

        Button(janela_comunidades, text="Confirmar Seleção",
               command=confirmar_selecao).pack(pady=10)
        Button(janela_comunidades, text="Criar Nova Comunidade",
               command=criar_nova_comunidade).pack(pady=5)
        Button(janela_comunidades, text="Fechar",
               command=janela_comunidades.destroy).pack(pady=5)

    def exibir_janela_criar_comunidade(self):
        """Exibe uma janela para criar uma nova comunidade."""
        janela_criar_comunidade = Toplevel()
        janela_criar_comunidade.title("Criar Nova Comunidade")

        Label(janela_criar_comunidade, text="Nome da Comunidade:").grid(
            row=0, column=0, padx=10, pady=5)
        campo_nome_comunidade = Entry(janela_criar_comunidade)
        campo_nome_comunidade.grid(row=0, column=1, padx=10, pady=5)

        Label(janela_criar_comunidade, text="Descrição:").grid(
            row=1, column=0, padx=10, pady=5)
        campo_descricao_comunidade = Entry(janela_criar_comunidade)
        campo_descricao_comunidade.grid(row=1, column=1, padx=10, pady=5)

        def continuar():
            nome = campo_nome_comunidade.get()
            descricao = campo_descricao_comunidade.get()
            if not nome or not descricao:
                messagebox.showerror(
                    "Erro de Validação", "Por favor, insira o nome e a descrição da comunidade.")
                return
            janela_criar_comunidade.destroy()
            self.criar_comunidade(nome, descricao)
            self.exibir_janela_comunidades()  # Retorna para a seleção de comunidades

        Button(janela_criar_comunidade, text="Continuar",
               command=continuar).grid(row=2, column=0, padx=10, pady=10)
        Button(janela_criar_comunidade, text="Cancelar", command=janela_criar_comunidade.destroy).grid(
            row=2, column=1, padx=10, pady=10)

    def abrir_janela_acoes_comunidade(self, nome_comunidade):
        """Tela de ações específicas para a comunidade selecionada."""
        janela_acoes = Toplevel()
        janela_acoes.title(f"Ações para a Comunidade: {nome_comunidade}")

        Label(janela_acoes, text=f"Comunidade Selecionada: {
              nome_comunidade}").pack(pady=10)

        Button(janela_acoes, text="Adicionar Membro",
               command=self.abrir_janela_adicionar).pack(pady=5)
        Button(janela_acoes, text="Remover Membro",
               command=self.abrir_janela_remover).pack(pady=5)

    def adicionar_numero_google(self, temp_file_path):
        """Funcionalidade para adicionar o nome e telefone no Google Contacts."""
        self.driver.get("https://contacts.google.com")

        try:    
            elemento_import = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button' and .//div[text()='Import']]"))
            )
            elemento_import.click()

            input_file = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='file']"))
            )
            # Verifica se o arquivo existe
            if not os.path.exists(temp_file_path):
                raise FileNotFoundError(
                    f"O arquivo {temp_file_path} não foi encontrado.")

            # Faz o upload do arquivo
            input_file.send_keys(temp_file_path)
            
            botao_select_file = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[text()='Import']]"))
            )
            botao_select_file.click()
            
            WebDriverException(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[text()='All done']")))

        except (TimeoutException, WebDriverException) as e:
            messagebox.showerror("Erro", f"Erro ao adicionar número: {e}")

        finally:
            # Certifique-se de passar o argumento correto, se necessário.
            time.sleep(5) #Tempo para numero aparecer no celular, não foi cronometrado.
            self.adicionar_membro_comunidade(temp_file_path)

    def adicionar_membro_comunidade(self, csv_file_path):
        import csv
        try:
            # Lê o arquivo CSV
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                nomes = [row["First Name"]
                         for row in reader if "First Name" in row and row["First Name"].strip()]

            # Seleciona a comunidade
            self.selecionar_comunidade()
            if not hasattr(self, 'comunidade_selecionada'):
                messagebox.showerror(
                    "Erro", "Nenhuma comunidade foi selecionada.")
                print("Erro: Nenhuma comunidade foi selecionada.")
                return

            comunidade_selecionada = self.comunidade_selecionada

            # Localiza e clica na comunidade
            comunidade_xpath = f"//div[@aria-label='Comunidade: {
                comunidade_selecionada}' and @role='button']"
            comunidade_elemento = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, comunidade_xpath))
            )
            comunidade_elemento.click()

            # Clica no ícone de menu
            menu_icon_xpath = "//span[@data-icon='menu']"
            menu_icon_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, menu_icon_xpath))
            )
            menu_icon_element.click()

            # Ver participantes
            ver_participantes_xpath = "//li[@role='button']//div[@aria-label='Ver participantes']"
            ver_participantes_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ver_participantes_xpath))
            )
            ver_participantes_element.click()

            botao_adicionar_xpath = "//div[@role='button' and @aria-label='Adicionar participantes']"
            botao_adicionar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, botao_adicionar_xpath))
            )
            botao_adicionar.click()

            for nome in nomes:
                try:
                    print(f"Adicionando: {nome}")
                    # Campo editável para digitar o nome
                    campo_editavel_xpath = "//div[@contenteditable='true' and @role='textbox']"
                    campo_editavel = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, campo_editavel_xpath))
                    )
                    campo_editavel.click()
                    campo_editavel.send_keys(Keys.CONTROL + "a")
                    campo_editavel.send_keys(Keys.BACKSPACE)
                    campo_editavel.send_keys(nome)
                    time.sleep(1)
                    # Primeiro botão correspondente ao nome digitado
                    campo_elemento_editavel = f"(//div[@role='checkbox' and .//span[contains(text(), '{nome.split()[0]}')]])[1]"
                    campo_elemento = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, campo_elemento_editavel))
                    )

                    # Verifica o estado do checkbox para saber se o membro já está no grupo
                    estado_checkbox = campo_elemento.get_attribute(
                        "aria-checked")
                    if estado_checkbox == "true":
                        print(f"{nome} já está no grupo. Pulando...")
                        continue  # Passa para o próximo nome
                    

                    # Se não estiver no grupo, clica para adicionar
                    if campo_elemento.is_displayed():
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", campo_elemento)
                        campo_elemento.click()
                        print(f"{nome} foi adicionado com sucesso.")
                    else:
                        print(f"O elemento correspondente ao nome {
                              nome} não está visível ou habilitado para clique.")
                        continue

                    campo_editavel.clear()

                except Exception as e:
                    print(f"Erro ao adicionar {nome}: {e}")
            
            # Confirmar a adição dos membros
            try:
                confirmar_xpath = "//div[@role='button' and .//span[@aria-label='Confirmar']]"
                print("Aguardando o botão de confirmação...")
                botao_confirmar = WebDriverWait(self.driver, 14).until(
                    EC.presence_of_element_located((By.XPATH, confirmar_xpath))
                )

                if botao_confirmar.is_displayed() and botao_confirmar.is_enabled():
                    print("Tentando clicar no botão...")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", botao_confirmar)
                    botao_confirmar.click()
                    print("Botão 'Confirmar' clicado com sucesso.")

                    adicionar_membro_xpath = "//div[contains(text(), 'Adicionar membro')]"

                    # Aguarda o botão "Adicionar membro" ficar clicável
                    adicionar_membro_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, adicionar_membro_xpath))
                    )
                    # Clica no botão "Adicionar membro"
                    self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", adicionar_membro_button)
                    adicionar_membro_button.click()
                else:
                    print("Botão 'Confirmar' não está visível ou habilitado.")
            except Exception as e:
                # Caso o botão "Confirmar" não esteja presente
                print("O botão 'Confirmar' não está presente na tela.")
                print("Isso pode significa que todos já estão no grupo.")
                # Aqui você pode adicionar lógica adicional, como exibir uma mensagem ao usuário.
                messagebox.showinfo(
                    "Todos já estão no grupo",
                    "Não há mais membros para adicionar. Todos já estão na comunidade."
                )
                root.destroy()
                

        except Exception as e:
            print(f"Erro ao adicionar membros: {e}")

    def criar_comunidade(self, nome, descricao):
        try:
            self.driver.get("https://web.whatsapp.com/")
            botao_comunidades = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Comunidades']"))
            )
            botao_comunidades.click()

            # Clica no botão "Criar Nova Comunidade"
            botao_criar_comunidade = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Criar comunidade' and @role='button']"))
            )
            botao_criar_comunidade.click()

            botao_continuar_comunidade = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button' and @aria-label='Continuar a criação da comunidade']"))
            )
            botao_continuar_comunidade.click()

            campo_nome_comunidade = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@title='Nome da comunidade' and @role='textbox']"))
            )
            campo_nome_comunidade.clear()
            campo_nome_comunidade.send_keys(nome)

            campo_descricao = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='textbox' and @title='Qual o propósito desta comunidade? É importante adicionar regras para os participantes.']"))
            )
            campo_descricao.clear()
            campo_descricao.send_keys(descricao)

            botao_confirmar_criacao = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Criar comunidade' and @role='button']//span[@data-icon='checkmark']"))
            )
            botao_confirmar_criacao.click()

            # Volta à tela principal
            botao_voltar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div[role='button'][aria-label='Voltar']"))
            )
            botao_voltar.click()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar comunidade: {e}")

    def fechar(self):
        """Fecha o WebDriver e libera recursos."""
        self.driver.quit()

    def remover_membros_comunidade(self, csv_file_path):
        import csv
        import unicodedata
        try:
            # Lê o arquivo CSV
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                nomes = [row["First Name"]
                        for row in reader if "First Name" in row and row["First Name"].strip()]

            # Normaliza nomes para comparação
            def normalize(text):
                return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

            # Seleciona a comunidade
            self.selecionar_comunidade()
            if not hasattr(self, 'comunidade_selecionada'):
                messagebox.showerror(
                    "Erro", "Nenhuma comunidade foi selecionada.")
                return

            comunidade_selecionada = self.comunidade_selecionada

            # Localiza e clica na comunidade
            comunidade_xpath = f"//div[@aria-label='Comunidade: {comunidade_selecionada}' and @role='button']"
            comunidade_elemento = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, comunidade_xpath))
            )
            comunidade_elemento.click()

            for nome in nomes:
                try:
                    print(f"Processando: {nome}")
                    nome_normalizado = normalize(nome)
                    # Fecha qualquer diálogo bloqueante
                    dialog_xpath = "//div[@role='dialog' and contains(@aria-label, 'Participantes')]"
                    try:
                        dialog_element = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, dialog_xpath))
                        )
                        close_button_xpath = "//div[@role='button' and @aria-label='Fechar']"
                        close_button = dialog_element.find_element(By.XPATH, close_button_xpath)
                        self.driver.execute_script("arguments[0].click();", close_button)
                        time.sleep(1)  # Aguarde para garantir o fechamento
                        print("Diálogo bloqueante fechado com sucesso.")
                    except TimeoutException:
                        print("Nenhum diálogo bloqueante encontrado. Continuando...")
                    print(f"Processando: {nome}")

                    # Clica no ícone de menu
                    menu_icon_xpath = "//span[@data-icon='menu']"
                    menu_icon_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, menu_icon_xpath))
                    )
                    menu_icon_element.click()

                    # Ver participantes
                    ver_participantes_xpath = "//li[@role='button']//div[@aria-label='Ver participantes']"
                    ver_participantes_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, ver_participantes_xpath))
                    )
                    ver_participantes_element.click()

                    # Digita o nome no campo de busca
                    campo_editavel_xpath = "//button[@aria-label='Lista de conversas']"
                    campo_editavel = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, campo_editavel_xpath))
                    )
                    campo_editavel.click()

                    input_xpath = "//div[@contenteditable='true' and @role='textbox']"
                    campo_texto = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, input_xpath)))
                    campo_texto.send_keys(Keys.CONTROL + "a")
                    campo_texto.send_keys(Keys.BACKSPACE)
                    campo_texto.send_keys(nome_normalizado)

                    # Verifica se há resultados na lista
                    nenhum_contato_xpath = "//span[text()='Nenhum contato encontrado']"
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, nenhum_contato_xpath))
                        )
                        print(f"'{nome}' não encontrado. Pulando...")
                        continue
                    except Exception:
                        print(f"'{nome}' encontrado. Verificando correspondência...")

                    # Verifica se o nome na lista corresponde ao nome do CSV
                    nomes_xpath = "//div[contains(@class, 'x1n2onr6') and contains(@class, 'xyw6214')]//span[@dir='auto']"
                    nomes_exibidos = self.driver.find_elements(By.XPATH, nomes_xpath)


                    nome_encontrado = False
                    for nome_lista in nomes_exibidos:
                        if normalize(nome) in normalize(nome_lista.text):
                            nome_encontrado = True
                            break

                    if not nome_encontrado:
                        print(f"Nome '{nome}' não corresponde. Pulando...")
                        continue

                    nome_card_xpath = "//div[contains(@class, 'x1n2onr6') and contains(@class, 'xyw6214')]//span[contains(@class, 'x1iyjqo2') and text() != '']"
                    try:
                        # Localiza o card correspondente ao nome
                        nome_card = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, nome_card_xpath))
                        )
                        
                        # Clica no card do nome
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", nome_card)
                        nome_card.click()
                        print(f"Nome '{nome}' encontrado e card clicado.")
                    except Exception as e:
                        print(f"Erro ao localizar ou clicar no card do nome '{nome}': {e}")

                    # Remove o participante
                    remover_xpath = "//li[@role='button']//div[contains(text(), 'Remover da comunidade')]"
                    remover_elemento = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, remover_xpath))
                    )
                    remover_elemento.click()

                    # Confirma a remoção
                    modal_xpath = "//div[@data-animate-modal-popup='true']"
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, modal_xpath))
                    )

                    remover_button_xpath = "//button//div[text()='Remover']"
                    remover_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, remover_button_xpath))
                    )
                    remover_button.click()

                    print(f"Membro '{nome}' removido com sucesso.")
                except Exception as e:
                    print(f"Erro ao processar '{nome}': {e}")

            # Mensagem final
            print("Processo de remoção concluído para todos os membros.")
        except Exception as e:
            print(f"Erro geral ao processar a remoção: {e}")
        finally:
            messagebox.showinfo("Processo Concluído", "Todos os nomes do CSV foram processados. O processo foi concluído com sucesso.")

    def abrir_janela_adicionar(self):
        # Dicionário para armazenar os dados preenchidos
        dados_pessoas = {}

        def somente_numeros(text):
            """Permitir apenas números no campo de entrada."""
            return text.isdigit() or text == ""

        def validar_telefone(telefone):
            """Valida se o telefone contém apenas números e tem o DDD."""
            return re.fullmatch(r'\d{10,11}', telefone) is not None

        def criar_linhas():
            """Cria ou ajusta as linhas dinamicamente com campos para Nome e Telefone."""
            # Obter o valor do campo de entrada
            try:
                qtd = int(entrada_qtd.get())
                if qtd <= 0 or qtd > 2000:
                    raise ValueError("A quantidade deve ser entre 1 e 2000.")
            except ValueError:
                messagebox.showerror(
                    "Erro", "Por favor, insira um número válido entre 1 e 400.")
                return

            # Salvar dados já preenchidos
            for widget in frame_tabela.winfo_children():
                info = widget.grid_info()
                row, col = info["row"], info["column"]
                if col == 1:  # Nome
                    nome = widget.get().strip()
                    if row in dados_pessoas:
                        dados_pessoas[row]["nome"] = nome
                    else:
                        dados_pessoas[row] = {"nome": nome, "telefone": ""}
                elif col == 3:  # Telefone
                    telefone = widget.get().strip()
                    if row in dados_pessoas:
                        dados_pessoas[row]["telefone"] = telefone
                    else:
                        dados_pessoas[row] = {"nome": "", "telefone": telefone}

            # Ajustar o número de linhas na tabela
            linhas_atuais = len(dados_pessoas)
            if qtd > linhas_atuais:
                # Adicionar novas linhas
                for i in range(linhas_atuais, qtd):
                    dados_pessoas[i] = {"nome": "", "telefone": ""}
            elif qtd < linhas_atuais:
                # Remover linhas excedentes
                for i in range(qtd, linhas_atuais):
                    dados_pessoas.pop(i, None)

            # Recriar os widgets na tabela
            for widget in frame_tabela.winfo_children():
                widget.destroy()

            for i in range(qtd):
                # Nome
                tk.Label(frame_tabela, text=f"Nome {
                         i+1}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
                nome_entry = tk.Entry(frame_tabela, width=30)
                nome_entry.grid(row=i, column=1, padx=5, pady=5)
                nome_entry.insert(0, dados_pessoas[i]["nome"])

                # Telefone
                tk.Label(frame_tabela, text=f"Telefone {
                         i+1}:").grid(row=i, column=2, padx=5, pady=5, sticky="w")
                telefone_entry = tk.Entry(frame_tabela, width=15)
                telefone_entry.grid(row=i, column=3, padx=5, pady=5)
                telefone_entry.insert(0, dados_pessoas[i]["telefone"])

            # Atualizar o canvas para ajustar o tamanho do frame
            canvas_tabela.update_idletasks()
            canvas_tabela.config(scrollregion=canvas_tabela.bbox("all"))

        def capturar_dados():
            """Captura os dados inseridos nas linhas e os valida."""
            dados = []
            for i, widget in enumerate(frame_tabela.winfo_children()):
                info = widget.grid_info()
                row, col = info["row"], info["column"]
                if col == 1:  # Nome
                    nome = widget.get().strip()
                elif col == 3:  # Telefone
                    telefone = widget.get().strip()
                    if not nome or not validar_telefone(telefone):
                        messagebox.showerror(
                            "Erro de Validação",
                            f"Erro na linha {
                                row + 1}: Verifique o nome e o telefone com DDD.",
                        )
                        return
                    dados.append(
                        {"First Name": nome, "Mobile Phone": telefone})
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="", encoding="utf-8") as temp_csv:
                    csv_writer = csv.DictWriter(
                        temp_csv, fieldnames=["First Name", "Mobile Phone"])
                    csv_writer.writeheader()
                    csv_writer.writerows(dados)
                    temp_file_path = temp_csv.name
                    print(f"Arquivo CSV criado: {temp_file_path}")
                self.adicionar_numero_google(temp_file_path)
            except Exception as e:
                print(f"Erro ao capturar dados: {e}")
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                    print(f"Arquivo CSV apagado: {temp_file_path}")

            nova_janela.destroy()

        # Criar nova janela
        nova_janela = tk.Toplevel(root)
        nova_janela.title("Adicionar Pessoas na Comunidade")
        nova_janela.geometry("600x600")

        # Campo para escolher a quantidade de pessoas
        tk.Label(nova_janela, text="Digite a quantidade de pessoas (máx 2000):").pack(
            pady=10)
        entrada_qtd = tk.Entry(nova_janela, validate="key", width=10)
        entrada_qtd.pack(pady=5)
        entrada_qtd.configure(validatecommand=(
            nova_janela.register(somente_numeros), "%P"))

        # Botão para criar linhas
        botao_criar_linhas = tk.Button(
            nova_janela, text="Criar Campos", command=criar_linhas)
        botao_criar_linhas.pack(pady=10)

        # Canvas e Scrollbar para a tabela
        frame_canvas = tk.Frame(nova_janela)
        frame_canvas.pack(pady=20, fill="both", expand=True)

        canvas_tabela = tk.Canvas(frame_canvas)
        scrollbar_tabela = tk.Scrollbar(
            frame_canvas, orient="vertical", command=canvas_tabela.yview)
        canvas_tabela.configure(yscrollcommand=scrollbar_tabela.set)

        # Posicionar o Canvas e o Scrollbar
        canvas_tabela.pack(side="left", fill="both", expand=True)
        scrollbar_tabela.pack(side="right", fill="y")

        # Frame interno para as linhas (dentro do Canvas)
        frame_tabela = tk.Frame(canvas_tabela)
        canvas_tabela.create_window((0, 0), window=frame_tabela, anchor="nw")

        # Botão para capturar os dados
        botao_capturar = tk.Button(
            nova_janela, text="Salvar Dados", command=capturar_dados)
        botao_capturar.pack(pady=10)

        botao_voltar = tk.Button(
            nova_janela, text="Voltar", command=nova_janela.destroy)
        botao_voltar.pack(pady=10)


    def abrir_janela_remover(self):
        """Função para abrir uma janela para remover membros da comunidade."""

        # Dicionário para armazenar os dados preenchidos
        dados_pessoas = {}

        def criar_linhas():
            """Cria ou ajusta as linhas dinamicamente com campos para Nome."""
            # Obter o valor do campo de entrada
            try:
                qtd = int(entrada_qtd.get())
                if qtd <= 0 or qtd > 2000:
                    raise ValueError("A quantidade deve ser entre 1 e 2000.")
            except ValueError:
                messagebox.showerror(
                    "Erro", "Por favor, insira um número válido entre 1 e 2000.")
                return

            # Salvar dados já preenchidos
            for widget in frame_tabela.winfo_children():
                info = widget.grid_info()
                row, col = info["row"], info["column"]
                if col == 1:  # Nome
                    nome = widget.get().strip()
                    if row in dados_pessoas:
                        dados_pessoas[row]["nome"] = nome
                    else:
                        dados_pessoas[row] = {"nome": nome}

            # Ajustar o número de linhas na tabela
            linhas_atuais = len(dados_pessoas)
            if qtd > linhas_atuais:
                for i in range(linhas_atuais, qtd):
                    dados_pessoas[i] = {"nome": ""}
            elif qtd < linhas_atuais:
                for i in range(qtd, linhas_atuais):
                    dados_pessoas.pop(i, None)

            # Recriar os widgets na tabela
            for widget in frame_tabela.winfo_children():
                widget.destroy()

            for i in range(qtd):
                # Nome
                tk.Label(frame_tabela, text=f"Nome {
                         i+1}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
                nome_entry = tk.Entry(frame_tabela, width=30)
                nome_entry.grid(row=i, column=1, padx=5, pady=5)
                nome_entry.insert(0, dados_pessoas[i]["nome"])

            # Atualizar o canvas para ajustar o tamanho do frame
            canvas_tabela.update_idletasks()
            canvas_tabela.config(scrollregion=canvas_tabela.bbox("all"))

        def capturar_dados_remocao():
            """Captura os dados inseridos nas linhas."""
            dados = []
            for i, widget in enumerate(frame_tabela.winfo_children()):
                info = widget.grid_info()
                row, col = info["row"], info["column"]
                if col == 1:  # Nome
                    nome = widget.get().strip()
                    if not nome:
                        messagebox.showerror("Erro de Validação", f"Erro na linha {
                                             row + 1}: Nome não pode estar vazio.")
                        return
                    dados.append({"First Name": nome})
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="", encoding="utf-8") as temp_csv:
                    csv_writer = csv.DictWriter(
                        temp_csv, fieldnames=["First Name"])
                    csv_writer.writeheader()
                    csv_writer.writerows(dados)
                    temp_file_path = temp_csv.name
                    print(f"Arquivo CSV criado: {temp_file_path}")
                self.remover_membros_comunidade(temp_file_path)
            except Exception as e:
                print(f"Erro ao capturar dados: {e}")
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                    print(f"Arquivo CSV apagado: {temp_file_path}")

            nova_janela.destroy()

        # Criar nova janela
        nova_janela = tk.Toplevel(root)
        nova_janela.title("Remover Pessoas da Comunidade")
        nova_janela.geometry("600x600")

        # Campo para escolher a quantidade de pessoas
        tk.Label(nova_janela, text="Digite a quantidade de pessoas a remover (máx 2000):").pack(
            pady=10)
        entrada_qtd = tk.Entry(nova_janela, validate="key", width=10)
        entrada_qtd.pack(pady=5)
        entrada_qtd.configure(validatecommand=(nova_janela.register(
            lambda text: text.isdigit() or text == ""), "%P"))

        # Botão para criar linhas
        botao_criar_linhas = tk.Button(
            nova_janela, text="Criar Campos", command=criar_linhas)
        botao_criar_linhas.pack(pady=10)

        # Canvas e Scrollbar para a tabela
        frame_canvas = tk.Frame(nova_janela)
        frame_canvas.pack(pady=20, fill="both", expand=True)

        canvas_tabela = tk.Canvas(frame_canvas)
        scrollbar_tabela = tk.Scrollbar(
            frame_canvas, orient="vertical", command=canvas_tabela.yview)
        canvas_tabela.configure(yscrollcommand=scrollbar_tabela.set)

        # Posicionar o Canvas e o Scrollbar
        canvas_tabela.pack(side="left", fill="both", expand=True)
        scrollbar_tabela.pack(side="right", fill="y")

        # Frame interno para as linhas (dentro do Canvas)
        frame_tabela = tk.Frame(canvas_tabela)
        canvas_tabela.create_window((0, 0), window=frame_tabela, anchor="nw")

        # Botão para capturar os dados
        botao_capturar = tk.Button(
            nova_janela, text="Remover Pessoas", command=capturar_dados_remocao)
        botao_capturar.pack(pady=10)

        botao_voltar = tk.Button(
            nova_janela, text="Voltar", command=nova_janela.destroy)
        botao_voltar.pack(pady=10)


# Inicializa o Tkinter e a classe de automação
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    app = WhatsAppAutomation()
    app.exibir_janela_comunidades()
    root.mainloop()
