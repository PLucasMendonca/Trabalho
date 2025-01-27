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
from PIL import ImageGrab
import numpy as np

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
            options.add_argument('--no-sandbox')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            # Inicia o Chrome
            print("3. Iniciando Chrome...")
            self.driver = uc.Chrome(options=options)
            
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
                compras_location = pyautogui.locateOnScreen('images/compras.png', confidence=0.9)
                if compras_location is None:
                    print("ERRO: Menu Compras não encontrado na tela!")
                    raise Exception("Menu Compras não encontrado na tela")
                
                print("Menu Compras encontrado! Movendo mouse...")
                compras_center = pyautogui.center(compras_location)
                pyautogui.moveTo(compras_center.x, compras_center.y)
                time.sleep(2)
                
                print("2. Procurando submenu Licitação...")
                licitacao_location = pyautogui.locateOnScreen('images/licitacao.png', confidence=0.9)
                if licitacao_location is None:
                    print("ERRO: Submenu Licitação não encontrado!")
                    raise Exception("Submenu Licitação e Dispensa não encontrado")
                
                print("Submenu encontrado! Clicando...")
                licitacao_center = pyautogui.center(licitacao_location)
                pyautogui.click(licitacao_center.x, licitacao_center.y)
                print("Clique em Licitação realizado!")
                time.sleep(3)
                
                print("3. Procurando botão Todas as Compras...")
                todas_compras_location = pyautogui.locateOnScreen('images/todas_compras.png', confidence=0.9)
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
                self.preencher_unidade_compradora(self.unidade_compradora)
                self.preencher_numero_compra(self.numero_compra)
                
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

    def preencher_unidade_compradora(self, codigo):
        try:
            print("\n=== PREENCHENDO UNIDADE COMPRADORA ===")
            # Aguarda um momento para a página carregar completamente
            time.sleep(2)
            
            # Tenta localizar o campo usando diferentes métodos
            print("Procurando campo 'Unidade compradora'...")
            
            # Método 1: Tentar localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen('unidade_compradora.png', confidence=0.7)
                if posicao:
                    print("Campo encontrado pelo método de imagem")
                    centro = pyautogui.center(posicao)
                    # Move o mouse para o centro exato
                    pyautogui.moveTo(centro.x, centro.y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    time.sleep(0.5)
                    pyautogui.write(str(codigo))
                    print(f"Unidade compradora {codigo} preenchida com sucesso!")
                    
                    # Aguarda um momento antes de preencher o próximo campo
                    time.sleep(1)
                    # Chama o método para preencher o número da compra com o valor informado
                    self.preencher_numero_compra(self.numero_compra)
                    return
                    
            except Exception as e:
                print(f"Erro no método 1: {str(e)}")
            
            # Método 2: Tentar localizar pelo texto na tela
            screenshot = ImageGrab.grab()
            texto = pytesseract.image_to_string(screenshot)
            
            if "Unidade compradora" in texto:
                print("Texto encontrado na tela, tentando localizar posição...")
                pos_inicial = pyautogui.position()
                
                for y in range(100, 700, 50):
                    for x in range(100, 1000, 50):
                        pyautogui.moveTo(x, y, duration=0.1)
                        # Captura uma pequena região ao redor do ponto atual
                        bbox = (x-50, y-20, x+150, y+20)  # left, top, right, bottom
                        screenshot = ImageGrab.grab(bbox=bbox)
                        texto_local = pytesseract.image_to_string(screenshot)
                        if "Unidade compradora" in texto_local:
                            print(f"Encontrado em x:{x}, y:{y}")
                            pyautogui.moveTo(x, y, duration=0.5)
                            pyautogui.click()
                            time.sleep(0.5)
                            pyautogui.write(str(codigo))
                            print(f"Unidade compradora {codigo} preenchida com sucesso!")
                            return
                
                pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
            
            print("Não foi possível localizar o campo automaticamente")
            # Método 3: Solicitar ajuda do usuário
            print("Por favor, mova o mouse para o campo 'Unidade compradora' e pressione Enter")
            input("Pressione Enter quando o mouse estiver posicionado...")
            pos = pyautogui.position()
            pyautogui.click(pos.x, pos.y)
            time.sleep(0.5)
            pyautogui.write(str(codigo))
            print(f"Unidade compradora {codigo} preenchida com sucesso!")
            
        except Exception as e:
            print(f"Erro ao preencher unidade compradora: {str(e)}")

    def clicar_botao_expandir(self):
        try:
            print("\n=== CLICANDO NO BOTÃO EXPANDIR ===")
            # Aguarda um momento para a página carregar
            time.sleep(2)
            
            # Localize o elemento
            print("Procurando botão expandir...")
            wait = WebDriverWait(self.driver, 10)
            botao = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-botao-expandir-item button[data-test='btn-expandir']")))
            
            # Simule o movimento do mouse até o elemento e clique
            actions = ActionChains(self.driver)
            actions.move_to_element(botao).click().perform()
            print("Botão expandir clicado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao clicar no botão expandir: {str(e)}")

    def clicar_botao_tarefas(self):
        try:
            print("\n=== CLICANDO NO BOTÃO DE TAREFAS ===")
            # Aguarda a página carregar após a pesquisa
            time.sleep(3)
            
            print("Procurando botão de tarefas...")
            
            # Tenta encontrar o botão na tela atual
            posicao = None
            
            # Loop para rolar a página e procurar o botão
            for _ in range(5):  # Tenta rolar até 5 vezes
                try:
                    posicao = pyautogui.locateOnScreen('botao_tarefas.png', confidence=0.7)
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
                
                # Aguarda um momento e clica no botão expandir
                time.sleep(2)
                self.clicar_botao_expandir()
                
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
                                return
                    
                    pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
                
                print("Não foi possível localizar o botão automaticamente")
                # Método 3: Solicitar ajuda do usuário
                print("Por favor, mova o mouse para o botão de tarefas e pressione Enter")
                input("Pressione Enter quando o mouse estiver posicionado...")
                pos = pyautogui.position()
                pyautogui.click(pos.x, pos.y)
                print("Botão de tarefas clicado com sucesso!")
                
                # Aguarda um momento e clica no botão expandir
                time.sleep(2)
                self.clicar_botao_expandir()
            
        except Exception as e:
            print(f"Erro ao clicar no botão de tarefas: {str(e)}")

    def clicar_pesquisar(self):
        try:
            print("\n=== CLICANDO EM PESQUISAR ===")
            # Aguarda um momento para garantir que a página está pronta
            time.sleep(2)
            
            # Tenta localizar o botão usando diferentes métodos
            print("Procurando botão 'Pesquisar'...")
            
            # Método 1: Tentar localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen('botao_pesquisar.png', confidence=0.7)
                if posicao:
                    print("Botão encontrado pelo método de imagem")
                    centro = pyautogui.center(posicao)
                    # Move o mouse para o centro exato
                    pyautogui.moveTo(centro.x, centro.y, duration=0.5)
                    time.sleep(0.5)
                    pyautogui.click()
                    print("Botão Pesquisar clicado com sucesso!")
                    
                    # Aguarda e clica no botão de tarefas
                    self.clicar_botao_tarefas()
                    
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
                            return
                
                pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
            
            print("Não foi possível localizar o botão automaticamente")
            # Método 3: Solicitar ajuda do usuário
            print("Por favor, mova o mouse para o botão 'Pesquisar' e pressione Enter")
            input("Pressione Enter quando o mouse estiver posicionado...")
            pos = pyautogui.position()
            pyautogui.click(pos.x, pos.y)
            print("Botão Pesquisar clicado com sucesso!")
            
            # Aguarda e clica no botão de tarefas
            self.clicar_botao_tarefas()
            
        except Exception as e:
            print(f"Erro ao clicar no botão pesquisar: {str(e)}")

    def preencher_numero_compra(self, numero):
        try:
            print("\n=== PREENCHENDO NÚMERO DA COMPRA ===")
            # Aguarda um momento para garantir que a página está pronta
            time.sleep(2)
            
            # Tenta localizar o campo usando diferentes métodos
            print("Procurando campo 'Número da compra'...")
            
            # Método 1: Tentar localizar pela imagem
            try:
                posicao = pyautogui.locateOnScreen('numero_compra.png', confidence=0.7)
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
                    
                    # Aguarda um momento e clica em pesquisar
                    time.sleep(1)
                    self.clicar_pesquisar()
                    
            except Exception as e:
                print(f"Erro no método 1: {str(e)}")
            
            # Método 2: Tentar localizar pelo texto na tela
            screenshot = ImageGrab.grab()
            texto = pytesseract.image_to_string(screenshot)
            
            if "Número da compra" in texto:
                print("Texto encontrado na tela, tentando localizar posição...")
                pos_inicial = pyautogui.position()
                
                for y in range(100, 700, 50):
                    for x in range(100, 1000, 50):
                        pyautogui.moveTo(x, y, duration=0.1)
                        bbox = (x-50, y-20, x+150, y+20)
                        screenshot = ImageGrab.grab(bbox=bbox)
                        texto_local = pytesseract.image_to_string(screenshot)
                        if "Número da compra" in texto_local:
                            print(f"Encontrado em x:{x}, y:{y}")
                            pyautogui.moveTo(x, y, duration=0.5)
                            pyautogui.click()
                            time.sleep(0.5)
                            pyautogui.write(str(numero))
                            print(f"Número da compra {numero} preenchido com sucesso!")
                            return
                
                pyautogui.moveTo(pos_inicial.x, pos_inicial.y)
            
            print("Não foi possível localizar o campo automaticamente")
            # Método 3: Solicitar ajuda do usuário
            print("Por favor, mova o mouse para o campo 'Número da compra' e pressione Enter")
            input("Pressione Enter quando o mouse estiver posicionado...")
            pos = pyautogui.position()
            pyautogui.click(pos.x, pos.y)
            time.sleep(0.5)
            pyautogui.write(str(numero))
            print(f"Número da compra {numero} preenchido com sucesso!")
            
            # Aguarda um momento e clica em pesquisar
            time.sleep(1)
            self.clicar_pesquisar()
            
        except Exception as e:
            print(f"Erro ao preencher número da compra: {str(e)}")

    def mainloop(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = ComprasnetAcesso()
    app.mainloop()
