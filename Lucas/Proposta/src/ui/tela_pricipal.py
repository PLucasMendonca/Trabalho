import tkinter as tk
from tkinter import ttk
import subprocess
from datetime import datetime
import os
import threading
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from src.processors.fila_processor import FilaProcessor
from src.processors.navegador_processor import NavegadorProcessor
from src.processors.direto_api import ProcessadorAPI
from src.bitrix.run_bitrix import run_bitrix
from src.utils.constantes import MODALIDADES
import time

# Mapeamento de nomes de portais
PORTAL_MAPPING = {
    "ComprasNet": "comprasnet",
    "Compras Públicaas": "compraspublicas",
    "BNC - Bolsa Nacional de Compras": "bnc",
    "ComprasBR": "comprasbr",
    "Licitanet": "licitanet",
    "BLL": "bll"
}

# Portais disponíveis para processamento
PORTAIS_DISPONIVEIS = list(MODALIDADES.keys())

class TelaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Propostas")
        self.root.state('zoomed')  # Maximiza a janela
        
        # Definir cores
        self.bg_color = "#f0f0f0"
        self.frame_bg = "#ffffff"
        self.highlight_color = "#f5f5f5"
        
        self.root.configure(bg=self.bg_color)
        
        # Frame principal que conterá os painéis
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configurar o grid
        self.main_frame.grid_columnconfigure(0, weight=1)  # Controle: 25%
        self.main_frame.grid_columnconfigure(1, weight=2)  # Fila/Resultados: 50%
        self.main_frame.grid_columnconfigure(2, weight=1)  # Saída: 25%
        
        # Configurar as linhas para a coluna do meio
        self.main_frame.grid_rowconfigure(0, weight=2)  # Fila: 66%
        self.main_frame.grid_rowconfigure(1, weight=1)  # Resultados: 33%
        
        # Inicializar processador de fila
        self.fila_processor = FilaProcessor()
        
        # Inicializar processador de navegador
        self.navegador_processor = None
        self.driver = None

        # Criar os painéis
        self.criar_painel_controle()   # Coluna 0
        self.criar_painel_fila()       # Coluna 1, Linha 0
        self.criar_painel_resultados() # Coluna 1, Linha 1
        self.criar_painel_saida()      # Coluna 2
        
        # Inicializar dados
        self.dados_json = None
        self.cards_data = []
        self.output_buffer = []
        self.processando = False
        self.deve_parar = False
        
        # Pilha para cards com portais disponíveis
        self.pilha_portais_disponiveis = []
        self.aguardando_instrucoes = False

    def criar_painel_controle(self):
        """Cria o painel de controle com os botões"""
        frame = tk.LabelFrame(self.main_frame, text="Controle", bg=self.frame_bg)
        frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Frame para os botões
        btn_frame = tk.Frame(frame, bg=self.frame_bg)
        btn_frame.pack(expand=True)
        
        # Botão Iniciar
        self.btn_iniciar = tk.Button(
            btn_frame,
            text="Iniciar Processamento",
            command=self.iniciar_processamento,
            width=20,
            height=2
        )
        self.btn_iniciar.pack(pady=10)
        
        # Botão Parar
        self.btn_parar = tk.Button(
            btn_frame,
            text="Parar Processamento",
            command=self.parar_processamento,
            width=20,
            height=2,
            state=tk.DISABLED
        )
        self.btn_parar.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(
            btn_frame,
            text="Status: Aguardando",
            bg=self.frame_bg
        )
        self.status_label.pack(pady=10)
        
    def criar_painel_fila(self):
        """Cria o painel que mostra a fila de processamento"""
        frame = tk.LabelFrame(self.main_frame, text="Fila de Processamento", bg=self.frame_bg)
        frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Lista de itens com scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.fila_list = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            bg=self.frame_bg,
            font=('Consolas', 10)
        )
        self.fila_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.fila_list.yview)
        
        # Contador de itens na fila
        self.contador_fila = tk.Label(
            frame,
            text="Itens na fila: 0",
            bg=self.frame_bg
        )
        self.contador_fila.pack(pady=5)
        
    def criar_painel_resultados(self):
        """Cria o painel que mostra os resultados do processamento"""
        frame = tk.LabelFrame(self.main_frame, text="Resultados", bg=self.frame_bg)
        frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        
        # Lista de resultados com scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resultados_list = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            bg=self.frame_bg,
            font=('Consolas', 10)
        )
        self.resultados_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resultados_list.yview)
        
        # Contador de resultados
        self.contador_resultados = tk.Label(
            frame,
            text="Total de resultados: 0",
            bg=self.frame_bg
        )
        self.contador_resultados.pack(pady=5)
        
    def criar_painel_saida(self):
        """Cria o painel que mostra os logs e prints"""
        frame = tk.LabelFrame(self.main_frame, text="Saída", bg=self.frame_bg)
        frame.grid(row=0, column=2, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Área de texto para output com scrollbars
        text_frame = tk.Frame(frame, bg=self.frame_bg)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(text_frame, orient="vertical")
        hsb = ttk.Scrollbar(text_frame, orient="horizontal")
        
        self.output_area = tk.Text(
            text_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='white',
            fg='black',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configurar as tags para diferentes tipos de mensagem
        self.output_area.tag_configure('error', foreground='red')
        self.output_area.tag_configure('success', foreground='green')
        self.output_area.tag_configure('info', foreground='blue')
        
        # Layout dos componentes
        self.output_area.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configurar o redimensionamento
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        vsb.config(command=self.output_area.yview)
        hsb.config(command=self.output_area.xview)
        
    def iniciar_processamento(self):
        """Inicia o processamento executando o script de informações gerais"""
        if self.processando:
            return
            
        self.processando = True
        self.deve_parar = False
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Processando...")
        
        # Limpar áreas de saída
        self.output_area.delete('1.0', tk.END)
        self.fila_list.delete(0, tk.END)
        self.resultados_list.delete(0, tk.END)
        self.contador_fila.config(text="Itens na fila: 0")
        self.contador_resultados.config(text="Total de resultados: 0")
        
        # Executar processo do Bitrix em uma thread separada
        self.adicionar_log("Iniciando processamento do Bitrix...")
        thread = threading.Thread(target=self.executar_bitrix)
        thread.daemon = True
        thread.start()
        
    def executar_bitrix(self):
        """Executa o processo do Bitrix"""
        try:
            # Executar o processo do Bitrix
            self.dados_json = run_bitrix()
            
            if self.dados_json:
                self.root.after(0, lambda: self.adicionar_log("Dados do Bitrix obtidos com sucesso!", "success"))
                self.root.after(0, self.carregar_dados)
            else:
                self.root.after(0, lambda: self.adicionar_log("Erro ao obter dados do Bitrix", "error"))
                self.root.after(0, lambda: self.finalizar_processamento("Erro ao obter dados do Bitrix"))
                
        except Exception as e:
            self.root.after(0, lambda: self.adicionar_log(f"Erro ao executar processo do Bitrix: {str(e)}", "error"))
            self.root.after(0, lambda: self.finalizar_processamento("Erro ao executar processo do Bitrix"))
            
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        self.adicionar_log("Carregando dados do arquivo JSON...")
        
        try:
            # Primeiro carregar os dados do JSON
            self.fila_processor.dados_json = self.dados_json
            
            # Depois carregar os cards aceitos
            self.cards_data = self.fila_processor.carregar_cards_aceitos(
                callback_log=self.adicionar_log
            )
            
            if self.cards_data:
                self.adicionar_log(f"\nTotal de cards aceitos: {len(self.cards_data)}")
                self.processar_cards_aceitos()
            else:
                self.finalizar_processamento("Nenhum card em estado 'ACEITAS' encontrado")
        except Exception as e:
            self.adicionar_log(f"Erro ao carregar cards: {str(e)}", "error")
            self.finalizar_processamento("Erro ao carregar cards")

    def processar_cards_aceitos(self):
        """Processa os cards aceitos e adiciona à fila"""
        # Adicionar à fila
        for card in self.cards_data:
            texto = f"Pregão: {card.get('pregao', 'N/A')} | Portal: {card.get('portal', 'N/A')} | Empresa: {card.get('empresa', 'N/A')}"
            self.fila_list.insert(tk.END, texto)
            
        # Atualizar contador da fila
        total_fila = len(self.cards_data)
        self.contador_fila.config(text=f"Itens na fila: {total_fila}")
        
        # Processar cada item da fila
        self.processar_proximo_item()
        
    def verificar_campos_obrigatorios(self, item):
        """Verifica se o card possui todos os campos obrigatórios"""
        campos_obrigatorios = {
            'portal': 'Portal',
            'pregao': 'Número do Pregão',
            'ao_estimado_orgao': 'AO ESTIMADO ÓRGÃO'
            #'modalidade': 'Modalidade'
        }
        
        campos_faltantes = []
        
        # Verificar portal
        portal = item.get('portal', '')
        portal_key = PORTAL_MAPPING.get(portal)
        if not portal_key or portal_key not in PORTAIS_DISPONIVEIS:
            campos_faltantes.append('Portal (inválido)')
            
        # Verificar outros campos
        for campo, nome in campos_obrigatorios.items():
            if campo != 'portal':  # Portal já foi verificado
                valor = item.get(campo)
                if not valor or valor == 'N/A':
                    campos_faltantes.append(nome)
        
        return campos_faltantes

    def processar_proximo_item(self):
        """Processa o próximo item da fila e adiciona ao resultado"""
        if self.deve_parar:
            self.finalizar_processamento("Processamento interrompido pelo usuário")
            return
            
        if not self.cards_data:
            # Todos os cards foram processados
            if self.pilha_portais_disponiveis:
                self.adicionar_log("\nProcessamento da fila principal concluído.", "success")
                self.adicionar_log(f"Existem {len(self.pilha_portais_disponiveis)} cards com portais disponíveis.", "info")
                self.iniciar_processamento_selenium()
            else:
                self.finalizar_processamento("Processamento concluído")
            return
            
        # Pegar próximo item
        item = self.cards_data.pop(0)
        
        # Tentar processar via API primeiro
        processador = ProcessadorAPI(callback_log=self.adicionar_log)
        processado_api = processador.processar_portal(item)
        
        if processado_api:
            # Se processou via API, adiciona aos resultados
            texto = f"ID: {item.get('ID', 'N/A')} | Pregão: {item.get('Número do Pregão', 'N/A')} | Portal: {item.get('portal', 'N/A')} | Status: Processado via API"
            self.resultados_list.insert(tk.END, texto)
        else:
            # Se não processou via API, verifica campos obrigatórios
            campos_faltantes = self.verificar_campos_obrigatorios(item)
            if campos_faltantes:
                # Campos faltantes
                self.adicionar_log(f"Card inválido - ID {item.get('ID', 'N/A')} - Campos faltantes: {', '.join(campos_faltantes)}", "error")
                
                # Adicionar aos resultados
                texto = f"ID: {item.get('ID', 'N/A')} | Pregão: {item.get('Número do Pregão', 'N/A')} | Portal: {item.get('portal', 'N/A')} | Status: Campos faltantes"
                self.resultados_list.insert(tk.END, texto)
            else:
                # Se tem todos os campos mas não processou via API, adiciona à pilha de portais
                self.adicionar_log(f"Card válido encontrado: ID {item.get('ID', 'N/A')} - {PORTAL_MAPPING.get(item.get('portal', 'N/A'), 'N/A')}", "info")
                self.pilha_portais_disponiveis.append(item)
            
        # Atualizar contador de resultados
        total_resultados = self.resultados_list.size()
        self.contador_resultados.config(text=f"Total de resultados: {total_resultados}")
        
        # Atualizar contador da fila
        self.contador_fila.config(text=f"Itens na fila: {len(self.cards_data)}")
        
        # Remover da fila visual
        self.fila_list.delete(0)
        
        # Processar próximo item após 1 segundo
        if not self.deve_parar:
            self.root.after(1000, self.processar_proximo_item)

    def adicionar_log(self, mensagem, tipo="info"):
        """Adiciona uma mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        texto = f"[{timestamp}] {mensagem}\n"
        
        self.output_area.insert(tk.END, texto, tipo)
        self.output_area.see(tk.END)
        
    def parar_processamento(self):
        """Para o processamento atual"""
        self.deve_parar = True
        self.status_label.config(text="Status: Parando...")
        
    def finalizar_processamento(self, mensagem):
        """Finaliza o processamento e atualiza a interface"""
        self.processando = False
        self.deve_parar = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Aguardando")
        
        # Fechar o Firefox se estiver aberto
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            
        self.adicionar_log(mensagem)
        
    def iniciar_processamento_selenium(self):
        """Inicia o processamento com Selenium"""
        try:
            self.adicionar_log("\nIniciando processamento via API...", "info")
            
            # Tentar processar via API primeiro
            from src.processors.direto_api import ProcessadorAPI
            processador = ProcessadorAPI(callback_log=self.adicionar_log)
            
            while self.pilha_portais_disponiveis:
                item = self.pilha_portais_disponiveis[0]  # Pega o primeiro sem remover
                
                if processador.processar_portal(item):
                    # Se processou com sucesso, remove da pilha e continua
                    self.pilha_portais_disponiveis.pop(0)
                    continue
                    
                # Se falhou, inicia o Firefox para este item
                self.status_label.config(text="Status: Iniciando Firefox...")
                
                # Configurar Firefox
                firefox_options = Options()
                firefox_options.add_argument('--start-maximized')
                
                # Inicializar driver
                self.driver = webdriver.Firefox(
                    service=Service(GeckoDriverManager().install()),
                    options=firefox_options
                )
                
                # Inicializar processador de navegador
                self.navegador_processor = NavegadorProcessor(self.driver)
                
                # Pegar os cards da pilha
                cards = self.pilha_portais_disponiveis
                self.pilha_portais_disponiveis = []
                
                # Atualizar interface
                self.adicionar_log("Firefox iniciado com sucesso!", "success")
                self.status_label.config(text="Status: Processando com Firefox...")
                
                # Processar cada card
                for card in cards:
                    if self.deve_parar:
                        break
                        
                    self.adicionar_log(f"\nProcessando pregão {card.get('pregao', 'N/A')}...", "info")
                    if self.navegador_processor.processar_card(card):
                        self.adicionar_log(f"Pregão {card.get('pregao', 'N/A')} processado com sucesso!", "success")
                    else:
                        self.adicionar_log(f"Erro ao processar pregão {card.get('pregao', 'N/A')}", "error")
                        
                    # Aguardar um pouco entre os cards
                    time.sleep(2)
                
                self.finalizar_processamento("Processamento com Firefox concluído")
                
        except Exception as e:
            self.adicionar_log(f"Erro ao iniciar Firefox: {str(e)}", "error")
            if self.driver:
                self.driver.quit()