import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AcaoEspecificaGUI:
    def __init__(self):
        self.window = ctk.CTkToplevel()
        self.window.title("Ações Específicas")
        self.window.geometry("800x600")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Ações em Elementos HTML", 
            font=("Arial", 20)
        ).pack(pady=10)
        
        # Frame para os campos
        campos_frame = ctk.CTkFrame(self.main_frame)
        campos_frame.pack(pady=20, padx=20, fill="x")
        
        # URL
        ctk.CTkLabel(campos_frame, text="URL da Página").pack(anchor="w")
        self.url = ctk.CTkEntry(campos_frame)
        self.url.pack(fill="x", pady=(0, 10))
        
        # Seletor do Elemento
        ctk.CTkLabel(campos_frame, text="Seletor CSS do Elemento").pack(anchor="w")
        self.seletor = ctk.CTkEntry(campos_frame)
        self.seletor.pack(fill="x", pady=(0, 10))
        
        # Tipo de Ação
        ctk.CTkLabel(campos_frame, text="Ação").pack(anchor="w")
        self.acao = ctk.CTkOptionMenu(
            campos_frame,
            values=["Clicar", "Preencher", "Obter Texto"]
        )
        self.acao.pack(fill="x", pady=(0, 10))
        
        # Valor (para preenchimento)
        ctk.CTkLabel(campos_frame, text="Valor (para preenchimento)").pack(anchor="w")
        self.valor = ctk.CTkEntry(campos_frame)
        self.valor.pack(fill="x", pady=(0, 10))
        
        # Botão de Execução
        ctk.CTkButton(
            self.main_frame,
            text="Executar Ação",
            command=self.executar_acao,
            width=200
        ).pack(pady=20)
        
        # Área de resultados
        self.resultado_text = ctk.CTkTextbox(self.main_frame, height=200)
        self.resultado_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.window.grab_set()  # Torna a janela modal
        
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

    def executar_acao(self):
        if not self.url.get().strip() or not self.seletor.get().strip():
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", "URL e seletor são obrigatórios!")
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
            
            # Aguardar carregamento do elemento
            wait = WebDriverWait(driver, 10)
            elemento = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.seletor.get()))
            )
            
            # Executar ação selecionada
            acao_selecionada = self.acao.get()
            
            if acao_selecionada == "Clicar":
                elemento.click()
                self.resultado_text.delete("1.0", "end")
                self.resultado_text.insert("1.0", "Clique executado com sucesso!")
                
            elif acao_selecionada == "Preencher":
                if not self.valor.get().strip():
                    self.resultado_text.delete("1.0", "end")
                    self.resultado_text.insert("1.0", "Valor é obrigatório para preenchimento!")
                    return
                    
                elemento.clear()
                elemento.send_keys(self.valor.get())
                self.resultado_text.delete("1.0", "end")
                self.resultado_text.insert("1.0", "Campo preenchido com sucesso!")
                
            elif acao_selecionada == "Obter Texto":
                texto = elemento.text
                self.resultado_text.delete("1.0", "end")
                self.resultado_text.insert("1.0", f"Texto obtido:\n\n{texto}")
            
        except Exception as e:
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", f"Erro durante a execução: {str(e)}")
            
        finally:
            driver.quit()
