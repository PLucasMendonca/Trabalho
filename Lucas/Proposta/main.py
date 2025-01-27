import os
import json
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk, messagebox
import glob

# Dicionário com as modalidades por portal
MODALIDADES = {
    'bll': ['Pregão', 'Concorrência', 'Dispensa', 'Licitação 13.303'],
    'comprasnet': ['Pregão', 'Concorrência', 'Cotação', 'Dispensa'],
    'compraspublicas': ['Pregão', 'Concorrência', 'Dispensa'],
    'bnc': ['Pregão', 'Concorrência', 'Dispensa', 'Licitação 13.303'],
    'comprasbr': ['Pregão', 'Concorrência', 'Dispensa'],
    'licitanet': ['Pregão', 'Concorrência', 'Dispensa']
}

# Mapeamento de valores das modalidades por portal
MODALIDADE_VALUES = {
    'bll': {'Pregão': '1', 'Concorrência': '2', 'Dispensa': '3', 'Licitação 13.303': '4'},
    'comprasnet': {'Pregão': '1', 'Concorrência': '2', 'Cotação': '3', 'Dispensa': '4'},
    'compraspublicas': {'Pregão': '1', 'Concorrência': '2', 'Dispensa': '3'},
    'bnc': {'Pregão': '1', 'Concorrência': '2', 'Dispensa': '3', 'Licitação 13.303': '4'},
    'comprasbr': {'Pregão': '1', 'Concorrência': '2', 'Dispensa': '3'},
    'licitanet': {'Pregão': '1', 'Concorrência': '2', 'Dispensa': '3'}
}

def fechar_popup_tour(driver, wait):
    """Função auxiliar para fechar o popup do tour se ele estiver presente"""
    try:
        # Tenta encontrar o botão de finalizar do tour
        tour_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-role='end']")))
        if tour_button:
            tour_button.click()
            time.sleep(1)  # Pequena pausa para garantir que o popup fechou
            print("Tour finalizado com sucesso!")
        return True
    except:
        return False

def verificar_aviso(driver, wait):
    """Função para verificar se apareceu o aviso de warning"""
    try:
        # Verifica se existe o título "Aviso!" e o ícone de warning
        aviso = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swal2-warning")))
        titulo = wait.until(EC.presence_of_element_located((By.ID, "swal2-title")))
        
        if aviso.is_displayed() and titulo.is_displayed() and titulo.text == "Aviso!":
            print("Aviso detectado! Pulando para o próximo registro...")
            return True
    except:
        pass
    return False

class SeletorPortal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Seletor de Portal")
        self.root.geometry("500x700")
        
        # Título
        tk.Label(
            self.root, 
            text="Selecione o Portal", 
            font=('Helvetica', 16, 'bold')
        ).pack(pady=20)
        
        # Frame para os botões com scrollbar
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas e Scrollbar
        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Estilo padrão para os botões
        button_style = {
            'width': 40,
            'height': 2,
            'font': ('Helvetica', 11),
            'pady': 5,
            'wraplength': 350
        }
        
        # Lista de portais
        portais = [
            ("BLL - Bolsa de Licitações do Brasil", "bll"),
            ("ComprasNet - Compras Governamentais", "comprasnet"),
            ("Portal de Compras Públicas", "compraspublicas"),
            ("BNC - Bolsa Nacional de Compras", "bnc"),
            ("Compras BR - Portal de Compras do Brasil", "comprasbr"),
            ("LicitaNet - Portal de Licitações", "licitanet")
        ]
        
        # Criando botões para cada portal
        for texto, comando in portais:
            tk.Button(
                scrollable_frame,
                text=texto,
                command=lambda cmd=comando, txt=texto: self.abrir_formulario(cmd, txt),
                **button_style
            ).pack(pady=10)
        
        # Empacotando o canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.root.mainloop()
        
    def abrir_formulario(self, portal_id, portal_nome):
        # Zera o arquivo JSON antes de abrir o formulário
        with open('dados.json', 'w', encoding='utf-8') as arquivo:
            json.dump({
                "portal_id": portal_id,
                "portal_nome": portal_nome,
                "registros": []
            }, arquivo, ensure_ascii=False, indent=4)
            
        self.root.destroy()  # Fecha a janela de seleção
        
        # Abre o formulário específico do portal
        if portal_id == "bll":
            FormularioBLL(portal_id, portal_nome)
        elif portal_id == "comprasnet":
            FormularioComprasNet(portal_id, portal_nome)
        elif portal_id == "compraspublicas":
            FormularioComprasPublicas(portal_id, portal_nome)
        elif portal_id == "bnc":
            FormularioBNC(portal_id, portal_nome)
        elif portal_id == "comprasbr":
            FormularioComprasBR(portal_id, portal_nome)
        elif portal_id == "licitanet":
            FormularioLicitaNet(portal_id, portal_nome)
        else:
            messagebox.showinfo("Em Desenvolvimento", f"O formulário para o portal {portal_nome} está em desenvolvimento!")
            SeletorPortal()

