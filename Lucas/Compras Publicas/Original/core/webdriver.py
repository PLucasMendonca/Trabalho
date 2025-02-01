import os
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from config.settings import CHROME_OPTIONS, WAIT_TIMEOUT, RETRY_ATTEMPTS
import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_exception(retries=RETRY_ATTEMPTS, delay=1):
    """Decorator para retry em caso de erro"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:  # Última tentativa
                        logger.error(f"Erro após {retries} tentativas: {e}")
                        raise
                    logger.warning(f"Tentativa {attempt + 1} falhou: {e}. Tentando novamente...")
                    time.sleep(delay * (attempt + 1))  # Backoff exponencial
            return None
        return wrapper
    return decorator

class WebDriverManager:
    _instance = None
    
    @classmethod
    def get_driver(cls):
        """
        Retorna uma instância única do WebDriver (Singleton Pattern)
        """
        if cls._instance is None:
            try:
                # Configurar opções do Chrome
                options = uc.ChromeOptions()
                
                # Forçar versão específica do ChromeDriver
                version_main = 131  # Versão atual do Chrome
                
                # Adicionar extensão Buster
                extension_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'extensions', 'buster.crx')
                if os.path.exists(extension_path):
                    options.add_extension(extension_path)
                    logger.info("Extensão Buster carregada com sucesso")
                else:
                    logger.error(f"Arquivo da extensão Buster não encontrado em: {extension_path}")
                
                # Outras opções
                options.add_argument('--start-maximized')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--disable-popup-blocking')
                options.add_argument('--disable-notifications')
                
                # Preferências de download
                prefs = {
                    "download.default_directory": os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads'),
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True
                }
                options.add_experimental_option("prefs", prefs)
                
                # Adicionar opções do settings.py
                for option in CHROME_OPTIONS:
                    options.add_argument(option)
                
                # Criar uma nova instância do Chrome
                cls._instance = uc.Chrome(
                    options=options,
                    version_main=version_main,
                    driver_executable_path=None,  # Força o download da versão correta
                    browser_executable_path=None  # Usa o Chrome padrão instalado
                )
                logger.info("WebDriver iniciado com sucesso")
                
            except Exception as e:
                logger.error(f"Erro ao inicializar WebDriver: {e}")
                raise
                
        return cls._instance
    
    @classmethod
    @retry_on_exception()
    def wait_for_element(cls, by, value, timeout=WAIT_TIMEOUT):
        """
        Aguarda um elemento estar presente e visível
        """
        try:
            driver = cls.get_driver()
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            if not element.is_displayed():
                raise TimeoutException(f"Elemento {value} não está visível")
            return element
        except TimeoutException as e:
            logger.error(f"Timeout esperando elemento {value}: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao aguardar elemento {value}: {e}")
            raise
    
    @classmethod
    def quit(cls):
        """
        Fecha o WebDriver e limpa a instância
        """
        try:
            if cls._instance:
                cls._instance.quit()
                cls._instance = None
                logger.info("WebDriver fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar WebDriver: {e}")
            cls._instance = None  # Limpar mesmo em caso de erro
