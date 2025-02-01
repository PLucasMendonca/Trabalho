import customtkinter as ctk
from tkinter import messagebox
from core.credentials import CredentialsManager
import logging

logger = logging.getLogger(__name__)

class LoginGUI:
    def __init__(self):
        self.root = ctk.CTkToplevel()
        self.root.title("Gerenciar Logins")
        self.root.geometry("600x700")
        
        # Inicializar gerenciador de credenciais
        self.credentials_manager = CredentialsManager()
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Criar widgets
        self.criar_widgets()
        
        # Cleanup ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.grab_set()
    
    def criar_widgets(self):
        """Cria a interface do usuário"""
        # Título
        ctk.CTkLabel(
            self.main_frame,
            text="Gerenciar Credenciais",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Frame para os campos
        campos_frame = ctk.CTkFrame(self.main_frame)
        campos_frame.pack(pady=20, padx=20, fill="x")
        
        # Nome do Perfil
        ctk.CTkLabel(
            campos_frame,
            text="Nome do Perfil:",
            font=("Arial", 12)
        ).pack(anchor="w", pady=(5,0))
        self.nome_perfil = ctk.CTkEntry(campos_frame, width=300)
        self.nome_perfil.pack(fill="x", pady=(0, 10))
        
        # Usuário
        ctk.CTkLabel(
            campos_frame,
            text="Usuário:",
            font=("Arial", 12)
        ).pack(anchor="w", pady=(5,0))
        self.usuario = ctk.CTkEntry(campos_frame, width=300)
        self.usuario.pack(fill="x", pady=(0, 10))
        
        # Senha
        ctk.CTkLabel(
            campos_frame,
            text="Senha:",
            font=("Arial", 12)
        ).pack(anchor="w", pady=(5,0))
        self.senha = ctk.CTkEntry(campos_frame, width=300, show="*")
        self.senha.pack(fill="x", pady=(0, 10))
        
        # Checkbox MEI
        self.mei_var = ctk.BooleanVar()
        self.mei_checkbox = ctk.CTkCheckBox(
            campos_frame,
            text="Usuário MEI",
            variable=self.mei_var,
            font=("Arial", 12)
        )
        self.mei_checkbox.pack(anchor="w", pady=(5,10))
        
        # Frame para os botões
        botoes_frame = ctk.CTkFrame(self.main_frame)
        botoes_frame.pack(pady=10, padx=20, fill="x")
        
        # Botão Salvar
        ctk.CTkButton(
            botoes_frame,
            text="Salvar",
            command=self.salvar_credenciais,
            width=120
        ).pack(side="left", padx=5)
        
        # Botão Excluir
        ctk.CTkButton(
            botoes_frame,
            text="Excluir",
            command=self.excluir_credenciais,
            width=120,
            fg_color="red",
            hover_color="darkred"
        ).pack(side="left", padx=5)
        
        # Botão Limpar
        ctk.CTkButton(
            botoes_frame,
            text="Limpar",
            command=self.limpar_campos,
            width=120
        ).pack(side="left", padx=5)
        
        # Lista de Perfis
        ctk.CTkLabel(
            self.main_frame,
            text="Perfis Salvos:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20,5))
        
        # Frame scrollável para perfis
        self.perfis_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=300,
            height=150
        )
        self.perfis_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Atualizar lista de perfis
        self.atualizar_lista_perfis()
    
    def salvar_credenciais(self):
        """Salva as credenciais de uma empresa"""
        try:
            # Obter dados do formulário
            nome = self.nome_perfil.get().strip()
            usuario = self.usuario.get().strip()
            senha = self.senha.get().strip()
            is_mei = self.mei_var.get()
            
            # Validar campos
            if not nome or not usuario or not senha:
                messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")
                return
            
            # Salvar credenciais
            if self.credentials_manager.add_empresa(nome, usuario, senha, is_mei):
                # Limpar campos
                self.usuario.delete(0, "end")
                self.senha.delete(0, "end")
                self.nome_perfil.delete(0, "end")
                self.mei_var.set(False)
                
                # Atualizar lista
                self.atualizar_lista_perfis()
                
                messagebox.showinfo("Sucesso", "Credenciais salvas com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro ao salvar credenciais: {e}")
            messagebox.showerror("Erro", "Erro ao salvar credenciais")
    
    def excluir_credenciais(self):
        """Exclui as credenciais de uma empresa"""
        try:
            # Validar nome do perfil
            nome = self.nome_perfil.get().strip()
            if not nome:
                messagebox.showwarning("Atenção", "Digite o nome do perfil para excluir!")
                return
            
            # Confirmar exclusão
            if not messagebox.askyesno("Confirmar", f"Deseja realmente excluir o perfil {nome}?"):
                return
            
            # Excluir credenciais
            if self.credentials_manager.remove_empresa(nome):
                # Limpar campos
                self.limpar_campos()
                
                # Atualizar lista
                self.atualizar_lista_perfis()
                
                messagebox.showinfo("Sucesso", "Credenciais excluídas com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Perfil não encontrado!")
            
        except Exception as e:
            logger.error(f"Erro ao excluir credenciais: {e}")
            messagebox.showerror("Erro", "Erro ao excluir credenciais")
    
    def carregar_credenciais(self, value):
        """Carrega as credenciais de uma empresa"""
        try:
            # Obter nome do perfil selecionado
            if not value:
                return
            
            # Remover indicador MEI e espaços extras
            nome = value.split(" (MEI)")[0].strip() if "(MEI)" in value else value.strip()
            
            # Buscar credenciais
            perfil = self.credentials_manager.get_empresa(nome)
            if not perfil:
                logger.warning(f"Perfil {nome} não encontrado")
                messagebox.showwarning("Atenção", f"Perfil {nome} não encontrado")
                return
            
            # Preencher campos
            self.limpar_campos()
            self.nome_perfil.insert(0, nome)
            self.usuario.insert(0, perfil.get("login", ""))
            self.senha.insert(0, perfil.get("senha", ""))
            self.mei_var.set(perfil.get("usuario_mei", "não").lower() == "sim")
            
            logger.info(f"Credenciais do perfil {nome} carregadas com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar credenciais: {e}")
            messagebox.showerror("Erro", "Erro ao carregar credenciais")
    
    def widget_exists(self, widget):
        """Verifica se um widget ainda existe e é válido"""
        try:
            return widget.winfo_exists()
        except:
            return False
    
    def atualizar_lista_perfis(self):
        """Atualiza a lista de perfis"""
        try:
            # Limpar frame atual
            for widget in self.perfis_frame.winfo_children():
                widget.destroy()
            
            # Obter credenciais
            credenciais = self.credentials_manager.get_credentials()
            empresas = credenciais.get("empresas", {})
            
            if not empresas:
                # Mostrar mensagem quando não há perfis
                ctk.CTkLabel(
                    self.perfis_frame,
                    text="Nenhum perfil cadastrado",
                    font=("Arial", 12, "italic"),
                    text_color="gray"
                ).pack(pady=10)
                return
            
            # Criar botões para cada perfil
            for nome, dados in empresas.items():
                # Determinar se é MEI
                is_mei = dados.get("usuario_mei", "não").lower() == "sim"
                display_name = f"{nome} (MEI)" if is_mei else nome
                
                # Criar botão
                btn = ctk.CTkButton(
                    self.perfis_frame,
                    text=display_name,
                    command=lambda n=display_name: self.carregar_credenciais(n),
                    width=250
                )
                btn.pack(pady=2)
                
                # Criar tooltip
                self.criar_tooltip(btn, f"Clique para carregar as credenciais de {display_name}")
            
            logger.info("Lista de perfis atualizada com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar lista de perfis: {e}")
            messagebox.showerror("Erro", "Erro ao atualizar lista de perfis")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        try:
            # Limpar campos de texto com segurança
            for campo in ['nome_perfil', 'usuario', 'senha']:
                try:
                    if hasattr(self, campo):
                        widget = getattr(self, campo)
                        if self.widget_exists(widget):
                            widget.delete(0, "end")
                except Exception as e:
                    logger.error(f"Erro ao limpar campo {campo}: {e}")
            
            # Desmarcar checkbox MEI com segurança
            try:
                if hasattr(self, 'mei_var'):
                    self.mei_var.set(False)
            except Exception as e:
                logger.error(f"Erro ao limpar checkbox MEI: {e}")
            
            # Remover seleção da lista com segurança
            try:
                if hasattr(self, 'perfis_frame') and self.widget_exists(self.perfis_frame):
                    for widget in self.perfis_frame.winfo_children():
                        if isinstance(widget, ctk.CTkButton) and self.widget_exists(widget):
                            widget.configure(fg_color="transparent")
            except Exception as e:
                logger.error(f"Erro ao limpar seleção da lista: {e}")
            
            logger.debug("Campos limpos com sucesso")
        except Exception as e:
            logger.error(f"Erro ao limpar campos: {e}")
    
    def criar_tooltip(self, widget, text):
        """Cria um tooltip para um widget"""
        def show_tooltip(event):
            tooltip = ctk.CTkToplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ctk.CTkLabel(
                tooltip,
                text=text,
                font=("Arial", 10),
                fg_color=("gray85", "gray25"),
                corner_radius=6
            )
            label.pack(padx=4, pady=4)
            
            def hide_tooltip():
                tooltip.destroy()
            
            tooltip.bind("<Leave>", lambda e: hide_tooltip())
            widget.bind("<Leave>", lambda e: hide_tooltip())
        
        widget.bind("<Enter>", show_tooltip)
    
    def atualizar(self):
        """Atualiza a interface de login"""
        try:
            # Recarregar credenciais
            self.credentials_manager.load_credentials()
            
            # Atualizar lista de perfis
            self.atualizar_lista_perfis()
            
            # Limpar campos
            self.limpar_campos()
            
            logger.info("Interface de login atualizada")
        except Exception as e:
            logger.error(f"Erro ao atualizar interface de login: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar interface: {e}")
    
    def destroy(self):
        """Método para destruir a janela"""
        if hasattr(self, 'root'):
            self.root.destroy()
    
    def on_closing(self):
        """Cleanup ao fechar a janela"""
        try:
            self.destroy()
        except Exception as e:
            logger.error(f"Erro ao fechar janela: {e}")
