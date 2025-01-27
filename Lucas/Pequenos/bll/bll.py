from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    try:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Descomente para executar em modo headless
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        return driver
    except Exception as e:
        logger.error(f"Erro ao inicializar o driver: {str(e)}")
        raise

def inserir_senha(driver, senha, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        for digito in senha:
            # Aguardar até que os botões estejam visíveis
            botoes = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@type='button']"))
            )
            
            # Localizar o botão correto com base nos valores
            botao_encontrado = False
            for botao in botoes:
                valores = botao.get_attribute("value")
                if digito in valores:
                    wait.until(EC.element_to_be_clickable(botao))
                    botao.click()
                    botao_encontrado = True
                    break
            
            if not botao_encontrado:
                raise ValueError(f"Botão para o dígito {digito} não encontrado")
            
    except TimeoutException:
        logger.error("Timeout ao aguardar elementos na página")
        raise
    except Exception as e:
        logger.error(f"Erro ao inserir senha: {str(e)}")
        raise

def main():
    driver = None
    try:
        driver = setup_driver()
        
        # Configurar URL do site
        URL_SITE = "https://bllcompras.com/Home/Login"  # Substitua pela URL real
        driver.get(URL_SITE)
        logger.info("Página carregada com sucesso")

        # Aguardar e preencher email
        wait = WebDriverWait(driver, 10)
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        email_input.send_keys("minhakamizeta@gmail.com")
        logger.info("Email preenchido")

        # Inserir senha
        senha = "457688"  # Substitua pela senha real
        inserir_senha(driver, senha)
        logger.info("Senha inserida")

        # Clicar no botão de login
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]"))
        )
        login_button.click()
        logger.info("Login realizado com sucesso")

        # Aguardar o modal de seleção de perfil
        logger.info("Aguardando modal de seleção de perfil...")
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-data"))
        )

        # Aguardar um pouco para a tabela carregar completamente
        driver.implicitly_wait(2)
        
        # Encontrar a tabela de perfis
        table = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-data"))
        )
        
        # Encontrar todas as linhas da tabela, excluindo o cabeçalho
        rows = table.find_elements(By.XPATH, ".//tbody/tr[position()>1]")
        
        if not rows:
            logger.warning("Nenhum perfil encontrado!")
            resposta = input("Deseja tentar entrar em outro perfil? (s/n): ")
            if resposta.lower() != 's':
                logger.info("Operação cancelada pelo usuário")
                return
        
        perfil_selecionado = None
        # Procura apenas por "OPERADOR"
        for row in rows:
            try:
                # Pegar as células da linha
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    nome_perfil = cells[0].text.strip()
                    status = cells[1].text.strip()
                    
                    logger.info(f"Verificando perfil: {nome_perfil} (Status: {status})")
                    
                    if status.upper() == "SIM" and "OPERADOR" in nome_perfil.upper():
                        perfil_selecionado = row
                        logger.info(f"Perfil OPERADOR encontrado: {nome_perfil}")
                        break
            except Exception as e:
                logger.warning(f"Erro ao verificar perfil: {str(e)}")
                continue

        if perfil_selecionado:
            try:
                botao_selecionar = perfil_selecionado.find_element(By.XPATH, ".//td[@class='tablebutton']/a")
                nome_selecionado = perfil_selecionado.find_elements(By.TAG_NAME, "td")[0].text.strip()
                logger.info(f"Selecionando perfil: {nome_selecionado}")
                botao_selecionar.click()
                logger.info("Perfil selecionado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao clicar no perfil: {str(e)}")
                raise
        else:
            logger.error("Nenhum perfil OPERADOR ativo encontrado")
            resposta = input("Deseja tentar entrar em outro perfil? (s/n): ")
            if resposta.lower() != 's':
                logger.info("Operação cancelada pelo usuário")
                return

    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise
    finally:
        if driver:
            try:
                # Mantém o navegador aberto até pressionar Enter
                input("Pressione Enter para fechar o navegador...")
            finally:
                #driver.quit()
                logger.info("Driver fechado")

if __name__ == "__main__":
    main()
