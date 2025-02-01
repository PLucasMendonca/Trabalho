import customtkinter as ctk
from pathlib import Path
import atexit
import logging
import sys
from UI.login_gui import LoginGUI
from UI.portal_gui import PortalGUI
from UI.pesquisa_gui import PesquisaGUI
from core.webdriver import WebDriverManager
from config.settings import THEME, KEYBOARD_SHORTCUTS
from utils.logging_config import setup_logging
import tkinter as tk
from tkinter import messagebox

logger = logging.getLogger(__name__)

class MainApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Portal de Compras")
        self.root.geometry("400x300")
        
        # Configurar tema inicial
        self.tema_atual = "light"
        self.aplicar_tema()
        
        # Criar diretório de logs se não existir
        logs_dir = Path(__file__).parent / 'logs'
        logs_dir.mkdir(exist_ok=True)
        
        self.current_window = None
        self.criar_interface()
        
        # Registrar atalhos
        self.registrar_atalhos()
        
        # Registrar função de limpeza
        atexit.register(self.cleanup)
        
        logger.info("Iniciando aplicação")
    
    def aplicar_tema(self):
        """Aplica o tema atual na interface"""
        tema = THEME[self.tema_atual]
        ctk.set_appearance_mode(self.tema_atual)
        self.root.configure(**tema)
    
    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        self.tema_atual = "dark" if self.tema_atual == "light" else "light"
        self.aplicar_tema()
        logger.info(f"Tema alterado para: {self.tema_atual}")
    
    def registrar_atalhos(self):
        """Registra os atalhos de teclado"""
        for atalho, funcao in KEYBOARD_SHORTCUTS.items():
            if hasattr(self, funcao):
                self.root.bind(atalho, lambda e, f=funcao: getattr(self, f)())
                logger.debug(f"Atalho registrado: {atalho} -> {funcao}")
    
    def mostrar_ajuda(self):
        """Mostra janela de ajuda com atalhos"""
        ajuda = "Atalhos disponíveis:\n\n"
        for atalho, funcao in KEYBOARD_SHORTCUTS.items():
            ajuda += f"{atalho}: {funcao}\n"
        
        janela_ajuda = ctk.CTkToplevel(self.root)
        janela_ajuda.title("Ajuda - Atalhos")
        janela_ajuda.geometry("300x400")
        
        texto = ctk.CTkTextbox(janela_ajuda)
        texto.pack(padx=10, pady=10, fill="both", expand=True)
        texto.insert("1.0", ajuda)
        texto.configure(state="disabled")
    
    def atualizar_interface(self):
        """Atualiza a interface atual"""
        if self.current_window:
            self.current_window.atualizar()
        logger.info("Interface atualizada")
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Portal de Compras Públicas",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Frame de botões
        botoes_frame = ctk.CTkFrame(main_frame)
        botoes_frame.pack(pady=20, fill="x")
        
        # Botões principais
        ctk.CTkButton(
            botoes_frame,
            text="Gerenciar Logins",
            command=self.abrir_login_gui
        ).pack(pady=5, fill="x")
        
        ctk.CTkButton(
            botoes_frame,
            text="Portal",
            command=self.abrir_portal_gui
        ).pack(pady=5, fill="x")
        
        ctk.CTkButton(
            botoes_frame,
            text="Pesquisar",
            command=self.abrir_pesquisa_gui
        ).pack(pady=5, fill="x")
        
        # Botão de tema
        ctk.CTkButton(
            main_frame,
            text="Alternar Tema",
            command=self.alternar_tema
        ).pack(pady=10)
        
        # Botão de ajuda
        ctk.CTkButton(
            main_frame,
            text="Ajuda (F1)",
            command=self.mostrar_ajuda
        ).pack(pady=5)
    
    def abrir_login_gui(self):
        """Abre a interface de gerenciamento de logins"""
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginGUI()
        logger.info("Interface de login aberta")
    
    def abrir_portal_gui(self):
        """Abre a interface do portal"""
        try:
            if self.current_window:
                self.current_window.destroy()
            
            # Criar nova janela para o portal
            portal_window = ctk.CTkToplevel(self.root)
            portal_window.title("Portal de Compras")
            portal_window.geometry("500x600")
            
            # Criar interface do portal
            self.current_window = PortalGUI(portal_window)
            portal_window.protocol("WM_DELETE_WINDOW", self.fechar_janela_atual)
            portal_window.grab_set()
            
            logger.info("Interface do portal aberta")
            
        except Exception as e:
            logger.error(f"Erro ao abrir interface do portal: {e}")
            messagebox.showerror("Erro", str(e))
    
    def abrir_pesquisa_gui(self):
        """Abre a interface de pesquisa"""
        if self.current_window:
            self.current_window.destroy()
        self.current_window = PesquisaGUI()
        logger.info("Interface de pesquisa aberta")
    
    def fechar_janela_atual(self):
        """Fecha a janela atual"""
        try:
            if self.current_window:
                if hasattr(self.current_window, 'root'):
                    self.current_window.root.destroy()
                self.current_window = None
            WebDriverManager.quit()
        except Exception as e:
            logger.error(f"Erro ao fechar janela: {e}")
    
    def cleanup(self):
        """Limpa recursos ao fechar a aplicação"""
        try:
            if self.current_window:
                self.current_window.destroy()
            WebDriverManager.quit()
            logger.info("Recursos limpos com sucesso")
        except Exception as e:
            logger.error(f"Erro ao limpar recursos: {e}")
    
    def on_closing(self):
        """Cleanup ao fechar a aplicação"""
        try:
            self.cleanup()
            self.root.quit()
            logger.info("Aplicação encerrada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao encerrar aplicação: {e}")
            sys.exit(1)
    
    def run(self):
        """Inicia a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # Configurar logging
    setup_logging()
    
    # Iniciar aplicação
    app = MainApp()
    app.run()