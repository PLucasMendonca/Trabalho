import customtkinter as ctk
from tkinter import messagebox
from core.webdriver import WebDriverManager
from core.credentials import CredentialsManager
from core.automation_rules import AutomationRules
from utils.validation import validate_action, validate_form_data, validate_webdriver, ValidationContext
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import PORTAL_URL, WAIT_TIMEOUT
import logging
from datetime import datetime
import threading
import json
import os

logger = logging.getLogger(__name__)

class LoadingOverlay:
    def __init__(self, parent):
        self.parent = parent
        self.overlay = None
        self.progress = None
        self.label = None
    
    def show(self, message="Carregando..."):
        """Mostra overlay com mensagem de carregamento"""
        self.overlay = ctk.CTkFrame(self.parent)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Frame central
        center_frame = ctk.CTkFrame(self.overlay)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Barra de progresso
        self.progress = ctk.CTkProgressBar(center_frame)
        self.progress.pack(pady=10, padx=20)
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        
        # Mensagem
        self.label = ctk.CTkLabel(center_frame, text=message)
        self.label.pack(pady=5)
    
    def update_message(self, message):
        """Atualiza a mensagem do overlay"""
        if self.label:
            self.label.configure(text=message)
    
    def hide(self):
        """Esconde o overlay"""
        if self.overlay:
            self.progress.stop()
            self.overlay.destroy()
            self.overlay = None