class FormularioBase:
    def __init__(self, portal_id, portal_nome):
        self.root = tk.Tk()
        self.root.title(f"Formulário - {portal_nome}")
        self.root.geometry("500x700")
        
        self.portal_id = portal_id
        self.portal_nome = portal_nome
        
        # Frame para os campos
        self.campos_frame = tk.Frame(self.root)
        self.campos_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Frame para os botões
        self.botoes_frame = tk.Frame(self.root)
        self.botoes_frame.pack(pady=20)
        
        # Frame para a lista
        self.lista_frame = tk.Frame(self.root)
        self.lista_frame.pack(fill='both', expand=True, padx=20)
        
        # Botões
        tk.Button(self.botoes_frame, text="Adicionar", command=self.adicionar_dados).pack(side=tk.LEFT, padx=10)
        tk.Button(self.botoes_frame, text="Enviar para Chrome", command=self.enviar_chrome).pack(side=tk.LEFT, padx=10)
        tk.Button(self.botoes_frame, text="Voltar", command=self.voltar).pack(side=tk.LEFT, padx=10)
        
        # Lista de dados
        tk.Label(self.lista_frame, text="Clique em um item para removê-lo da lista:").pack(pady=5)
        self.lista_dados = tk.Listbox(self.lista_frame, width=60, height=10)
        self.lista_dados.pack(pady=10)
        self.lista_dados.bind('<<ListboxSelect>>', self.remover_item)
        
        self.carregar_dados()
    
    def criar_campo(self, frame, label_text, tipo="entry"):
        label = tk.Label(frame, text=label_text)
        label.pack(pady=5)
        
        if tipo == "entry":
            campo = tk.Entry(frame, width=50)
        elif tipo == "combobox":
            campo = ttk.Combobox(frame, width=47, state="readonly")
            campo['values'] = MODALIDADES.get(self.portal_id, [])
        
        campo.pack(pady=5)
        return campo
    
    def carregar_dados(self):
        try:
            with open('dados.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                for registro in dados['registros']:
                    self.lista_dados.insert(tk.END, self.formato_lista(registro))
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
    
    def formato_lista(self, registro):
        # Será sobrescrito pelas classes filhas
        pass
    
    def coletar_dados(self):
        # Será sobrescrito pelas classes filhas
        pass
    
    def adicionar_dados(self):
        novo_registro = self.coletar_dados()
        if novo_registro:
            with open('dados.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            
            dados['registros'].append(novo_registro)
            
            with open('dados.json', 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            
            self.lista_dados.insert(tk.END, self.formato_lista(novo_registro))
            self.limpar_campos()
    
    def limpar_campos(self):
        # Será sobrescrito pelas classes filhas
        pass
    
    def remover_item(self, event):
        try:
            selection = self.lista_dados.curselection()
            if selection:
                index = selection[0]
                self.lista_dados.delete(index)
                
                with open('dados.json', 'r', encoding='utf-8') as arquivo:
                    dados = json.load(arquivo)
                dados['registros'].pop(index)
                with open('dados.json', 'w', encoding='utf-8') as arquivo:
                    json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao remover item: {str(e)}")
    
    def enviar_chrome(self):
        driver = None
        try:
            # Configurações do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Configurar o download automático
            prefs = {
                "download.default_directory": os.path.join(os.path.expanduser('~'), 'Downloads'),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            try:
                # Primeira tentativa: usar o ChromeDriverManager
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print("Chrome iniciado com ChromeDriverManager")
                
            except Exception as e1:
                print(f"Primeira tentativa falhou: {str(e1)}")
                try:
                    # Segunda tentativa: procurar o chromedriver no PATH
                    driver = webdriver.Chrome(options=chrome_options)
                    print("Chrome iniciado com driver do PATH")
                    
                except Exception as e2:
                    print(f"Segunda tentativa falhou: {str(e2)}")
                    try:
                        # Terceira tentativa: usar o Service sem ChromeDriverManager
                        service = Service()
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                        print("Chrome iniciado com Service padrão")
                        
                    except Exception as e3:
                        print(f"Terceira tentativa falhou: {str(e3)}")
                        # Última tentativa: especificar o caminho do chromedriver manualmente
                        import sys
                        chromedriver_path = os.path.join(os.path.dirname(sys.executable), 'chromedriver.exe')
                        service = Service(executable_path=chromedriver_path)
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                        print(f"Chrome iniciado com chromedriver em: {chromedriver_path}")
            
            if not driver:
                raise Exception("Não foi possível inicializar o Chrome")
            
            url = "https://minha.effecti.com.br/#/proposta-minhas"
            driver.get(url)
            wait = WebDriverWait(driver, 5)
            
            try:
                # Login mais rápido e direto
                email_field = wait.until(EC.presence_of_element_located((By.NAME, "input-login")))
                password_field = wait.until(EC.presence_of_element_located((By.NAME, "input-password")))
                
                # Preenche email e senha de uma vez
                email_field.send_keys("fernanda@alcantaramendes.com.br")
                password_field.send_keys("Alcantara@2025")
                
                # Clica no botão Entrar imediatamente
                entrar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button-submit a.login-btn.l-button")))
                entrar_button.click()
                print("Login realizado com sucesso!")
                
                # Reduz o tempo de espera e já procura o botão Cadastrar Proposta
                print("Aguardando página carregar...")
                time.sleep(3)  # Aguarda a página carregar completamente
                
                # Espera o overlay desaparecer
                try:
                    overlay = WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.overlay.fullscreen"))
                    )
                except:
                    print("Aviso: Overlay não encontrado ou já invisível")
                
                print("Procurando botão Cadastrar Proposta...")
                try:
                    # Primeira tentativa: esperar o botão estar clicável
                    cadastrar_proposta_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-new-proposal"))
                    )
                    cadastrar_proposta_button.click()
                except:
                    try:
                        # Segunda tentativa: usar JavaScript para remover overlay e clicar
                        driver.execute_script("""
                            // Remove qualquer overlay
                            var overlays = document.querySelectorAll('div.overlay');
                            overlays.forEach(function(overlay) {
                                overlay.remove();
                            });
                            
                            // Encontra e clica no botão
                            var botao = document.querySelector('button.btn-new-proposal');
                            if(botao) {
                                botao.click();
                            }
                        """)
                    except:
                        # Terceira tentativa: localizar por XPath e usar Actions
                        from selenium.webdriver.common.action_chains import ActionChains
                        button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-new-proposal')]")
                        actions = ActionChains(driver)
                        actions.move_to_element(button).click().perform()
                
                print("Iniciando cadastro de proposta...")
                
                # Fecha o popup do tour se aparecer, com tempo reduzido
                if fechar_popup_tour(driver, wait):
                    print("Tour inicial fechado!")
                
                # Carrega os dados do JSON
                with open('dados.json', 'r', encoding='utf-8') as arquivo:
                    dados = json.load(arquivo)
                
                # Seleciona portal e empresa em sequência rápida
                select_element = wait.until(EC.presence_of_element_located((By.ID, "sel-portal")))
                select = Select(select_element)
                
                # Mapeamento dos IDs dos portais
                portal_mapping = {
                    'bll': '24',
                    'comprasnet': '1',
                    'compraspublicas': '3',
                    'bnc': '1362',
                    'comprasbr': '898',
                    'licitanet': '28'
                }
                
                # Seleciona o portal
                portal_id = portal_mapping.get(dados['portal_id'])
                if portal_id:
                    select.select_by_value(portal_id)
                    print(f"Portal selecionado: {dados['portal_nome']}")
                    
                    # Seleciona a empresa Fernanda imediatamente após o portal
                    empresa_select = wait.until(EC.presence_of_element_located((By.ID, "branch")))
                    Select(empresa_select).select_by_value("1")
                    print("Empresa selecionada!")
                    
                    # Mapeamento dos campos específicos por portal
                    field_mapping = {
                        'bll': {
                            'bidding': 'sel-bidding',
                            'organ': 'sel-organ',
                            'quotation': 'sel-quotation'
                        },
                        'comprasnet': {
                            'bidding': 'sel-bidding',
                            'uasg': 'sel-organ',
                            'quotation': 'sel-quotation',
                            'uasg_name': 'sel-uasg-name'
                        },
                        'compraspublicas': {
                            'bidding': 'sel-bidding',
                            'organ': 'sel-organ',
                            'quotation': 'sel-quotation'
                        },
                        'bnc': {
                            'bidding': 'sel-bidding',
                            'organ': 'sel-organ',
                            'quotation': 'sel-quotation'
                        },
                        'comprasbr': {
                            'bidding': 'sel-bidding',
                            'organ': 'sel-organ',
                            'quotation': 'sel-quotation'
                        },
                        'licitanet': {
                            'bidding': 'sel-bidding',
                            'organ': 'sel-organ',
                            'quotation': 'sel-quotation'
                        }
                    }
                    
                    # Pega os IDs corretos para o portal atual
                    portal_fields = field_mapping.get(dados['portal_id'])
                    
                    if portal_fields:
                        fechar_popup_tour(driver, wait)
                        
                        if dados['portal_id'] == 'comprasnet':
                            try:
                                # Campo Licitação (Número da compra)
                                print("Tentando preencher campo Licitação...")
                                bidding_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['bidding'])))
                                bidding_field.click()
                                
                                # Usar valores padrão se não houver registros
                                if not dados.get('registros'):
                                    print("Nenhum registro encontrado, usando valores padrão...")
                                    edital_numero = '990012024'
                                    uasg = '980425'
                                    modalidade = 'Pregão'
                                else:
                                    edital_numero = dados['registros'][-1].get('numero_compra', '990012024')
                                    uasg = dados['registros'][-1].get('uasg', '980425')
                                    modalidade = dados['registros'][-1].get('modalidade', 'Pregão')
                                
                                bidding_field.send_keys(str(edital_numero))
                                print(f"Campo Licitação preenchido: {edital_numero}")
                                
                                # Campo UASG
                                print("Tentando preencher campo UASG...")
                                uasg_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['uasg'])))
                                uasg_field.click()
                                uasg_field.send_keys(str(uasg))
                                print(f"Campo UASG preenchido: {uasg}")
                                
                                # Modalidade
                                print("Selecionando modalidade...")
                                select_element = wait.until(EC.presence_of_element_located((By.ID, portal_fields['quotation'])))
                                select = Select(select_element)
                                modalidade_id = MODALIDADE_VALUES['comprasnet'].get(modalidade, '1')
                                select.select_by_value(modalidade_id)
                                print(f"Modalidade selecionada: {modalidade}")
                                
                            except Exception as e:
                                print(f"Erro ao preencher campos do ComprasNet: {str(e)}")
                                print("Detalhes do erro:")
                                import traceback
                                print(traceback.format_exc())
                                return
                                
                        else:
                            # Preenchimento padrão para outros portais
                            try:
                                # Campo Licitação/Edital
                                bidding_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['bidding'])))
                                bidding_field.click()
                                edital_numero = dados['registros'][-1].get('numero_edital', '')
                                bidding_field.send_keys(str(edital_numero))
                                print(f"Campo Licitação preenchido: {edital_numero}")
                                
                                # Campo Órgão
                                organ_field = wait.until(EC.presence_of_element_located((By.ID, portal_fields['organ'])))
                                organ_field.click()
                                orgao = dados['registros'][-1].get('orgao', '')
                                organ_field.send_keys(str(orgao))
                                print(f"Campo Órgão preenchido: {orgao}")
                                
                                # Modalidade
                                select_element = wait.until(EC.presence_of_element_located((By.ID, portal_fields['quotation'])))
                                select = Select(select_element)
                                modalidade = dados['registros'][-1].get('modalidade', 'Pregão')
                                modalidade_id = MODALIDADE_VALUES[dados['portal_id']].get(modalidade, '1')
                                select.select_by_value(modalidade_id)
                                print(f"Modalidade selecionada: {modalidade}")
                                
                            except Exception as e:
                                print(f"Erro ao preencher campos: {str(e)}")
                                return
                        
                        # Carregar Itens
                        print("Clicando em Carregar Itens...")
                        carregar_itens_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Carregar Itens')]")))
                        carregar_itens_button.click()
                        print("Botão Carregar Itens clicado!")
                        
                        time.sleep(2)  # Aguarda carregamento
                        
                        # Verificar aviso
                        if verificar_aviso(driver, wait):
                            print("Aviso detectado. Fechando navegador...")
                            driver.quit()
                            return
                        
                        # Scroll e exportação
                        print("Rolando a página...")
                        driver.execute_script("window.scrollBy(0, 300);")
                        time.sleep(1)  # Aguarda o scroll

                        # Após rolar, tenta fechar o span do tour
                        try:
                            print("Procurando botão finalizar do tour...")
                            finalizar_button = driver.find_element(By.CSS_SELECTOR, "div.popover.minha-tour.tour-tour-proposta-cadastro a[data-role='end']")
                            finalizar_button.click()
                            print("Tour fechado com sucesso!")
                            time.sleep(1)  # Aguarda o tour fechar
                        except Exception as e:
                            print(f"Aviso: Tour não encontrado após scroll - {str(e)}")
                        
                        # Exportar planilha
                        try:
                            print("Procurando botão Exportar planilha...")
                            exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Exportar planilha"]')))
                            driver.execute_script("arguments[0].click();", exportar)
                            print("Botão Exportar planilha clicado!")
                            
                            time.sleep(2)  # Aguarda modal abrir
                            
                            print("Procurando botão Exportar na modal...")
                            # Tenta diferentes seletores para o botão Exportar
                            try:
                                # Primeira tentativa - botão pela classe
                                confirmar_exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.modal-footer button.btn-primary")))
                            except:
                                try:
                                    # Segunda tentativa - botão pelo texto
                                    confirmar_exportar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Exportar')]")))
                                except:
                                    # Terceira tentativa - botão pela estrutura HTML fornecida
                                    confirmar_exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-v-1d2d804c] button.btn.btn-primary")))
                            
                            # Tenta clicar de diferentes formas
                            try:
                                confirmar_exportar.click()
                            except:
                                try:
                                    driver.execute_script("arguments[0].click();", confirmar_exportar)
                                except:
                                    # Última tentativa - força o clique via JavaScript
                                    driver.execute_script("""
                                        var buttons = document.querySelectorAll('button');
                                        for(var i = 0; i < buttons.length; i++) {
                                            if(buttons[i].textContent.includes('Exportar')) {
                                                buttons[i].click();
                                                break;
                                            }
                                        }
                                    """)
                            
                            print("Exportação iniciada!")
                            
                            # Aguarda o download do arquivo
                            print("Aguardando download do arquivo...")
                            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
                            timeout = 30
                            start_time = time.time()
                            
                            while time.time() - start_time < timeout:
                                # Procura por arquivos que começam com 'exportacao_' e terminam com '.xlsx'
                                files = [f for f in os.listdir(download_path) if f.startswith('exportação_') and f.endswith('.xlsx')]
                                if files:
                                    # Pega o arquivo mais recente
                                    newest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getctime)
                                    print(f"Arquivo exportado encontrado: {newest_file}")
                                    time.sleep(2)  # Garante que o arquivo terminou de ser baixado)
                                    
                                    # Após encontrar o arquivo, inicia o processamento
                                    print("\nIniciando processamento do arquivo...")
                                    from excel_processor import processar_arquivo_exportado
                                    
                                    resultado = processar_arquivo_exportado(newest_file)
                                    if resultado:
                                        print("\nArquivos gerados:")
                                        print(f"Excel processado: {resultado['excel']}")
                                        print(f"JSON gerado: {resultado['json']}")
                                        
                                        # Remove o arquivo Excel original após processamento
                                        try:
                                            os.remove(newest_file)
                                            print(f"\nArquivo Excel original removido: {newest_file}")
                                        except Exception as e:
                                            print(f"Aviso: Não foi possível remover o arquivo original: {str(e)}")
                                        
                                        # Gera o documento Word
                                        from word_processor import criar_tabela_word
                                        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'word', 'MUNDIAL PROPOSTA 447338.docx')
                                        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proposta_final.docx')
                                        
                                        # Tenta com diferentes variações do marcador
                                        marcadores = [
                                            "{{TABELA_AQUI}}",
                                            "{{tabela_aqui}}",
                                            "{TABELA_AQUI}",
                                            "{tabela_aqui}",
                                            "TABELA_AQUI",
                                            "tabela_aqui"
                                        ]
                                        
                                        documento_word = None
                                        for marcador in marcadores:
                                            print(f"\nTentando com marcador: {marcador}")
                                            documento_word = criar_tabela_word(
                                                json_file=resultado['json'],
                                                template_file=template_path,
                                                marcador_tabela=marcador,
                                                output_file=output_path
                                            )
                                            if documento_word:
                                                print(f"Documento Word gerado com sucesso usando marcador: {marcador}")
                                                break
                                        
                                        if documento_word:
                                            print(f"Documento Word gerado: {documento_word}")
                                        else:
                                            print("Não foi possível gerar o documento Word com nenhum dos marcadores tentados")
                                        
                                        print("\nProcessamento concluído com sucesso!")
                                        return {
                                            'excel': resultado['excel'],
                                            'json': resultado['json'],
                                            'word': documento_word
                                        }
                                    else:
                                        print("Erro: Não foi possível processar o arquivo Excel")
                                    
                                time.sleep(1)
                            
                            print("Tempo limite de download excedido!")
                            
                        except Exception as e:
                            print(f"Erro durante a exportação: {str(e)}")
                            print("Detalhes do erro:")
                            import traceback
                            print(traceback.format_exc())
                    
            except Exception as e:
                print(f"Erro durante o processo: {str(e)}")
                print("Detalhes do erro:")
                import traceback
                print(traceback.format_exc())
                
        except Exception as e:
            print(f"Erro ao inicializar o Chrome: {str(e)}")
            print("Detalhes do erro:")
            import traceback
            print(traceback.format_exc())
            
        finally:
            if driver:
                driver.quit()
    
    def encontrar_ultimo_excel(self):
        """Encontra o arquivo Excel mais recente na pasta de downloads."""
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        # Procura por arquivos que começam com 'exportacao_' e terminam com .xlsx
        lista_arquivos = glob.glob(os.path.join(downloads_path, 'exportacao_*.xlsx'))
        if not lista_arquivos:
            return None
        # Retorna o arquivo mais recente
        return max(lista_arquivos, key=os.path.getctime)

    def processar_excel(self, arquivo_excel):
        """Processa o arquivo Excel, modificando valores específicos."""
        try:
            # Lê o arquivo original com openpyxl engine
            print("Iniciando leitura do arquivo Excel...")
            df = pd.read_excel(arquivo_excel, engine='openpyxl')
            new_df = df.copy()

            print(f"Arquivo lido com sucesso. Colunas encontradas: {list(df.columns)}")

            # Modifica valores da terceira coluna
            if len(df.columns) > 2:
                third_column = df.columns[2]
                new_df.iloc[1:, 2] = 0
                print(f"Valores da terceira coluna ({third_column}) modificados")

            # Preenche campos "marca" e "modelo"
            colunas_lower = [col.lower() for col in new_df.columns]
            if 'marca' in colunas_lower:
                idx = colunas_lower.index('marca')
                new_df.iloc[:, idx] = 'Própria'
                print("Campo 'marca' preenchido")
            if 'modelo' in colunas_lower:
                idx = colunas_lower.index('modelo')
                new_df.iloc[:, idx] = 'Própria'
                print("Campo 'modelo' preenchido")

            # Cria o nome do arquivo modificado
            nome_base = os.path.splitext(os.path.basename(arquivo_excel))[0]
            novo_arquivo = arquivo_excel.replace('.xlsx', '_modificado.xlsx')
            
            # Salva o arquivo modificado
            print(f"Salvando arquivo modificado como: {novo_arquivo}")
            new_df.to_excel(novo_arquivo, index=False, engine='openpyxl')
            print(f"Excel processado e salvo com sucesso")
            return novo_arquivo
        except Exception as e:
            print(f"Erro ao processar Excel: {str(e)}")
            print("Detalhes do erro:")
            import traceback
            print(traceback.format_exc())
            return None

    def excel_para_json(self, arquivo_excel):
        """Converte o arquivo Excel para JSON com formato específico."""
        try:
            # Lê o arquivo Excel com openpyxl engine
            print("Iniciando conversão do Excel para JSON...")
            df = pd.read_excel(arquivo_excel, engine='openpyxl')
            
            # Prepara os dados no formato desejado
            nome_base = os.path.splitext(os.path.basename(arquivo_excel))[0]
            data = {
                "processo": nome_base,
                "colunas": list(df.columns),
                "dados": df.to_dict(orient="records")
            }
            
            # Cria o nome do arquivo JSON
            arquivo_json = arquivo_excel.replace('.xlsx', '.json')
            
            # Salva o JSON
            print(f"Salvando dados em: {arquivo_json}")
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"Arquivo JSON criado com sucesso")
            return arquivo_json
        except Exception as e:
            print(f"Erro ao converter Excel para JSON: {str(e)}")
            print("Detalhes do erro:")
            import traceback
            print(traceback.format_exc())
            return None

    def excluir_excel_temporario(self, arquivo_excel):
        """Exclui o arquivo Excel após a conversão para JSON."""
        try:
            if os.path.exists(arquivo_excel):
                os.remove(arquivo_excel)
                print(f"Arquivo Excel excluído: {arquivo_excel}")
        except Exception as e:
            print(f"Erro ao excluir arquivo Excel: {str(e)}")

    def processar_arquivo_exportado(self, arquivo_excel):
        """
        Processa o arquivo Excel exportado e prepara os dados para o Word
        """
        try:
            print(f"\nProcessando arquivo Excel: {arquivo_excel}")
            # Lê o arquivo Excel
            df = pd.read_excel(arquivo_excel, engine='openpyxl')
            
            # Remove linhas vazias
            df = df.dropna(how='all')
            
            # Processa as colunas necessárias
            dados_processados = []
            for index, row in df.iterrows():
                item = {
                    'item': row.get('Item', ''),
                    'descricao': row.get('Descrição', ''),
                    'unidade': row.get('Unidade de fornecimento', ''),
                    'quantidade': row.get('Quantidade', 0),
                    'valor_unitario': row.get('Valor Unitário', 0),
                    'valor_total': row.get('Valor Total', 0)
                }
                dados_processados.append(item)
            
            print(f"Processados {len(dados_processados)} itens do Excel")
            return dados_processados
            
        except Exception as e:
            print(f"Erro ao processar arquivo Excel: {str(e)}")
            print("Detalhes do erro:")
            import traceback
            print(traceback.format_exc())
            return None

    def gerar_documento_word(self, dados_processados, template_word=None):
        """
        Gera um documento Word com os dados processados
        """
        try:
            from docx import Document
            from docx.shared import Pt
            
            # Se não fornecido template, cria novo documento
            if template_word and os.path.exists(template_word):
                doc = Document(template_word)
                print(f"Usando template: {template_word}")
            else:
                doc = Document()
                print("Criando novo documento Word")
            
            # Adiciona tabela com os dados
            table = doc.add_table(rows=1, cols=6)
            table.style = 'Table Grid'
            
            # Cabeçalho
            header_cells = table.rows[0].cells
            headers = ['Item', 'Descrição', 'Unidade', 'Quantidade', 'Valor Unitário', 'Valor Total']
            for i, header in enumerate(headers):
                header_cells[i].text = header
            
            # Dados
            for item in dados_processados:
                row_cells = table.add_row().cells
                row_cells[0].text = str(item['item'])
                row_cells[1].text = str(item['descricao'])
                row_cells[2].text = str(item['unidade'])
                row_cells[3].text = str(item['quantidade'])
                row_cells[4].text = f"R$ {item['valor_unitario']:.2f}"
                row_cells[5].text = f"R$ {item['valor_total']:.2f}"
            
            # Salva o documento
            output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proposta_processada.docx')
            doc.save(output_file)
            print(f"\nDocumento Word gerado com sucesso: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Erro ao gerar documento Word: {str(e)}")
            print("Detalhes do erro:")
            import traceback
            print(traceback.format_exc())
            return None

    def processar_arquivo(self, arquivo_excel, arquivo_word):
        """
        Processa o arquivo Excel e gera o documento Word
        """
        try:
            print("\nIniciando processamento do arquivo...")
            
            # Processa o Excel e gera o JSON
            resultado = processar_arquivo_exportado(arquivo_excel)
            if not resultado:
                print("Erro ao processar o arquivo Excel")
                return False
            
            # Remove o arquivo Excel processado pois não será mais necessário
            try:
                os.remove(resultado['excel'])
                print(f"\nArquivo Excel original removido: {resultado['excel']}")
            except:
                pass
            
            # Lista de marcadores para tentar
            marcadores = [
                "{{TABELA_AQUI}}",
                "{{tabela_aqui}}",
                "{TABELA_AQUI}",
                "{tabela_aqui}",
                "TABELA_AQUI",
                "tabela_aqui"
            ]
            
            # Tenta gerar o documento Word com cada marcador
            for marcador in marcadores:
                print(f"\nTentando com marcador: {marcador}")
                
                # Define o nome do arquivo de saída baseado no template
                template_dir = os.path.dirname(arquivo_word)
                template_nome = os.path.basename(arquivo_word)
                nome_base = os.path.splitext(template_nome)[0]
                arquivo_saida = os.path.join(template_dir, f"{nome_base}_proposta.docx")
                
                # Gera o documento Word
                doc_gerado = criar_tabela_word(
                    resultado['json'],
                    template_file=arquivo_word,
                    marcador_tabela=marcador,
                    output_file=arquivo_saida
                )
                
                if doc_gerado:
                    print(f"Documento Word gerado com sucesso usando marcador: {marcador}")
                    print(f"Documento Word gerado: {doc_gerado}")
                    return True
                
            print("\nNão foi possível gerar o documento Word com nenhum dos marcadores tentados")
            return False
        
        except Exception as e:
            print(f"Erro durante o processamento: {str(e)}")
            return False
        finally:
            print("\nProcessamento concluído com sucesso!")

    def voltar(self):
        self.root.destroy()
        SeletorPortal()

