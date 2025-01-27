import tkinter as tk
from tkinter import ttk, messagebox
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pyautogui
import pytesseract
from PIL import ImageGrab, Image
import numpy as np
import cv2
from io import BytesIO
from bs4 import BeautifulSoup

# Configurando o caminho do Tesseract
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if not os.path.exists(tesseract_path):
    print(f"ERRO: Tesseract não encontrado em {tesseract_path}")
    print("Por favor, instale o Tesseract-OCR primeiro!")
    exit(1)
pytesseract.pytesseract.tesseract_cmd = tesseract_path

class ComprasnetAcesso:
    def __init__(self):
        self.driver = None
        self.cnpj = None
        self.mei_confirmado = False
        self.criar_janela()

    def criar_janela(self):
        self.janela = tk.Tk()
        self.janela.title("Acesso Comprasnet")
        self.janela.geometry("300x100")

        ttk.Label(self.janela, text="CNPJ:").pack(pady=5)
        self.cnpj_entry = ttk.Entry(self.janela)
        self.cnpj_entry.pack(pady=5)

        ttk.Button(self.janela, text="Acessar", command=self.iniciar_automacao).pack(pady=10)

    def formatar_cnpj(self, cnpj):
        numeros = ''.join(filter(str.isdigit, cnpj))
        if len(numeros) != 14:
            messagebox.showerror("Erro", "CNPJ deve ter 14 números")
            return None
        return numeros

    def validar_numero(self, P):
        # Permite apenas números e backspace
        if P == "" or P.isdigit():
            return True
        return False
        
    def solicitar_dados_compra(self):
        # Cria uma nova janela
        janela_dados = tk.Toplevel()
        janela_dados.title("Dados da Compra")
        janela_dados.geometry("300x200")
        
        # Configura o validador para aceitar apenas números
        validador = janela_dados.register(self.validar_numero)
        
        # Frame para organizar os widgets
        frame = ttk.Frame(janela_dados, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Unidade Compradora
        ttk.Label(frame, text="Unidade Compradora:").pack(pady=5)
        unidade_entry = ttk.Entry(frame, validate="key", validatecommand=(validador, '%P'))
        unidade_entry.pack(pady=5)
        
        # Número da Compra
        ttk.Label(frame, text="Número da Compra:").pack(pady=5)
        numero_entry = ttk.Entry(frame, validate="key", validatecommand=(validador, '%P'))
        numero_entry.pack(pady=5)
        
        # Variável para controlar quando o usuário terminar
        self.dados_preenchidos = False
        self.unidade_compradora = None
        self.numero_compra = None
        
        def confirmar():
            unidade = unidade_entry.get().strip()
            numero = numero_entry.get().strip()
            
            if not unidade or not numero:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
                return
                
            self.unidade_compradora = unidade
            self.numero_compra = numero
            self.dados_preenchidos = True
            janela_dados.destroy()
        
        # Botão Confirmar
        ttk.Button(frame, text="Confirmar", command=confirmar).pack(pady=20)
        
        # Centraliza a janela
        janela_dados.transient(self.janela)
        janela_dados.grab_set()
        self.janela.wait_window(janela_dados)
        
        return self.dados_preenchidos

    def perguntar_mei(self):
        # Cria uma nova janela
        janela_mei = tk.Toplevel()
        janela_mei.title("Informação MEI")
        janela_mei.geometry("300x150")
        
        # Variável para armazenar a resposta
        self.is_mei = tk.BooleanVar()
        
        # Frame para organizar os widgets
        frame = ttk.Frame(janela_mei, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Checkbox MEI
        ttk.Label(frame, text="A empresa é MEI?").pack(pady=5)
        ttk.Checkbutton(frame, variable=self.is_mei).pack(pady=5)
        
        def confirmar_mei():
            self.mei_confirmado = True
            janela_mei.destroy()
        
        # Botão Confirmar
        ttk.Button(frame, text="Confirmar", command=confirmar_mei).pack(pady=20)
        
        # Centraliza a janela
        janela_mei.transient(self.janela)
        janela_mei.grab_set()
        self.janela.wait_window(janela_mei)
        
        return self.is_mei.get()

    def buscar_itens_pregao(self):
        """Extrai itens da página atual usando BeautifulSoup."""
        try:
            
            # Capturar HTML da página atual
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Selecionar todos os itens na página
            itens = []
            for item in soup.select(".cp-itens-card"):
                numero = item.select_one(".dots.cp-item-bold").text.strip() if item.select_one(".dots.cp-item-bold") else None
                descricao = item.select_one(".text-uppercase").text.strip() if item.select_one(".text-uppercase") else None
                quantidade = item.select_one(".cp-texto-item .mb-half-half").text.strip() if item.select_one(".cp-texto-item .mb-half-half") else None
                valor_estimado = item.select_one(".cp-valor-item span").text.strip() if item.select_one(".cp-valor-item span") else None
                
                itens.append({
                    "Número": numero,
                    "Descrição": descricao,
                    "Quantidade": quantidade,
                    "Valor Estimado": valor_estimado
                })
            
            # Criar janela Tkinter para exibir os itens
            janela_itens = tk.Toplevel()
            janela_itens.title("Itens do Pregão")
            janela_itens.geometry("800x600")
            
            # Criar Treeview
            tree = ttk.Treeview(janela_itens, columns=("Número", "Descrição", "Quantidade", "Valor Estimado"), show="headings")
            
            # Definir cabeçalhos
            tree.heading("Número", text="Número")
            tree.heading("Descrição", text="Descrição")
            tree.heading("Quantidade", text="Quantidade")
            tree.heading("Valor Estimado", text="Valor Estimado")
            
            # Configurar larguras das colunas
            tree.column("Número", width=100)
            tree.column("Descrição", width=300)
            tree.column("Quantidade", width=100)
            tree.column("Valor Estimado", width=150)
            
            # Adicionar scrollbar
            scrollbar = ttk.Scrollbar(janela_itens, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Posicionar elementos
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Inserir itens na tabela
            for item in itens:
                tree.insert("", "end", values=(
                    item["Número"],
                    item["Descrição"],
                    item["Quantidade"],
                    item["Valor Estimado"]
                ))
            
            return itens
            
        except Exception as e:
            print(f"Erro ao buscar itens do pregão: {str(e)}")
            return None

    def iniciar_automacao(self):
        self.cnpj = self.formatar_cnpj(self.cnpj_entry.get())
        if not self.cnpj:
            return

        # Solicita os dados antes de iniciar a automação
        if not self.solicitar_dados_compra():
            print("Operação cancelada pelo usuário")
            return

        print(f"\nCNPJ formatado: {self.cnpj}")
        self.janela.withdraw()

        try:
            print("\n=== INICIANDO AUTOMAÇÃO ===")
            
            # Fecha Chrome existente
            print("1. Fechando Chrome existente...")
            os.system("taskkill /f /im chrome.exe")
            time.sleep(2)
            
            # Configura o Chrome
            print("2. Configurando Chrome...")
            options = uc.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--kiosk')  # Força modo tela cheia
            options.add_argument('--window-size=1920,1080')  # Define tamanho máximo da janela
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--allow-insecure-localhost')
            
            # Inicia o Chrome
            print("3. Iniciando Chrome...")
            self.driver = uc.Chrome(options=options)
            self.driver.maximize_window()  # Garante maximização após iniciar
            
            # Acessa o site
            print("4. Acessando Comprasnet...")
            self.driver.get("https://www.comprasnet.gov.br/seguro/loginPortal.asp")
            time.sleep(2)

              
            # Clica no botão de fornecedor
            print("5. Clicando no botão fornecedor...")
            fornecedor_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.br-button.circle.expand.fornecedor"))
            )
            self.driver.execute_script("arguments[0].click();", fornecedor_button)
            time.sleep(2)
            
            # Clica no botão Gov.br
            print("6. Clicando no botão Gov.br...")
            govbr_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.br-button.is-primary"))
            )
            self.driver.execute_script("arguments[0].click();", govbr_button)
            time.sleep(2)
            
            # Preenche CPF
            print("7. Preenchendo CPF...")
            campo_cpf = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "accountId"))
            )
            campo_cpf.send_keys("012.071.231-88")
            
            # Clica em continuar
            print("8. Clicando em continuar...")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "enter-account-id"))
            ).click()
            
            # Aguarda e verifica captcha
            print("\n=== VERIFICANDO CAPTCHA ===")
            print("Se aparecer captcha, resolva-o manualmente.")
            print("Aguardando campo de senha aparecer...")
            
            campo_senha = WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            print("Campo senha encontrado! Preenchendo...")
            campo_senha.send_keys("Fer050287@")
            
            print("Aguardando botão entrar...")
            botao_entrar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submit-button"))
            )
            print("Clicando em entrar...")
            botao_entrar.click()
            
            print("Aguardando login completar...")
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.CLASS_NAME, "br-form"))
            )
            print("Login realizado com sucesso!")
            
            print("\n=== SELECIONANDO CNPJ ===")
            print("Procurando lista de CNPJs...")
            time.sleep(2)  # Espera a lista carregar
            
            # Encontra todos os inputs de rádio
            cnpj_inputs = self.driver.find_elements(By.CSS_SELECTOR, "div.br-radio input[type='radio']")
            print(f"Encontrados {len(cnpj_inputs)} CNPJs")
            
            cnpj_encontrado = False
            for input_element in cnpj_inputs:
                valor = input_element.get_attribute("value")
                print(f"Verificando CNPJ: {valor}")
                if self.cnpj in valor:
                    print("CNPJ encontrado! Tentando selecionar...")
                    try:
                        self.driver.execute_script("arguments[0].click();", input_element)
                        print("CNPJ selecionado com sucesso!")
                        cnpj_encontrado = True
                        break
                    except Exception as e:
                        print(f"Erro ao clicar no CNPJ: {str(e)}")
                        continue

            if not cnpj_encontrado:
                print("ERRO: CNPJ não encontrado na lista!")
                raise Exception("CNPJ não encontrado")

            print("\n=== CONFIRMANDO SELEÇÃO ===")
            print("Aguardando botão confirmar...")
            botao_confirmar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.br-button.is-primary"))
            )
            print("Clicando em confirmar...")
            self.driver.execute_script("arguments[0].click();", botao_confirmar)
            time.sleep(5)

            print("\n=== NAVEGANDO NO MENU ===")
            try:
                print("1. Procurando menu Compras...")
                compras_location = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'compras.png'), confidence=0.9)
                if compras_location is None:
                    print("ERRO: Menu Compras não encontrado na tela!")
                    raise Exception("Menu Compras não encontrado na tela")
                
                print("Menu Compras encontrado! Movendo mouse...")
                compras_center = pyautogui.center(compras_location)
                pyautogui.moveTo(compras_center.x, compras_center.y)
                time.sleep(2)
                
                print("2. Procurando submenu Licitação...")
                licitacao_location = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'licitacao.png'), confidence=0.9)
                if licitacao_location is None:
                    print("ERRO: Submenu Licitação não encontrado!")
                    raise Exception("Submenu Licitação e Dispensa não encontrado")
                
                print("Submenu encontrado! Clicando...")
                licitacao_center = pyautogui.center(licitacao_location)
                pyautogui.click(licitacao_center.x, licitacao_center.y)
                print("Clique em Licitação realizado!")
                time.sleep(3)
                
                print("3. Procurando botão Todas as Compras...")
                todas_compras_location = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'todas_compras.png'), confidence=0.9)
                if todas_compras_location is None:
                    print("ERRO: Botão Todas as Compras não encontrado!")
                    raise Exception("Botão Todas as Compras não encontrado")
                
                print("Botão encontrado! Clicando em Todas as Compras...")
                todas_compras_center = pyautogui.center(todas_compras_location)
                pyautogui.click(todas_compras_center.x, todas_compras_center.y)
                print("Clique em Todas as Compras realizado!")
                
                # Aguarda a página carregar
                time.sleep(3)
                
                # Preenche os campos com os dados informados
                if not self.preencher_unidade_compradora(self.unidade_compradora):
                    print("Erro ao preencher unidade compradora")
                    return
                
                if not self.preencher_numero_compra(self.numero_compra):
                    print("Erro ao preencher número da compra")
                    return
                
                if not self.clicar_pesquisar():
                    print("Erro ao clicar em pesquisar")
                    return
                
                if not self.clicar_botao_tarefas():
                    print("Erro ao clicar no botão de tarefas")
                    return
                
                print("\n=== PROCESSO FINALIZADO COM SUCESSO ===")
                
            except Exception as e:
                print("\n=== ERRO NA NAVEGAÇÃO ===")
                print(f"Tipo do erro: {type(e).__name__}")
                print(f"Mensagem de erro: {str(e)}")
                if hasattr(e, '__traceback__'):
                    print(f"Linha: {e.__traceback__.tb_lineno}")
                raise Exception("Erro durante a navegação na página") from e
                
        except Exception as e:
            print("\n=== ERRO ===")
            print(f"Tipo do erro: {type(e).__name__}")
            print(f"Mensagem: {str(e)}")
            if hasattr(e, '__traceback__'):
                print(f"Linha: {e.__traceback__.tb_lineno}")
            raise

    def clicar_checkbox_declaracoes(self):
        try:
            print("\n=== CLICANDO NO CHECKBOX DE DECLARAÇÕES ===")
            time.sleep(2)
            
            print("Procurando checkbox de declarações...")
            
            # Método 1: Tentar localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'checkbox_declaracoes.png'), confidence=0.7)
                if posicao:
                    print("Checkbox encontrado pelo método de imagem")
                    # Calcula a posição mais à esquerda (10% da largura)
                    centro = pyautogui.center(posicao)
                    click_x = posicao.left + (posicao.width * 0.1)  # 10% da largura a partir da esquerda
                    click_y = centro.y
                    
                    # Move o mouse para a posição calculada
                    pyautogui.moveTo(click_x, click_y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    print("Checkbox de declarações clicado com sucesso!")
                    return True
            except Exception as e:
                print(f"Erro no método 1: {str(e)}")
            
            # Método 2: Tentar localizar pelo texto na tela
            screenshot = ImageGrab.grab()
            texto = pytesseract.image_to_string(screenshot)
            
            if "Declarações" in texto:
                print("Texto encontrado na tela, tentando localizar posição...")
                pos_inicial = pyautogui.position()
                
                for y in range(100, 700, 50):
                    for x in range(100, 1000, 50):
                        pyautogui.moveTo(x, y, duration=0.1)
                        bbox = (x-50, y-20, x+150, y+20)
                        screenshot = ImageGrab.grab(bbox=bbox)
                        texto_local = pytesseract.image_to_string(screenshot)
                        if "Declarações" in texto_local:
                            print(f"Encontrado em x:{x}, y:{y}")
                            pyautogui.moveTo(x, y, duration=0.5)
                            pyautogui.click()
                            print("Checkbox de declarações clicado com sucesso!")
                            return True
                
                pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
            
            print("Não foi possível localizar o checkbox de declarações")
            return False
            
        except Exception as e:
            print(f"Erro ao clicar no checkbox de declarações: {str(e)}")
            return False

    def clicar_marcar_todas_e_confirmar(self):
        try:
            print("\n=== CLICANDO EM MARCAR TODAS E CONFIRMAR ===")
            time.sleep(2)
            
            print("Procurando botão 'Marcar todas'...")
            
            # Tenta encontrar o botão na tela atual
            posicao = None
            
            # Loop para rolar a página e procurar o botão
            for _ in range(5):  # Tenta rolar até 5 vezes
                try:
                    posicao = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'marcar_todas.png'), confidence=0.7)
                    if posicao:
                        print("Botão encontrado!")
                        break
                except Exception as e:
                    print(f"Não encontrado na posição atual: {str(e)}")
                
                # Se não encontrou, rola a página um pouco
                print("Rolando a página para baixo...")
                pyautogui.press('pagedown')
                time.sleep(1)
            
            if posicao:
                # Calcula a posição mais à esquerda (10% da largura)
                click_x = posicao.left + (posicao.width * 0.1)  # 10% da largura a partir da esquerda
                click_y = posicao.top + (posicao.height / 2)  # Mantém centralizado verticalmente
                
                # Move o mouse para a posição calculada
                pyautogui.moveTo(click_x, click_y, duration=0.5)
                time.sleep(0.5)
                pyautogui.click()
                print("Clicado em Marcar todas!")
            else:
                print("Botão não encontrado")
                return False
            
            # Aguarda um pouco para as checkboxes serem marcadas
            time.sleep(2)
            
            # Rola a página para baixo para encontrar o botão Confirmar
            print("Rolando a página para encontrar o botão Confirmar...")
            # Rola a página algumas vezes até encontrar o botão
            for _ in range(3):  # Tenta rolar até 3 vezes
                pyautogui.press('pagedown')  # Pressiona Page Down
                time.sleep(1)  # Aguarda a rolagem
                
                # Procura e clica no botão Confirmar
                print("Procurando botão 'Confirmar'...")
                confirmar_path = os.path.join(os.path.dirname(__file__), "images", "confirmar.png")
                if not os.path.exists(confirmar_path):
                    print(f"Imagem do botão Confirmar não encontrada em: {confirmar_path}")
                    return False
                    
                confirmar_region = pyautogui.locateOnScreen(confirmar_path, confidence=0.7)
                if confirmar_region:
                    print("Botão Confirmar encontrado!")
                    # Calcula a posição mais à esquerda (10% da largura)
                    click_x = confirmar_region.left + (confirmar_region.width * 0.1)
                    click_y = confirmar_region.top + (confirmar_region.height / 2)
                    
                    pyautogui.moveTo(click_x, click_y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    print("Clicado em Confirmar!")
                    
                    # Aguarda a página carregar após o clique em Confirmar
                    print("Aguardando página carregar...")
                    time.sleep(5)
                    
                    # Extrai os itens da página
                    print("\n=== EXTRAINDO ITENS DA PÁGINA ===")
                    itens = self.extrair_itens()
                    if itens:
                        print(f"Encontrados {len(itens)} itens")
                        return True
                    else:
                        print("Nenhum item encontrado na página")
                        return False
                
                print("Botão Confirmar não encontrado, tentando rolar mais...")
            
            print("Botão Confirmar não encontrado após todas as tentativas")
            return False
                
        except Exception as e:
            print(f"Erro: {str(e)}")
            return False
            
    def atualizar_lista_itens(self, itens):
        try:
            # Cria uma nova janela para mostrar os itens
            janela_itens = tk.Toplevel()
            janela_itens.title("Itens Encontrados")
            janela_itens.geometry("800x600")
            
            # Cria um frame com scrollbar
            frame = ttk.Frame(janela_itens)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Adiciona scrollbar
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Cria o Treeview
            colunas = ('Número', 'Descrição', 'Quantidade', 'Unidade', 'Valor Estimado')
            tree = ttk.Treeview(frame, columns=colunas, show='headings', yscrollcommand=scrollbar.set)
            
            # Configura as colunas
            tree.column('Número', width=70, anchor='center')
            tree.column('Descrição', width=350, anchor='w')
            tree.column('Quantidade', width=100, anchor='center')
            tree.column('Unidade', width=80, anchor='center')
            tree.column('Valor Estimado', width=150, anchor='center')
            
            # Adiciona os cabeçalhos
            for col in colunas:
                tree.heading(col, text=col)
            
            # Adiciona os itens
            for item in itens:
                tree.insert('', tk.END, values=(
                    item['numero'],
                    item['descricao'],
                    item['quantidade'],
                    item['unidade'],
                    item['valor_estimado']
                ))
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=tree.yview)
            
        except Exception as e:
            print(f"Erro ao atualizar lista de itens: {str(e)}")


    def preencher_unidade_compradora(self, codigo):
        try:
            print("\n=== PREENCHENDO UNIDADE COMPRADORA ===")
            print(f"Tentando preencher código: {codigo}")
            
            # Método 1: Tentar localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'unidade_compradora.png'), confidence=0.7)
                if posicao:
                    print("Campo encontrado pelo método de imagem")
                    # Calcula a posição mais à esquerda (10% da largura)
                    click_x = posicao.left + (posicao.width * 0.1)  # 10% da largura a partir da esquerda
                    click_y = posicao.top + (posicao.height / 2)  # Mantém centralizado verticalmente
                    
                    # Move o mouse e clica
                    pyautogui.moveTo(click_x, click_y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    time.sleep(0.5)
                    pyautogui.write(str(codigo))
                    print(f"Unidade compradora {codigo} preenchida com sucesso!")
                    return True
            except Exception as e:
                print(f"Erro no método 1: {str(e)}")
        
            print("Não foi possível localizar o campo 'Unidade compradora'")
            return False
            
        except Exception as e:
            print(f"Erro ao preencher unidade compradora: {str(e)}")
            return False

    def preencher_numero_compra(self, numero):
        try:
            print("\n=== PREENCHENDO NÚMERO DA COMPRA ===")
            time.sleep(2)
            
            print("Procurando campo 'Número da compra'...")
            
            # Tenta localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'numero_compra.png'), confidence=0.7)
                if posicao:
                    print("Campo encontrado pelo método de imagem")
                    centro = pyautogui.center(posicao)
                    # Move o mouse para o centro exato
                    pyautogui.moveTo(centro.x, centro.y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    time.sleep(0.5)
                    pyautogui.write(str(numero))
                    print(f"Número da compra {numero} preenchido com sucesso!")
                    return True
            except Exception as e:
                print(f"Erro ao tentar método por imagem: {str(e)}")
            
            # Se não encontrou pela imagem, tenta pelo texto
            print("Tentando localizar pelo texto na tela...")

            print("Não foi possível localizar o campo 'Número da compra'")
            return False
            
        except Exception as e:
            print(f"Erro ao preencher número da compra: {str(e)}")
            return False

    def clicar_botao_tarefas(self):
        try:
            print("\n=== CLICANDO NO BOTÃO DE TAREFAS ===")
            time.sleep(3)
            
            print("Procurando botão de tarefas...")
            
            # Tenta encontrar o botão na tela atual
            posicao = None
            
            # Loop para rolar a página e procurar o botão
            for _ in range(5):  # Tenta rolar até 5 vezes
                try:
                    posicao = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'botao_tarefas.png'), confidence=0.7)
                    if posicao:
                        print("Botão encontrado!")
                        break
                except Exception as e:
                    print(f"Não encontrado na posição atual: {str(e)}")
                
                # Se não encontrou, rola a página um pouco
                print("Rolando a página para baixo...")
                pyautogui.press('pagedown')
                time.sleep(1)
            
            if posicao:
                centro = pyautogui.center(posicao)
                # Move o mouse para o centro exato
                pyautogui.moveTo(centro.x, centro.y, duration=0.5)
                time.sleep(0.5)
                pyautogui.click()
                print("Botão de tarefas clicado com sucesso!")
                return True
            else:
                print("Botão não encontrado. Tentando método alternativo...")
                # Método alternativo: procura pelo texto na tela
                screenshot = ImageGrab.grab()
                texto = pytesseract.image_to_string(screenshot)
                
                if "tasks" in texto.lower():
                    print("Texto 'tasks' encontrado na tela, tentando localizar posição...")
                    pos_inicial = pyautogui.position()
                    
                    for y in range(100, 700, 50):
                        for x in range(100, 1000, 50):
                            pyautogui.moveTo(x, y, duration=0.1)
                            bbox = (x-20, y-20, x+20, y+20)
                            screenshot = ImageGrab.grab(bbox=bbox)
                            texto_local = pytesseract.image_to_string(screenshot)
                            if "tasks" in texto_local.lower():
                                print(f"Encontrado em x:{x}, y:{y}")
                                pyautogui.moveTo(x, y, duration=0.5)
                                pyautogui.click()
                                print("Botão de tarefas clicado com sucesso!")
                                return True
                    
                    pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
                
                print("Não foi possível localizar o botão de tarefas")
                return False
            
        except Exception as e:
            print(f"Erro ao clicar no botão de tarefas: {str(e)}")
            return False

    def clicar_pesquisar(self):
        try:
            print("\n=== CLICANDO EM PESQUISAR ===")
            time.sleep(2)
            
            print("Procurando botão 'Pesquisar'...")
            
            # Método 1: Tentar localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen(os.path.join(os.path.dirname(__file__), 'images', 'pesquisar.png'), confidence=0.7)
                if posicao:
                    print("Botão encontrado pelo método de imagem")
                    centro = pyautogui.center(posicao)
                    # Move o mouse para o centro exato
                    pyautogui.moveTo(centro.x, centro.y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    print("Botão Pesquisar clicado com sucesso!")
                    return True
            except Exception as e:
                print(f"Erro no método 1: {str(e)}")
            
            # Método 2: Tentar localizar pelo texto na tela
            screenshot = ImageGrab.grab()
            texto = pytesseract.image_to_string(screenshot)
            
            if "Pesquisar" in texto:
                print("Texto encontrado na tela, tentando localizar posição...")
                pos_inicial = pyautogui.position()
                
                for y in range(100, 700, 50):
                    for x in range(100, 1000, 50):
                        pyautogui.moveTo(x, y, duration=0.1)
                        bbox = (x-50, y-20, x+150, y+20)
                        screenshot = ImageGrab.grab(bbox=bbox)
                        texto_local = pytesseract.image_to_string(screenshot)
                        if "Pesquisar" in texto_local:
                            print(f"Encontrado em x:{x}, y:{y}")
                            pyautogui.moveTo(x, y, duration=0.5)
                            pyautogui.click()
                            print("Botão Pesquisar clicado com sucesso!")
                            return True
                
                pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
            
            print("Não foi possível localizar o botão 'Pesquisar'")
            return False
            
        except Exception as e:
            print(f"Erro ao clicar no botão pesquisar: {str(e)}")
            return False

    def mainloop(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = ComprasnetAcesso()
    app.mainloop()