class PortalGUI(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        # Configurar frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Gerenciadores
        self.credentials_manager = CredentialsManager()
        self.driver = None
        
        # Variáveis
        self.perfil_var = ctk.StringVar(value="")
        self.uf_var = ctk.StringVar(value="Selecione")
        
        # Status
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status: Aguardando")
        self.status_label.pack(pady=(0, 10))
        
        # Overlay de carregamento
        self.loading = LoadingOverlay(self.root)
        
        # Criar barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10), padx=10, fill="x")
        self.progress_bar.pack_forget()  # Inicialmente oculta
        
        # Label para status detalhado
        self.status_detail = ctk.CTkLabel(self.main_frame, text="")
        self.status_detail.pack(pady=(0, 10), padx=10, fill="x")
        self.status_detail.pack_forget()  # Inicialmente oculta
        
        # Criar widgets
        self.criar_widgets()
        
        # Carregar perfis
        self.carregar_perfis()
        
        # Configurar layout
        self.pack(expand=True, fill="both", padx=10, pady=10)
    
    def executar_com_loading(self, func, mensagem_loading="Carregando...", *args, **kwargs):
        """Executa uma função mostrando overlay de loading"""
        def wrapper():
            try:
                self.loading.show(mensagem_loading)
                resultado = func(*args, **kwargs)
                return resultado
            except Exception as e:
                logger.error(f"Erro durante execução: {e}")
                messagebox.showerror("Erro", str(e))
                return None
            finally:
                self.loading.hide()
        
        # Executar em thread separada
        thread = threading.Thread(target=wrapper)
        thread.start()
    
    @validate_action("criar_interface")
    def criar_widgets(self):
        """Cria a interface do usuário"""
        # Título
        ctk.CTkLabel(
            self.main_frame,
            text="Automação de Pregão",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 15))
        
        # Frame para perfil de login
        login_frame = ctk.CTkFrame(self.main_frame)
        login_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            login_frame,
            text="Empresa:",
            font=("Arial", 12)
        ).pack(pady=(5, 0))
        
        self.perfil_dropdown = ctk.CTkComboBox(
            login_frame,
            variable=self.perfil_var,
            values=self.get_perfis(),
            width=300
        )
        self.perfil_dropdown.pack(pady=5)
        
        # Frame para dados do pregão
        pregao_frame = ctk.CTkFrame(self.main_frame)
        pregao_frame.pack(fill="x", padx=10, pady=10)
        
        # Título da seção
        ctk.CTkLabel(
            pregao_frame,
            text="Dados do Pregão",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Número do Pregão
        ctk.CTkLabel(pregao_frame, text="Número do Pregão:", anchor="w").pack(padx=10)
        self.numero_pregao = ctk.CTkEntry(pregao_frame, width=300)
        self.numero_pregao.pack(pady=(0, 10))
        
        # Data do Pregão
        ctk.CTkLabel(pregao_frame, text="Data do Pregão (dd/mm/aaaa):", anchor="w").pack(padx=10)
        self.data_pregao = ctk.CTkEntry(pregao_frame, width=300)
        self.data_pregao.pack(pady=(0, 10))
        
        # UF
        ctk.CTkLabel(pregao_frame, text="UF:", anchor="w").pack(padx=10)
        self.uf_dropdown = ctk.CTkComboBox(
            pregao_frame,
            variable=self.uf_var,
            values=self.get_ufs(),
            width=300
        )
        self.uf_dropdown.pack(pady=(0, 10))
        
        # Órgão
        ctk.CTkLabel(pregao_frame, text="Órgão:", anchor="w").pack(padx=10)
        self.orgao = ctk.CTkEntry(pregao_frame, width=300)
        self.orgao.pack(pady=(0, 10))
        
        # Frame para botões
        botoes_frame = ctk.CTkFrame(self.main_frame)
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        # Botões lado a lado com mesmo tamanho
        ctk.CTkButton(
            botoes_frame,
            text="Iniciar Automação",
            command=lambda: self.executar_com_loading(self.iniciar_automacao, "Iniciando automação..."),
            width=140,
            font=("Arial", 12)
        ).pack(side="left", padx=5, expand=True)
        
        ctk.CTkButton(
            botoes_frame,
            text="Parar Automação",
            command=self.parar_automacao,
            width=140,
            font=("Arial", 12)
        ).pack(side="right", padx=5, expand=True)
    
    def get_ufs(self):
        """Retorna lista de UFs"""
        return [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
            "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
            "SP", "SE", "TO"
        ]
    
    @validate_action("get_perfis")
    def get_perfis(self):
        """Retorna lista de perfis disponíveis"""
        credentials = self.credentials_manager.get_credentials()
        return list(credentials.get("empresas", {}).keys())
    
    def validar_data(self, data_str):
        """Valida o formato da data"""
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            return None
    
    @validate_action("iniciar_automacao")
    def iniciar_automacao(self):
        """Inicia o processo de automação"""
        with ValidationContext("iniciar_automacao"):
            # Validar campos
            perfil = self.perfil_var.get()
            numero = self.numero_pregao.get().strip()
            data = self.data_pregao.get().strip()
            uf = self.uf_var.get()
            orgao = self.orgao.get().strip()
            
            # Validações obrigatórias
            if not perfil:
                messagebox.showerror("Erro", "Selecione um perfil!")
                return
            
            if not numero:
                messagebox.showerror("Erro", "Informe o número do pregão!")
                return
            
            if not self.validar_data(data):
                messagebox.showerror("Erro", "Data inválida! Use o formato dd/mm/aaaa")
                return
            
            # Validar credenciais
            credenciais = self.credentials_manager.get_empresa(perfil)
            if not credenciais:
                messagebox.showerror("Erro", "Credenciais não encontradas!")
                return
            
            try:
                # Mostrar barra de progresso e status
                self.progress_bar.pack()
                self.status_detail.pack()
                self.progress_bar.set(0)
                self.update_status("Iniciando automação...", 0)
                
                # Iniciar WebDriver
                self.driver = WebDriverManager.get_driver()
                self.update_status("WebDriver iniciado com sucesso", 10)
                
                # Realizar login
                self.update_status("Realizando login...", 20)
                AutomationRules.realizar_login(self.driver, credenciais)
                self.update_status("Login realizado com sucesso", 40)
                
                # Realizar pesquisa
                self.update_status("Pesquisando pregão...", 60)
                
                # Preparar parâmetros opcionais
                uf_value = uf if uf != "Selecione" else None
                orgao_value = orgao if orgao.strip() else None
                
                if not AutomationRules.pesquisar_pregao(
                    driver=self.driver,
                    numero_pregao=numero,
                    data=data,
                    uf=uf_value,
                    orgao=orgao_value
                ):
                    raise Exception("Erro ao pesquisar pregão")
                self.update_status("Pregão encontrado com sucesso", 80)

                # Registrar proposta
                self.update_status("Registrando proposta...", 90)
                
                # Carregar configurações
                with open("json/credentials.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                    empresa_atual = config["empresas"].get(perfil, {})
                    caminho_relativo = empresa_atual.get("caminho_anexo", "core/docs/a.pdf")
                    is_mei = empresa_atual.get("usuario_mei", "não").lower() == "sim"
                
                # Converter para caminho absoluto
                arquivo_pdf = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), caminho_relativo))
                
                if not AutomationRules.registrar_proposta(self.driver, arquivo_pdf=arquivo_pdf, is_mei=is_mei):
                    raise Exception("Erro ao registrar proposta. Verifique o log para mais detalhes.")
                self.update_status("Proposta registrada com sucesso", 95)
                
                # Finalizar
                self.update_status("Automação concluída com sucesso!", 100)
                messagebox.showinfo("Sucesso", "Automação iniciada com sucesso!")
                self.status_label.configure(text="Status: Automação em execução")
                
            except Exception as e:
                logger.error(f"Erro ao iniciar automação: {e}")
                self.update_status(f"Erro: {str(e)}", 0)
                messagebox.showerror("Erro", str(e))
                self.status_label.configure(text="Status: Erro na automação")
            finally:
                # Ocultar barra de progresso após 3 segundos
                self.schedule_hide_progress()
    
    def update_status(self, message, progress):
        """Atualiza status e barra de progresso"""
        self.status_detail.configure(text=message)
        self.progress_bar.set(progress / 100)
        self.root.update()  # Força atualização da interface
    
    def hide_progress(self):
        """Oculta barra de progresso e status"""
        self.progress_bar.pack_forget()
        self.status_detail.pack_forget()
        
    def schedule_hide_progress(self):
        """Agenda ocultação da barra de progresso"""
        self.root.after(3000, self.hide_progress)
    
    @validate_action("parar_automacao")
    def parar_automacao(self):
        """Para o processo de automação"""
        try:
            WebDriverManager.quit()
            self.status_label.configure(text="Status: Automação parada")
            messagebox.showinfo("Sucesso", "Automação parada com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao parar automação: {e}")
            messagebox.showerror("Erro", str(e))
    
    def carregar_perfis(self):
        """Carrega perfis"""
        self.perfil_dropdown.configure(values=self.get_perfis())
    
    def atualizar(self):
        """Atualiza a interface do portal"""
        try:
            # Recarregar credenciais
            self.credentials_manager.load_credentials()
            
            # Atualizar combobox de usuários
            self.carregar_perfis()
            
            logger.info("Interface do portal atualizada")
        except Exception as e:
            logger.error(f"Erro ao atualizar interface do portal: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar interface: {e}")
