import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from tkinter import messagebox
from config.settings import SEARCH_HISTORY_FILE

logger = logging.getLogger(__name__)

class PesquisaGUI:
    def __init__(self):
        self.root = ctk.CTkToplevel()
        self.root.title("Pesquisa Automatizada")
        self.root.geometry("800x600")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Criar widgets
        self.criar_widgets()
        
        # Cleanup ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
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
    
    def criar_widgets(self):
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Pesquisa em Páginas", 
            font=("Arial", 20)
        ).pack(pady=10)
        
        # Frame para os campos
        campos_frame = ctk.CTkFrame(self.main_frame)
        campos_frame.pack(pady=20, padx=20, fill="x")
        
        # URL
        ctk.CTkLabel(campos_frame, text="URL da Página").pack(anchor="w")
        self.url = ctk.CTkEntry(campos_frame)
        self.url.pack(fill="x", pady=(0, 10))
        
        # Elemento de Busca
        ctk.CTkLabel(campos_frame, text="Elemento HTML (opcional)").pack(anchor="w")
        self.elemento = ctk.CTkEntry(campos_frame)
        self.elemento.pack(fill="x", pady=(0, 10))
        
        # Texto de Busca
        ctk.CTkLabel(campos_frame, text="Texto para Buscar").pack(anchor="w")
        self.texto_busca = ctk.CTkEntry(campos_frame)
        self.texto_busca.pack(fill="x", pady=(0, 10))
        
        # Botão de Pesquisa
        ctk.CTkButton(
            self.main_frame,
            text="Iniciar Pesquisa",
            command=self.pesquisar,
            width=200
        ).pack(pady=20)
        
        # Área de resultados
        self.resultado_text = ctk.CTkTextbox(self.main_frame, height=200)
        self.resultado_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.root.grab_set()  # Torna a janela modal
        
    def aceitar_cookies(self, driver):
        try:
            # Aguardar o botão de aceitar cookies aparecer e clicar nele
            wait = WebDriverWait(driver, 10)
            botao_cookies = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar todos os cookies')]"))
            )
            botao_cookies.click()
            return True
        except Exception as e:
            print(f"Erro ao aceitar cookies: {str(e)}")
            return False

    def pesquisar(self):
        if not self.url.get().strip():
            self.resultado_text.insert("1.0", "URL é obrigatória!\n")
            return
            
        try:
            # Configuração do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            
            # Inicializar o driver
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Abrir a URL
            driver.get(self.url.get())
            
            # Tentar aceitar cookies se necessário
            self.aceitar_cookies(driver)
            
            # Aguardar carregamento
            wait = WebDriverWait(driver, 10)
            
            # Se houver elemento específico
            if self.elemento.get().strip():
                elementos = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.elemento.get()))
                )
                
                resultados = []
                for elem in elementos:
                    if self.texto_busca.get().lower() in elem.text.lower():
                        resultados.append(elem.text)
                
                self.resultado_text.delete("1.0", "end")
                if resultados:
                    self.resultado_text.insert("1.0", "Resultados encontrados:\n\n")
                    for res in resultados:
                        self.resultado_text.insert("end", f"{res}\n\n")
                else:
                    self.resultado_text.insert("1.0", "Nenhum resultado encontrado.")
            
            else:
                # Busca em toda a página
                page_source = driver.page_source.lower()
                if self.texto_busca.get().lower() in page_source:
                    self.resultado_text.delete("1.0", "end")
                    self.resultado_text.insert("1.0", "Texto encontrado na página!")
                else:
                    self.resultado_text.delete("1.0", "end")
                    self.resultado_text.insert("1.0", "Texto não encontrado.")
            
        except Exception as e:
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", f"Erro durante a pesquisa: {str(e)}")
            
        finally:
            driver.quit()

    def atualizar(self):
        """Atualiza a interface de pesquisa"""
        try:
            # Recarregar histórico de pesquisas
            self.carregar_historico()
            
            # Atualizar comboboxes
            self.atualizar_comboboxes()
            
            # Limpar campos de entrada
            self.limpar_campos()
            
            logger.info("Interface de pesquisa atualizada")
        except Exception as e:
            logger.error(f"Erro ao atualizar interface de pesquisa: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar interface: {e}")

    def carregar_historico(self):
        """Recarrega o histórico de pesquisas"""
        try:
            with open(SEARCH_HISTORY_FILE, 'r', encoding='utf-8') as f:
                self.historico = json.load(f)
            logger.debug("Histórico de pesquisas carregado")
        except FileNotFoundError:
            self.historico = {}
            logger.warning("Arquivo de histórico não encontrado")
        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {e}")
            self.historico = {}

    def atualizar_comboboxes(self):
        """Atualiza os valores das comboboxes"""
        try:
            # Atualizar UFs
            self.uf_combobox.configure(values=self.get_ufs())
            
            # Atualizar órgãos baseado no histórico
            orgaos = list(set(item['orgao'] for items in self.historico.values() 
                            for item in items if 'orgao' in item))
            if self.orgao_combobox:
                self.orgao_combobox.configure(values=sorted(orgaos))
            
            logger.debug("Comboboxes atualizadas")
        except Exception as e:
            logger.error(f"Erro ao atualizar comboboxes: {e}")

    def limpar_campos(self):
        """Limpa os campos de entrada"""
        try:
            if hasattr(self, 'numero_pregao_entry'):
                self.numero_pregao_entry.delete(0, 'end')
            if hasattr(self, 'data_pregao_entry'):
                self.data_pregao_entry.delete(0, 'end')
            if hasattr(self, 'orgao_combobox'):
                self.orgao_combobox.set('')
            if hasattr(self, 'uf_combobox'):
                self.uf_combobox.set('')
            
            logger.debug("Campos limpos")
        except Exception as e:
            logger.error(f"Erro ao limpar campos: {e}")