class FormularioBLL(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_edital = self.criar_campo(self.campos_frame, "N° do Edital:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        # Configurar as opções da modalidade
        if isinstance(self.modalidade, ttk.Combobox):
            self.modalidade['values'] = MODALIDADES.get(self.portal_id, [])
            self.modalidade.set('Pregão')  # Valor padrão
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Edital: {registro['numero_edital']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_edital": self.numero_edital.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_edital.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('')

class FormularioComprasNet(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_compra = self.criar_campo(self.campos_frame, "N° da Compra:")
        self.uasg = self.criar_campo(self.campos_frame, "UASG:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Compra: {registro['numero_compra']} - UASG: {registro['uasg']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_compra": self.numero_compra.get(),
            "uasg": self.uasg.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_compra.delete(0, tk.END)
        self.uasg.delete(0, tk.END)
        self.modalidade.set('')

class FormularioComprasPublicas(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_processo = self.criar_campo(self.campos_frame, "N° do Processo:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Processo: {registro['numero_processo']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_processo": self.numero_processo.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_processo.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('')

class FormularioBNC(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_edital = self.criar_campo(self.campos_frame, "N° do Edital:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        # Configurar as opções da modalidade
        if isinstance(self.modalidade, ttk.Combobox):
            self.modalidade['values'] = MODALIDADES.get(self.portal_id, [])
            self.modalidade.set('Pregão')  # Valor padrão
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Edital: {registro['numero_edital']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_edital": self.numero_edital.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_edital.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('')

class FormularioComprasBR(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_edital = self.criar_campo(self.campos_frame, "N° do Edital:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Edital: {registro['numero_edital']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_edital": self.numero_edital.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_edital.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('')

class FormularioLicitaNet(FormularioBase):
    def __init__(self, portal_id, portal_nome):
        super().__init__(portal_id, portal_nome)
        
        self.numero_edital = self.criar_campo(self.campos_frame, "N° do Edital:")
        self.orgao = self.criar_campo(self.campos_frame, "Órgão:")
        self.modalidade = self.criar_campo(self.campos_frame, "Modalidade:", "combobox")
        
        self.root.mainloop()
    
    def formato_lista(self, registro):
        return f"Edital: {registro['numero_edital']} - Órgão: {registro['orgao']} - Modalidade: {registro['modalidade']}"
    
    def coletar_dados(self):
        return {
            "numero_edital": self.numero_edital.get(),
            "orgao": self.orgao.get(),
            "modalidade": self.modalidade.get(),
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def limpar_campos(self):
        self.numero_edital.delete(0, tk.END)
        self.orgao.delete(0, tk.END)
        self.modalidade.set('')

def processar_arquivo(arquivo_excel, arquivo_word):
    """
    Processa o arquivo Excel e gera o documento Word
    """
    try:
        print("\nIniciando processamento do arquivo...")
        
        # Processa o Excel e gera o JSON
        resultado = processar_arquivo_exportado(arquivo_excel)
        if not resultado:
            print("Erro ao processar o arquivo Excel")
            return False
            
        # Remove o arquivo Excel processado pois não será mais necessário
        try:
            os.remove(resultado['excel'])
            print(f"\nArquivo Excel original removido: {resultado['excel']}")
        except:
            pass
        
        # Define o nome do arquivo de saída baseado no template
        template_dir = os.path.dirname(arquivo_word)
        template_nome = os.path.basename(arquivo_word)
        nome_base = os.path.splitext(template_nome)[0]
        arquivo_saida = os.path.join(template_dir, f"{nome_base}_proposta.docx")
        print(f"\nGerando arquivo: {arquivo_saida}")
            
        # Tenta gerar o documento Word
        doc_gerado = criar_tabela_word(
            resultado['json'],
            template_file=arquivo_word,
            marcador_tabela="{{TABELA_AQUI}}",
            output_file=arquivo_saida
        )
            
        if doc_gerado:
            print(f"Documento Word gerado com sucesso: {doc_gerado}")
            return True
                
        print("\nNão foi possível gerar o documento Word")
        return False
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return False
    finally:
        print("\nProcessamento concluído!")

if __name__ == "__main__":
    app = SeletorPortal()
    time.sleep(50)