from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
import time
from abc import ABC, abstractmethod

class PortalLicitacao(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    @abstractmethod
    def fazer_login(self, usuario, senha):
        pass
    
    @abstractmethod
    def buscar_licitacoes(self, criterios):
        pass
    
    @abstractmethod
    def dar_lance(self, id_licitacao, valor):
        pass

class PortalBLL(PortalLicitacao):
    def fazer_login(self, usuario, senha):
        try:
            # Elementos específicos do portal BLL
            self.wait.until(EC.presence_of_element_located((By.ID, "Email"))).send_keys(usuario)
            self.wait.until(EC.presence_of_element_located((By.ID, "Senha"))).send_keys(senha)
            self.wait.until(EC.element_to_be_clickable((By.ID, "btn-login"))).click()
            logger.info("Login realizado com sucesso no portal BLL")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer login no portal BLL: {str(e)}")
            return False

    def buscar_licitacoes(self, criterios):
        try:
            # Implementar busca específica para BLL
            logger.info("Buscando licitações no portal BLL")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar licitações no BLL: {str(e)}")
            return []

    def dar_lance(self, id_licitacao, valor):
        try:
            # Implementar lance específico para BLL
            logger.info(f"Lance dado no portal BLL: R$ {valor}")
            return True
        except Exception as e:
            logger.error(f"Erro ao dar lance no BLL: {str(e)}")
            return False

class PortalBNC(PortalLicitacao):
    def fazer_login(self, usuario, senha):
        try:
            # Elementos específicos do portal BNC
            self.wait.until(EC.presence_of_element_located((By.ID, "usuario"))).send_keys(usuario)
            self.wait.until(EC.presence_of_element_located((By.ID, "senha"))).send_keys(senha)
            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-login"))).click()
            logger.info("Login realizado com sucesso no portal BNC")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer login no portal BNC: {str(e)}")
            return False

    def buscar_licitacoes(self, criterios):
        try:
            # Implementar busca específica para BNC
            logger.info("Buscando licitações no portal BNC")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar licitações no BNC: {str(e)}")
            return []

    def dar_lance(self, id_licitacao, valor):
        try:
            # Implementar lance específico para BNC
            logger.info(f"Lance dado no portal BNC: R$ {valor}")
            return True
        except Exception as e:
            logger.error(f"Erro ao dar lance no BNC: {str(e)}")
            return False

class LicitacaoBot:
    def __init__(self):
        self.setup_logger()
        self.setup_driver()
        self.portal = None
        
    def setup_logger(self):
        logger.add("logs/bot.log", rotation="500 MB")
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def set_portal(self, portal_nome):
        """Define qual portal será utilizado"""
        if portal_nome == "BLL":
            self.portal = PortalBLL(self.driver)
        elif portal_nome == "BNC":
            self.portal = PortalBNC(self.driver)
        else:
            raise ValueError(f"Portal não suportado: {portal_nome}")
        
    def login(self, portal_url, usuario, senha):
        """Realiza login no portal selecionado"""
        try:
            if not self.portal:
                raise ValueError("Portal não selecionado. Use set_portal() primeiro.")
                
            self.driver.get(portal_url)
            return self.portal.fazer_login(usuario, senha)
        except Exception as e:
            logger.error(f"Erro ao acessar portal: {str(e)}")
            return False
            
    def monitorar_licitacoes(self, criterios):
        """Monitora licitações baseado nos critérios definidos"""
        try:
            if not self.portal:
                raise ValueError("Portal não selecionado. Use set_portal() primeiro.")
                
            return self.portal.buscar_licitacoes(criterios)
        except Exception as e:
            logger.error(f"Erro ao monitorar licitações: {str(e)}")
            return []
            
    def analisar_preco(self, valor_atual, valor_minimo):
        """Analisa se o preço atual está dentro dos parâmetros aceitáveis"""
        return valor_atual > valor_minimo
    
    def dar_lance(self, id_licitacao, valor):
        """Realiza um lance na licitação"""
        try:
            if not self.portal:
                raise ValueError("Portal não selecionado. Use set_portal() primeiro.")
                
            return self.portal.dar_lance(id_licitacao, valor)
        except Exception as e:
            logger.error(f"Erro ao dar lance: {str(e)}")
            return False
            
    def finalizar(self):
        """Encerra o bot e fecha o navegador"""
        try:
            self.driver.quit()
            logger.info("Bot finalizado")
        except:
            pass  # Ignora erros ao fechar o navegador
