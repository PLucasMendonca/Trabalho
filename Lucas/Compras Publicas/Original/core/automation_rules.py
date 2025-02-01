"""
Módulo responsável pelas regras de negócio da automação.
Contém os seletores HTML e as regras de navegação do portal.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
import re
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class AutomationRules:
    """Classe que contém as regras de negócio e seletores para automação"""
    
    # URLs do portal
    PORTAL_URLS = {
        'login': 'https://operacao.portaldecompraspublicas.com.br/18/loginext/',
        'pregoes': 'https://operacao.portaldecompraspublicas.com.br/4/Pregoes/'
    }
    
    # Constantes de tempo de espera
    WAIT_TIMEOUT = 10
    
    # Seletores para cookies e elementos gerais
    GENERAL_SELECTORS = {
        'aceitar_cookies': {
            'type': By.XPATH,
            'value': '//*[@id="onetrust-accept-btn-handler"]',
            'description': 'Botão de aceitar cookies'
        }
    }
    
    # Seletores para login
    LOGIN_SELECTORS = {
        'usuario': {
            'type': By.XPATH,
            'value': '//*[@id="nome"]',
            'description': 'Campo de usuário'
        },
        'senha': {
            'type': By.XPATH,
            'value': '//*[@id="senha"]',
            'description': 'Campo de senha'
        },
        'botao_entrar': {
            'type': By.XPATH,
            'value': '//*[@id="login"]/div[3]/input',
            'description': 'Botão de login'
        },
        'menu_logado': {
            'type': By.CLASS_NAME,
            'value': 'menuBlock',
            'description': 'Menu que aparece após login'
        }
    }
    
    # Constantes para os seletores do formulário de pesquisa
    PREGAO_SELECTORS = {
        'form': '//form[@id="defaultForm2"]',
        'numero': {
            'value': '//input[@id="ttBusca"]',
            'label': 'Processo'
        },
        'data': {
            'value': '//input[@id="ttAbertura"]',
            'label': 'Abertura'
        },
        'uf': {
            'value': '//select[@id="slCD_UF"]',
            'label': 'UF'
        },
        'objeto': {
            'value': '//input[@id="ttObjeto"]',
            'label': 'Objeto'
        },
        'orgao': {
            'value': '//input[@id="ttOrgao"]',
            'label': 'Órgão'
        },
        'modalidade': {
            'value': '//select[@id="slCD_MODALIDADE_LICITACAO"]',
            'label': 'Modalidade'
        },
        'realizacao': {
            'value': '//select[@id="slCD_TIPO_REALIZACAO_LICITACAO"]',
            'label': 'Realização'
        },
        'julgamento': {
            'value': '//select[@id="slCD_TIPO_JULGAMENTO_LICITACAO"]',
            'label': 'Julgamento'
        },
        'grupo_material': {
            'value': '//select[@id="slCD_GRUPO_MATERIAL"]',
            'label': 'Grupo de Fornecimento'
        },
        'linha_material': {
            'value': '//select[@id="slCD_CLASSE_MATERIAL"]',
            'label': 'Linha de Fornecimento'
        },
        'tratamento': {
            'value': '//select[@id="slCD_TRATAMENTO_DIFERENCIADO"]',
            'label': 'Tratamento Diferenciado'
        },
        'status': {
            'value': '//select[@id="ttSTATUS"]',
            'label': 'Status'
        },
        'data_inicial': {
            'value': '//input[@id="ttDATA_INICIAL"]',
            'label': 'Período (Data Inicial)'
        },
        'data_final': {
            'value': '//input[@id="ttDATA_FINAL"]',
            'label': 'Período (Data Final)'
        },
        'botao_pesquisar': {
            'value': '//input[@name="btPesquisar"]',
            'label': 'Buscar'
        },
        'resultado_pesquisa': {
            'value': 'searchTableSorter',
            'label': 'Tabela de Resultados'
        }
    }
    
    # Seletores para declarações e proposta
    DECLARACOES_SELECTORS = {
        'guia_declaracoes': {
            'type': By.XPATH,
            'value': '//*[@id="GrupoDeclaracoes"]/a',
            'description': 'Link para abrir declarações'
        },
        'form_declaracoes': {
            'type': By.ID,
            'value': 'defaultForm',
            'description': 'Formulário de declarações'
        },
        'validade_proposta': {
            'type': By.ID,
            'value': 'ttPRAZO_VALIDADE',
            'description': 'Campo de validade da proposta'
        },
        'radio_mei_sim': {
            'type': By.ID,
            'value': 'radioIt1',
            'description': 'Radio button MEI - Sim'
        },
        'radio_mei_nao': {
            'type': By.ID,
            'value': 'radioIt2',
            'description': 'Radio button MEI - Não'
        },
        'salvar_declaracoes': {
            'type': By.CSS_SELECTOR,
            'value': 'input[value="Salvar Declarações"]',
            'description': 'Botão salvar declarações'
        }
    }
    
    # Métodos utilitários para interação com elementos
    @staticmethod
    def wait_and_click(driver, selector, timeout=10, description=None):
        """
        Espera um elemento ficar clicável e clica nele de forma segura
        
        Args:
            driver: Instância do WebDriver
            selector: Tupla com (By.TIPO, "valor") ou dicionário com type e value
            timeout: Tempo máximo de espera
            description: Descrição do elemento para logs
        """
        try:
            if isinstance(selector, dict):
                by, value = selector['type'], selector['value']
            else:
                by, value = selector

            desc = description or f"elemento {value}"
            logger.info(f"Aguardando {desc}...")
            
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            
            # Tentar diferentes métodos de clique
            try:
                element.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", element)
                except:
                    driver.execute_script("arguments[0].dispatchEvent(new Event('click'));", element)
            
            logger.info(f"Clique em {desc} realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao clicar em {desc}: {str(e)}")
            return False

    @staticmethod
    def wait_and_fill(driver, selector, value, timeout=10, description=None):
        """
        Espera um elemento ficar visível e preenche seu valor
        
        Args:
            driver: Instância do WebDriver
            selector: Tupla com (By.TIPO, "valor") ou dicionário com type e value
            value: Valor a ser preenchido
            timeout: Tempo máximo de espera
            description: Descrição do elemento para logs
        """
        try:
            if isinstance(selector, dict):
                by, value_selector = selector['type'], selector['value']
            else:
                by, value_selector = selector

            desc = description or f"campo {value_selector}"
            logger.info(f"Preenchendo {desc} com valor: {value}")
            
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value_selector))
            )
            
            element.clear()
            element.send_keys(value)
            logger.info(f"Campo {desc} preenchido com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao preencher {desc}: {str(e)}")
            return False

    @staticmethod
    def check_all_boxes(driver, selector="input[type='checkbox']", timeout=10):
        """
        Marca todas as checkboxes encontradas
        
        Args:
            driver: Instância do WebDriver
            selector: Seletor CSS para encontrar as checkboxes
            timeout: Tempo máximo de espera
        """
        try:
            logger.info("Verificando e marcando checkboxes...")
            checkboxes = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            
            total = len(checkboxes)
            marcadas = 0
            
            for checkbox in checkboxes:
                if not checkbox.is_selected():
                    try:
                        driver.execute_script("arguments[0].click();", checkbox)
                        marcadas += 1
                        time.sleep(0.5)
                    except Exception as e:
                        logger.warning(f"Erro ao marcar checkbox {checkbox.get_attribute('name')}: {str(e)}")
            
            logger.info(f"Checkboxes processadas: {total} total, {marcadas} marcadas")
            return True
        except Exception as e:
            logger.error(f"Erro ao processar checkboxes: {str(e)}")
            return False

    @staticmethod
    def select_radio_option(driver, name, value, timeout=10, description=None):
        """
        Seleciona uma opção em um grupo de radio buttons
        
        Args:
            driver: Instância do WebDriver
            name: Nome do grupo de radio buttons
            value: Valor a ser selecionado
            timeout: Tempo máximo de espera
            description: Descrição opcional para logs
        """
        try:
            desc = description or f"radio button {name}={value}"
            logger.info(f"Selecionando {desc}...")
            selector = f"input[type='radio'][name='{name}'][value='{value}']"
            
            radio = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            if not radio.is_selected():
                driver.execute_script("arguments[0].click();", radio)
                time.sleep(1)
                logger.info(f"{desc} selecionado com sucesso")
            else:
                logger.info(f"{desc} já estava selecionado")
            return True
        except Exception as e:
            logger.error(f"Erro ao selecionar {desc}: {str(e)}")
            return False

    @staticmethod
    def wait_for_visibility(driver, selector, timeout=10, description=None):
        """
        Espera um elemento ficar visível
        
        Args:
            driver: Instância do WebDriver
            selector: Tupla com (By.TIPO, "valor") ou dicionário com type e value
            timeout: Tempo máximo de espera
            description: Descrição do elemento para logs
        """
        try:
            if isinstance(selector, dict):
                by, value = selector['type'], selector['value']
            else:
                by, value = selector

            desc = description or f"elemento {value}"
            logger.info(f"Aguardando visibilidade de {desc}...")
            
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            
            logger.info(f"{desc} está visível")
            return element
        except Exception as e:
            logger.error(f"Erro ao aguardar visibilidade de {desc}: {str(e)}")
            return None

    @staticmethod
    def esperar_elemento(driver, selector, timeout=10):
        """
        Espera um elemento ficar visível e clicável
        
        :param driver: Instância do WebDriver
        :param selector: Dicionário com type e value do seletor
        :param timeout: Tempo máximo de espera em segundos
        :return: Elemento web quando encontrado
        """
        try:
            elemento = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((selector['type'], selector['value']))
            )
            logger.debug(f"Elemento encontrado: {selector['description']}")
            return elemento
        except Exception as e:
            logger.error(f"Erro ao esperar elemento {selector['description']}: {e}")
            raise
    
    @staticmethod
    def preencher_campo(driver, selector, valor):
        """
        Preenche um campo de forma segura
        
        :param driver: Instância do WebDriver
        :param selector: Dicionário com type e value do seletor
        :param valor: Valor a ser preenchido
        """
        try:
            elemento = AutomationRules.esperar_elemento(driver, selector)
            elemento.clear()
            elemento.send_keys(valor)
            logger.debug(f"Campo {selector['description']} preenchido com: {valor}")
        except Exception as e:
            logger.error(f"Erro ao preencher campo {selector['description']}: {e}")
            raise
    
    @staticmethod
    def clicar_elemento(driver, selector):
        """
        Clica em um elemento de forma segura
        
        :param driver: Instância do WebDriver
        :param selector: Dicionário com type e value do seletor
        """
        try:
            elemento = AutomationRules.esperar_elemento(driver, selector)
            elemento.click()
            logger.debug(f"Clique realizado em: {selector['description']}")
        except Exception as e:
            logger.error(f"Erro ao clicar em {selector['description']}: {e}")
            raise
    
    @staticmethod
    def aceitar_cookies(driver):
        """
        Aceita os cookies do portal
        
        :param driver: Instância do WebDriver
        """
        try:
            # Esperar botão de cookies aparecer (com timeout menor pois nem sempre aparece)
            elemento = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    AutomationRules.GENERAL_SELECTORS['aceitar_cookies']['type'],
                    AutomationRules.GENERAL_SELECTORS['aceitar_cookies']['value']
                ))
            )
            elemento.click()
            logger.info("Cookies aceitos com sucesso")
        except Exception as e:
            # Não levantar erro pois o botão pode não aparecer em algumas situações
            logger.warning(f"Botão de cookies não encontrado: {e}")
    
    @staticmethod
    def realizar_login(driver, credenciais):
        """
        Realiza o login no portal
        
        :param driver: Instância do WebDriver
        :param credenciais: Dicionário com login e senha
        """
        try:
            # Navegar para a página de login
            driver.get(AutomationRules.PORTAL_URLS['login'])
            logger.info("Navegando para página de login")
            
            # Aguardar página carregar completamente
            time.sleep(3)
            
            # Aceitar cookies se aparecer
            AutomationRules.aceitar_cookies(driver)
            
            # Esperar e preencher usuário com retry
            max_tentativas = 3
            for tentativa in range(max_tentativas):
                try:
                    # Aguardar campo de usuário ficar visível e interativo
                    wait = WebDriverWait(driver, 10)
                    campo_usuario = wait.until(
                        EC.presence_of_element_located((
                            AutomationRules.LOGIN_SELECTORS['usuario']['type'],
                            AutomationRules.LOGIN_SELECTORS['usuario']['value']
                        ))
                    )
                    
                    # Garantir que o campo está visível
                    driver.execute_script("arguments[0].scrollIntoView(true);", campo_usuario)
                    time.sleep(0.5)
                    
                    # Limpar e preencher
                    campo_usuario.clear()
                    campo_usuario.send_keys(credenciais['login'])
                    logger.info("Campo usuário preenchido com sucesso")
                    break
                except Exception as e:
                    if tentativa == max_tentativas - 1:
                        raise
                    logger.warning(f"Tentativa {tentativa + 1} falhou: {str(e)}")
                    time.sleep(2)
            
            # Esperar e preencher senha com retry
            for tentativa in range(max_tentativas):
                try:
                    # Aguardar campo de senha ficar visível e interativo
                    campo_senha = wait.until(
                        EC.presence_of_element_located((
                            AutomationRules.LOGIN_SELECTORS['senha']['type'],
                            AutomationRules.LOGIN_SELECTORS['senha']['value']
                        ))
                    )
                    
                    # Garantir que o campo está visível
                    driver.execute_script("arguments[0].scrollIntoView(true);", campo_senha)
                    time.sleep(0.5)
                    
                    # Limpar e preencher
                    campo_senha.clear()
                    campo_senha.send_keys(credenciais['senha'])
                    logger.info("Campo senha preenchido com sucesso")
                    break
                except Exception as e:
                    if tentativa == max_tentativas - 1:
                        raise
                    logger.warning(f"Tentativa {tentativa + 1} falhou: {str(e)}")
                    time.sleep(2)
            
            # Esperar e clicar no botão com retry
            for tentativa in range(max_tentativas):
                try:
                    # Aguardar botão ficar clicável
                    botao_entrar = wait.until(
                        EC.element_to_be_clickable((
                            AutomationRules.LOGIN_SELECTORS['botao_entrar']['type'],
                            AutomationRules.LOGIN_SELECTORS['botao_entrar']['value']
                        ))
                    )
                    
                    # Garantir que o botão está visível
                    driver.execute_script("arguments[0].scrollIntoView(true);", botao_entrar)
                    time.sleep(0.5)
                    
                    # Clicar
                    botao_entrar.click()
                    logger.info("Botão de login clicado com sucesso")
                    break
                except Exception as e:
                    if tentativa == max_tentativas - 1:
                        raise
                    logger.warning(f"Tentativa {tentativa + 1} falhou: {str(e)}")
                    time.sleep(2)
            
            # Aguardar login ser completado
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((
                        AutomationRules.LOGIN_SELECTORS['menu_logado']['type'],
                        AutomationRules.LOGIN_SELECTORS['menu_logado']['value']
                    ))
                )
                logger.info("Login realizado com sucesso")
            except Exception as e:
                logger.error("Erro ao verificar se login foi completado")
                raise
                
        except Exception as e:
            logger.error(f"Erro ao realizar login: {str(e)}")
            raise
    
    @staticmethod
    def pesquisar_pregao(driver, numero_pregao, data=None, uf=None, orgao=None):
        """
        Pesquisa um pregão específico e baixa seu edital
        
        Args:
            driver: WebDriver do Selenium
            numero_pregao: Número do pregão
            data: Data de abertura no formato dd/mm/aaaa (opcional)
            uf: UF do pregão (opcional)
            orgao: Órgão do pregão (opcional)
        """
        try:
            logger.info(f"Iniciando pesquisa do pregão {numero_pregao}")
            
            # Navegar para a página de pregões
            logger.info("Navegando para página de pregões")
            driver.get("https://operacao.portaldecompraspublicas.com.br/4/Pregoes/")
            
            # Aguardar carregamento da página com timeout maior
            logger.info("Aguardando carregamento da página...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "ttBusca"))
            )
            
            # Pequena pausa para garantir que a página carregou completamente
            time.sleep(2)
            
            # Preencher campo de processo (número do pregão)
            logger.info("Preenchendo campo de processo...")
            campo_processo = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "ttBusca"))
            )
            campo_processo.clear()
            campo_processo.send_keys(numero_pregao)
            
            # Preencher data de abertura se fornecida
            if data:
                logger.info("Preenchendo data de abertura...")
                try:
                    # Primeiro tenta preencher diretamente
                    campo_data = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "ttAbertura"))
                    )
                    campo_data.clear()
                    
                    # Usa JavaScript para definir o valor e disparar eventos
                    script = """
                        var element = document.querySelector("#ttAbertura");
                        element.value = arguments[0];
                        element.dispatchEvent(new Event('change', { bubbles: true }));
                        element.dispatchEvent(new Event('blur', { bubbles: true }));
                    """
                    driver.execute_script(script, data)
                    
                    # Pequena pausa para garantir que o datepicker processou o valor
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Erro ao preencher data: {str(e)}")
                    return False
            
            # Selecionar UF se fornecida
            if uf:
                logger.info(f"Selecionando UF: {uf}")
                select_uf = Select(WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "slCD_UF"))
                ))
                # Encontrar o value correto para a UF
                for option in select_uf.options:
                    if option.text == uf:
                        select_uf.select_by_value(option.get_attribute("value"))
                        break
            
            # Preencher órgão se fornecido
            if orgao:
                logger.info("Preenchendo órgão...")
                campo_orgao = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "ttOrgao"))
                )
                campo_orgao.clear()
                campo_orgao.send_keys(orgao)
            
            # Clicar no botão de busca
            logger.info("Clicando no botão de busca...")
            botao_busca = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="defaultForm2"]/div[15]/input'))
            )
            botao_busca.click()
            
            # Aguardar resultados
            logger.info("Aguardando resultados da pesquisa...")
            time.sleep(3)
            
            try:
                # Verificar total de registros
                counter = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "resultCounter"))
                )
                total_text = counter.find_element(By.TAG_NAME, "b").text
                logger.info(f"Total de registros encontrados: {total_text}")
                
                if int(total_text) != 1:
                    logger.error(f"Número de registros ({total_text}) diferente de 1. Não é seguro prosseguir.")
                    return False
                
                # Procurar o link do pregão
                logger.info("Procurando link do pregão...")
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="searchTableSorter"]/tbody/tr[1]/td[7]/a'))
                )
                
                logger.info("Link encontrado, clicando...")
                driver.execute_script("arguments[0].click();", link)
                logger.info("Link clicado com sucesso")
                
                # Aguardar carregamento da página do pregão
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "mainContent"))
                )
                
                # Baixar edital
                if not AutomationRules.baixar_edital(driver):
                    logger.error("Erro ao baixar edital")
                    return False
                logger.info("Edital baixado com sucesso")
                
                return True
                    
            except Exception as e:
                logger.error(f"Erro ao processar resultados: {str(e)}")
                return False
            
        except Exception as e:
            logger.error(f"Erro ao pesquisar pregão: {str(e)}")
            return False

    @staticmethod
    def baixar_edital(driver):
        """Baixa o edital do pregão"""
        try:
            logger.info("Iniciando download do edital...")
            
            # Aguardar e clicar no botão de download usando XPath exato
            try:
                botao_download = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[1]/div[2]/div[2]/div[1]/div/div[2]/a"))
                )
                driver.execute_script("arguments[0].click();", botao_download)
                time.sleep(2)
            except Exception as e:
                logger.error(f"Erro ao clicar no botão de download: {str(e)}")
                return False

            # Resolver captcha e fazer download
            if not AutomationRules.resolver_captcha_download(driver):
                return False
                
            # Aguardar download e fechar popup
            time.sleep(2)
            try:
                driver.switch_to.default_content()
                time.sleep(1)
                
                # Fechar qualquer popup que possa estar aberto
                try:
                    popup = driver.find_element(By.CLASS_NAME, "pp_close")
                    if popup.is_displayed():
                        popup.click()
                        time.sleep(2)
                except:
                    pass
                
                # Tentar clicar no botão de registrar proposta usando XPath exato
                max_tentativas = 3
                for tentativa in range(max_tentativas):
                    try:
                        # Garantir que estamos no conteúdo principal
                        driver.switch_to.default_content()
                        time.sleep(2)
                        
                        # Tentar clicar no botão
                        botao_registrar = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[1]/div[2]/div[3]/a[1]"))
                        )
                        # Rolar até o elemento
                        driver.execute_script("arguments[0].scrollIntoView(true);", botao_registrar)
                        time.sleep(2)
                        # Tentar primeiro com click() normal
                        try:
                            botao_registrar.click()
                        except:
                            # Se falhar, tentar com JavaScript
                            driver.execute_script("arguments[0].click();", botao_registrar)
                        logger.info("Botão de registro clicado com sucesso")
                        time.sleep(5)
                        return True
                    except Exception as e:
                        logger.warning(f"Tentativa {tentativa + 1} falhou: {str(e)}")
                        if tentativa < max_tentativas - 1:
                            time.sleep(5)
                            # Tentar recarregar a página na segunda tentativa
                            if tentativa == 1:
                                driver.refresh()
                                time.sleep(5)
                        else:
                            logger.error("Todas as tentativas de clicar no botão falharam")
                            return False
                
            except Exception as e:
                logger.error(f"Erro ao processar após download: {str(e)}")
                return False
            
        except Exception as e:
            logger.error(f"Erro ao baixar edital: {str(e)}")
            return False

    @staticmethod
    def resolver_captcha_download(driver):
        """Resolve o captcha e faz o download"""
        try:
            # Mudar para o iframe do popup
            iframe_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#pp_full_res > iframe"))
            )
            driver.switch_to.frame(iframe_popup)
            logger.info("Mudou para iframe do popup")
            time.sleep(2)

            # Mudar para o iframe do reCAPTCHA
            iframe_captcha = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
            )
            driver.switch_to.frame(iframe_captcha)
            logger.info("Mudou para iframe do reCAPTCHA")
            time.sleep(2)

            # Clicar no checkbox do captcha usando XPath exato
            max_tentativas = 3
            for tentativa in range(max_tentativas):
                try:
                    checkbox = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']/div[1]"))
                    )
                    driver.execute_script("arguments[0].click();", checkbox)
                    logger.info("Checkbox do captcha clicado")
                    time.sleep(5)
                    break
                except Exception as e:
                    if tentativa == max_tentativas - 1:
                        logger.error(f"Falha ao clicar no checkbox do captcha: {str(e)}")
                        return False
                    time.sleep(2)

            # Verificar se o captcha foi resolvido
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".recaptcha-checkbox-checked"))
                )
                logger.info("Captcha resolvido com sucesso")
            except:
                logger.error("Timeout aguardando resolução do captcha")
                return False

            # Voltar ao frame do popup para clicar no botão de download
            driver.switch_to.parent_frame()
            logger.info("Voltou para o frame do popup")
            time.sleep(2)

            # Clicar no botão de download usando XPath exato
            try:
                botao_download = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='btGravar']"))
                )
                driver.execute_script("arguments[0].click();", botao_download)
                logger.info("Botão de download clicado")
                time.sleep(3)
            except Exception as e:
                logger.error(f"Erro ao clicar no botão de download: {str(e)}")
                return False

            # Voltar ao frame principal para fechar o popup
            driver.switch_to.default_content()
            logger.info("Voltou para o frame principal")
            time.sleep(2)

            # Fechar o popup usando XPath exato
            try:
                botao_fechar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div[2]/div[3]/a"))
                )
                driver.execute_script("arguments[0].click();", botao_fechar)
                logger.info("Popup fechado com sucesso")
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Erro ao fechar popup: {str(e)}")
                # Continuar mesmo se falhar ao fechar o popup

            return True

        except Exception as e:
            logger.error(f"Erro ao resolver captcha: {str(e)}")
            # Garantir que voltamos ao frame principal
            try:
                driver.switch_to.default_content()
            except:
                pass
            return False

    @staticmethod
    def preencher_declaracoes_info(driver, is_mei=False):
        """Preenche declarações e informações complementares"""
        try:
            logger.info("Iniciando preenchimento de declarações...")
            
            # Tentar abrir a guia de declarações
            if not AutomationRules.wait_and_click(
                driver, 
                (By.XPATH, '//a[contains(@title, "Declarações")]'),
                description="link de declarações"
            ):
                # Tentar método alternativo
                if not AutomationRules.wait_and_click(
                    driver, 
                    (By.XPATH, '//a[contains(., "1 - DECLARAÇÕES")]'),
                    description="link alternativo de declarações"
                ):
                    raise Exception("Não foi possível abrir a guia de declarações")
            
            time.sleep(2)  # Aguardar animação

            # Verificar visibilidade do formulário
            form = AutomationRules.wait_for_visibility(
                driver,
                (By.ID, "defaultForm"),
                description="formulário de declarações"
            )
            
            if not form:
                # Tentar clicar novamente no link
                if not AutomationRules.wait_and_click(
                    driver,
                    (By.XPATH, '//a[contains(., "1 - DECLARAÇÕES")]'),
                    description="link de declarações (segunda tentativa)"
                ):
                    raise Exception("Não foi possível tornar o formulário visível")
                time.sleep(2)

            # Marcar todas as checkboxes
            if not AutomationRules.check_all_boxes(driver):
                logger.warning("Houve problemas ao marcar algumas checkboxes")

            # Selecionar opção MEI
            if not AutomationRules.select_radio_option(
                driver,
                "ttCD_BOLEANO_D_EPP",
                "1" if is_mei else "2",
                description="opção MEI"
            ):
                raise Exception("Erro ao selecionar opção MEI")

            # Preencher validade da proposta
            if not AutomationRules.wait_and_fill(
                driver,
                (By.ID, "ttPRAZO_VALIDADE"),
                "120",
                description="campo de validade da proposta"
            ):
                raise Exception("Erro ao preencher validade da proposta")

            # Salvar declarações
            logger.info("Tentando salvar declarações...")
            
            # Tentar diferentes seletores para o botão salvar
            botao_encontrado = False
            for selector in [
                (By.CSS_SELECTOR, "input[value='Salvar Declarações']"),
                (By.CSS_SELECTOR, "input.buttonDefault.btnGravar"),
                (By.CSS_SELECTOR, "input[type='submit'][value*='Salvar']")
            ]:
                if AutomationRules.wait_and_click(driver, selector, timeout=5, description="botão salvar"):
                    botao_encontrado = True
                    break
            
            if not botao_encontrado:
                raise Exception("Não foi possível encontrar o botão salvar")

            # Aguardar processamento
            time.sleep(3)
            
            # Verificar se houve sucesso
            try:
                form_after = driver.find_element(By.CSS_SELECTOR, "form[action*='Declaracoes']")
                if form_after.is_displayed():
                    logger.error("Formulário ainda está visível após salvar")
                    return False
            except:
                logger.info("Formulário não está mais visível - sucesso!")
                return True

            return True

        except Exception as e:
            logger.error(f"Erro ao preencher declarações: {str(e)}")
            return False

    @staticmethod
    def preencher_criterios_desempate(driver):
        """
        Preenche os critérios de desempate após as declarações iniciais
        """
        try:
            logger.info("Iniciando preenchimento de critérios de desempate...")
            
            # Verificar se o formulário está visível
            form = AutomationRules.wait_for_visibility(
                driver,
                (By.CSS_SELECTOR, "form[action*='CriteriosDesempate']"),
                description="formulário de critérios"
            )
            
            if not form:
                # Tentar expandir a seção
                if not AutomationRules.wait_and_click(
                    driver,
                    (By.CSS_SELECTOR, "#GrupoComplementar > a"),
                    description="link para expandir critérios"
                ):
                    raise Exception("Não foi possível expandir a seção de critérios")
                time.sleep(2)

            # Marcar todos os radio buttons como "Sim"
            logger.info("Marcando todos os critérios como Sim...")
            
            # Primeiro tentar via JavaScript (mais rápido)
            driver.execute_script("""
                document.querySelectorAll('input[type="radio"][value="1"]').forEach(radio => {
                    if (!radio.checked) {
                        radio.checked = true;
                        radio.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                });
            """)
            time.sleep(1)

            # Verificar se todos foram marcados e corrigir os que faltaram
            for i in range(2, 8):  # radios de 2 a 7
                radio_id = f"checkIt{i}-1"
                radio = driver.find_element(By.ID, radio_id)
                if not radio.is_selected():
                    logger.info(f"Marcando radio {radio_id} via clique")
                    if not AutomationRules.wait_and_click(
                        driver,
                        (By.ID, radio_id),
                        timeout=5,
                        description=f"radio button {i}"
                    ):
                        logger.warning(f"Não foi possível marcar o radio {radio_id}")

            # Salvar critérios
            logger.info("Salvando critérios de desempate...")
            
            # Tentar diferentes seletores para o botão salvar
            botao_encontrado = False
            for selector in [
                (By.CSS_SELECTOR, "input[value='Salvar Informações']"),
                (By.CSS_SELECTOR, "input.buttonDefault.btnGravar"),
                (By.CSS_SELECTOR, "input[type='submit'][value*='Salvar']")
            ]:
                if AutomationRules.wait_and_click(driver, selector, timeout=5, description="botão salvar critérios"):
                    botao_encontrado = True
                    break
            
            if not botao_encontrado:
                raise Exception("Não foi possível encontrar o botão salvar")

            # Aguardar processamento
            time.sleep(3)
            
            # Verificar se houve sucesso
            try:
                form_after = driver.find_element(By.CSS_SELECTOR, "form[action*='CriteriosDesempate']")
                if form_after.is_displayed():
                    logger.error("Formulário ainda está visível após salvar")
                    return False
            except:
                logger.info("Critérios salvos com sucesso!")
                return True

            return True

        except Exception as e:
            logger.error(f"Erro ao preencher critérios de desempate: {str(e)}")
            return False

    @staticmethod
    def preencher_proposta_precos(driver):
        """Preenche a proposta de preços para todos os itens"""
        logger.info("Iniciando preenchimento da proposta de preços")
        
        itens_processados = set()  # Conjunto para rastrear itens já processados
        tentativas_maximas = 3  # Número máximo de tentativas por item

        while True:
            try:
                # Encontrar próximo item não cadastrado
                numero_item, linha_item = AutomationRules.get_proximo_item_nao_cadastrado(driver)
                
                if numero_item is None:
                    logger.info("Não há mais itens para cadastrar")
                    return True  # Retorna True para indicar sucesso
                    
                if numero_item in itens_processados:
                    if len(itens_processados) >= tentativas_maximas:
                        logger.warning(f"Item {numero_item} já processado {tentativas_maximas} vezes, pulando...")
                        continue
                        
                logger.info(f"Preenchendo item {numero_item}")
                itens_processados.add(numero_item)
                
                # Clicar no ícone de editar do item
                editar_btn = linha_item.find_element(By.CSS_SELECTOR, "a.actionIcons[title='Editar Item']")
                driver.execute_script("arguments[0].click();", editar_btn)
                
                # Aguardar o formulário aparecer e estar pronto
                try:
                    form = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "insideTableForm"))
                    )
                    # Aguardar mais um pouco para garantir que o form está pronto
                    time.sleep(2)
                except:
                    logger.error("Erro ao aguardar formulário do item")
                    continue
                
                # Preencher os campos do item
                try:
                    AutomationRules.preencher_campos_item(driver)
                except Exception as e:
                    logger.error(f"Erro ao preencher campos: {str(e)}")
                    continue
                
                # Clicar em Registrar Item
                try:
                    registrar_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.buttonDefault[value='Registrar Item']"))
                    )
                    driver.execute_script("arguments[0].click();", registrar_btn)
                    time.sleep(2)
                except:
                    logger.error("Erro ao clicar em Registrar Item")
                    continue
                
                # Aguardar e clicar no botão OK do popup
                try:
                    # Aguardar o popup aparecer
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "infoModalBlock"))
                    )
                    time.sleep(1)
                    
                    # Tentar clicar no botão OK
                    popup_ok = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.confirmLink.enterLink"))
                    )
                    
                    driver.execute_script("arguments[0].click();", popup_ok)
                    logger.info("Botão OK do popup clicado com sucesso")
                    time.sleep(2)
                    
                except Exception as e:
                    logger.warning(f"Erro ao clicar no botão OK do popup: {str(e)}")
                    continue
                
            except Exception as e:
                logger.error(f"Erro ao preencher item: {str(e)}")
                continue
                
        return True

    @staticmethod
    def item_ja_cadastrado(driver, item_row):
        """
        Verifica se um item já foi cadastrado verificando o ícone verde
        
        Args:
            driver: Instância do WebDriver
            item_row: Elemento tr da linha do item
            
        Returns:
            bool: True se já cadastrado, False caso contrário
        """
        try:
            # Verifica se a linha tem a classe propostaOK
            if 'propostaOK' in item_row.get_attribute('class'):
                return True
                
            # Verifica se tem o ícone verde
            icones = item_row.find_elements(By.CSS_SELECTOR, "img[src='/4/img/icoOk.png'][alt='Item Gravado']")
            return len(icones) > 0
        except:
            return False

    @staticmethod
    def get_proximo_item_nao_cadastrado(driver):
        """
        Encontra o próximo item que ainda não foi cadastrado
        
        Args:
            driver: Instância do WebDriver
            
        Returns:
            tuple: (número do item, elemento tr da linha) ou (None, None) se não houver mais itens
        """
        try:
            # Aguardar a tabela estar presente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchTableSorter"))
            )
            
            # Encontrar todas as linhas de itens (apenas as linhas principais, não os forms)
            linhas_itens = driver.find_elements(By.CSS_SELECTOR, "tr.oddLine, tr.evenLine")
            
            for linha in linhas_itens:
                try:
                    # Verificar se é uma linha de item válida
                    if not linha.is_displayed():
                        continue
                
                    # Verificar se tem o número do item
                    numero_span = linha.find_element(By.CSS_SELECTOR, "td.td50 span")
                    if not numero_span.is_displayed():
                        continue
                    
                    numero_item = numero_span.text.strip()
                    
                    # Verificar se o item já foi cadastrado
                    icones = linha.find_elements(By.CSS_SELECTOR, "td.td80 img[alt='Item Gravado']")
                    if not icones:  # Se não encontrar o ícone verde, o item não foi cadastrado
                        logger.info(f"Encontrado item não cadastrado: {numero_item}")
                        return numero_item, linha
                        
                except Exception as e:
                    logger.warning(f"Erro ao processar linha: {str(e)}")
                    continue
                    
            logger.info("Não foram encontrados mais itens para cadastrar")
            return None, None
            
        except Exception as e:
            logger.error(f"Erro ao buscar próximo item: {str(e)}")
            return None, None

    @staticmethod
    def registrar_proposta(driver, arquivo_pdf, is_mei=False):
        """Registra uma nova proposta"""
        try:
            # Preencher declarações e informações complementares
            if not AutomationRules.preencher_declaracoes_info(driver, is_mei):
                logger.error("Erro ao preencher declarações e informações complementares")
                return False
            
            # Preencher critérios de desempate
            if not AutomationRules.preencher_criterios_desempate(driver):
                logger.error("Erro ao preencher critérios de desempate")
                return False
            
            # Preencher proposta de preços
            if not AutomationRules.preencher_proposta_precos(driver):
                logger.error("Erro ao preencher proposta de preços")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao registrar proposta: {str(e)}")
            return False

    @staticmethod
    def buscar_pregao(self, driver):
        """Busca o pregão desejado"""
        try:
            logger.info("Procurando link do pregão...")
            
            # Verificar número total de registros
            try:
                total_registros_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//p[@class='resultCounter']/b"))
                )
                total_registros = int(total_registros_elem.text)
                logger.info(f"Total de registros encontrados: {total_registros}")
                
                if total_registros != 1:
                    logger.error(f"Número de registros ({total_registros}) diferente de 1. Não é seguro prosseguir.")
                    return False
            except Exception as e:
                logger.error(f"Erro ao verificar número de registros: {str(e)}")
                return False

            # Se chegou aqui, temos exatamente 1 registro
            try:
                link_pregao = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//td[@class='td375']/a"))
                )
                driver.execute_script("arguments[0].click();", link_pregao)
                time.sleep(2)
                logger.info("Link do pregão clicado com sucesso")
                return True
            except Exception as e:
                logger.error(f"Erro ao clicar no link do pregão: {str(e)}")
                return False

        except Exception as e:
            logger.error(f"Erro ao buscar pregão: {str(e)}")
            return False

    @staticmethod
    def registrar_todos_itens(driver):
        """Registra todos os itens disponíveis para registro"""
        try:
            logger.info("Iniciando registro de todos os itens...")
            itens_registrados = 0
            max_tentativas = 50  # Limite de segurança para evitar loop infinito
            
            while True:  # Loop infinito, vamos controlar com max_tentativas
                if itens_registrados >= max_tentativas:
                    logger.warning(f"Atingido limite máximo de {max_tentativas} tentativas")
                    break
                
                # Aguardar a tabela de itens carregar
                try:
                    tabela = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table.tableItens"))
                    )
                except Exception as e:
                    logger.error(f"Erro ao encontrar tabela de itens: {str(e)}")
                    break
                
                # Encontrar links de edição
                links_editar = driver.find_elements(By.CSS_SELECTOR, "a.openTableFormLink[title='Editar Item']")
                
                if not links_editar:
                    logger.info("Nenhum item encontrado para registro - processo concluído")
                    break
                
                logger.info(f"Encontrados {len(links_editar)} itens para registrar")
                
                # Registrar o primeiro item da lista
                try:
                    link = links_editar[0]  # Sempre pegar o primeiro, já que após registrar um item a página atualiza
                    
                    # Pegar a descrição antes de clicar no link
                    descricao_item = AutomationRules.pegar_descricao_item(driver)
                    
                    # Verificar se o link está visível
                    if not WebDriverWait(driver, 10).until(
                        EC.visibility_of(link)
                    ):
                        logger.error("Link do item não está visível")
                        continue
                    
                    # Clicar no link e preencher o item
                    driver.execute_script("arguments[0].click();", link)
                    time.sleep(2)
                    
                    if not AutomationRules.preencher_proposta_precos(driver, descricao_item):
                        logger.error("Erro ao preencher item")
                        # Tentar fechar o formulário se houver erro
                        try:
                            fechar_btn = driver.find_element(By.CSS_SELECTOR, "a.closeTableForm")
                            driver.execute_script("arguments[0].click();", fechar_btn)
                        except:
                            pass
                        continue
                    
                    # Aguardar um pouco para o diálogo aparecer
                    time.sleep(2)
                    
                    # Fechar o diálogo de confirmação
                    if not AutomationRules.fechar_dialogo_apos_registro(driver):
                        logger.error("Erro ao fechar diálogo de confirmação")
                        continue
                    
                    itens_registrados += 1
                    logger.info(f"Item registrado com sucesso. Total de itens registrados: {itens_registrados}")
                    
                    # Aguardar a página atualizar antes de continuar
                    time.sleep(5)  # Aumentado para 5 segundos
                    
                    # Tentar atualizar a página se necessário
                    try:
                        driver.refresh()
                        time.sleep(3)  # Esperar a página recarregar
                    except:
                        pass
                    
                except Exception as e:
                    logger.error(f"Erro ao processar item: {str(e)}")
                    continue
            
            logger.info(f"Registro de itens concluído. Total de itens registrados: {itens_registrados}")
            return True if itens_registrados > 0 else False
            
        except Exception as e:
            logger.error(f"Erro ao registrar todos os itens: {str(e)}")
            return False

    @staticmethod
    def fechar_dialogo_apos_registro(driver):
        """Fecha o diálogo que aparece após registrar um item"""
        try:
            logger.info("Tentando fechar diálogo após registro...")
            
            # Esperar o diálogo aparecer
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "infoModalBlock"))
            )
            
            # Lista de seletores para o botão OK
            seletores = [
                "a.confirmLink.enterLink",
                "a[href='javascript: void(0)'].confirmLink",
                "//a[contains(@class, 'confirmLink') and contains(@class, 'enterLink')]"
            ]
            
            # Tentar cada seletor
            for seletor in seletores:
                try:
                    if seletor.startswith("//"):
                        # Se for XPath
                        botao = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, seletor))
                        )
                    else:
                        # Se for CSS
                        botao = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, seletor))
                        )
                    
                    # Tentar diferentes métodos de clique
                    try:
                        botao.click()
                    except:
                        try:
                            driver.execute_script("arguments[0].click();", botao)
                        except:
                            # Simular tecla Enter
                            botao.send_keys(Keys.RETURN)
                    
                    # Verificar se o diálogo fechou
                    try:
                        WebDriverWait(driver, 5).until_not(
                            EC.presence_of_element_located((By.CLASS_NAME, "infoModalBlock"))
                        )
                        logger.info("Diálogo fechado com sucesso")
                        return True
                    except:
                        continue
                except:
                    continue
            
            logger.error("Não foi possível fechar o diálogo")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao fechar diálogo: {str(e)}")
            return False

    @staticmethod
    def pegar_descricao_item(driver):
        """Pega a descrição completa do item"""
        try:
            # Tentar pegar do link moreTextLink
            link = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.moreTextLink"))
            )
            descricao = link.get_attribute("title")
            if descricao:
                logger.info(f"Descrição encontrada no link: {descricao}")
                return descricao
        except Exception as e:
            logger.warning(f"Erro ao pegar descrição do link: {str(e)}")
        
        # Se não conseguir pelo link, tentar outros métodos
        try:
            # Tentar pegar do texto da célula
            cell = driver.find_element(By.CSS_SELECTOR, "td.itemDescricao")
            descricao = cell.text
            if descricao:
                logger.info(f"Descrição encontrada na célula: {descricao}")
                return descricao
        except:
            pass
        
        # Se nada funcionar, retornar None
        logger.warning("Não foi possível encontrar a descrição do item")
        return None

    @staticmethod
    def preencher_campos_item(driver):
        """
        Preenche os campos do formulário de item
        
        Args:
            driver: Instância do WebDriver
        """
        try:
            # Aguardar o formulário ficar visível e interativo com retry
            max_attempts = 3
            form = None
            
            for attempt in range(max_attempts):
                try:
                    # Aguardar formulário ativo
                    form = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "tr.insideTableFormactive"))
                    )
                    if form and form.is_displayed():
                        break
                except:
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue
                    else:
                        raise Exception("Formulário não encontrado após várias tentativas")

            # Aguardar mais um pouco para garantir que o form está pronto
            time.sleep(2)

            # Lista de campos a serem preenchidos com seus IDs corretos
            campos = {
                "ttVALOR_UNITARIO": "2,00",  # Valor unitário
                "ttVALOR_TOTAL": "2,00",     # Valor total
                "ttMARCA": "modelo proprio",  # Modelo
                "ttFABRICANTE": "marca proprio",  # Marca/Fabricante
                "ttDETALHE": "Conforme edital"  # Descrição detalhada
            }

            # Preencher cada campo com retry
            for campo_id, valor in campos.items():
                max_field_attempts = 3
                for attempt in range(max_field_attempts):
                    try:
                        # Tentar encontrar o campo
                        campo = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, campo_id))
                        )
                        
                        # Scroll até o elemento
                        driver.execute_script("arguments[0].scrollIntoView(true);", campo)
                        time.sleep(0.5)
                        
                        # Limpar usando JavaScript
                        driver.execute_script("arguments[0].value = '';", campo)
                        time.sleep(0.2)
                        
                        # Preencher usando JavaScript
                        driver.execute_script(f"arguments[0].value = '{valor}';", campo)
                        time.sleep(0.2)
                        
                        # Disparar eventos para garantir que o valor seja registrado
                        driver.execute_script("""
                            var campo = arguments[0];
                            campo.dispatchEvent(new Event('change', { bubbles: true }));
                            campo.dispatchEvent(new Event('blur', { bubbles: true }));
                            campo.dispatchEvent(new Event('input', { bubbles: true }));
                        """, campo)
                        
                        logger.info(f"Campo {campo_id} preenchido com sucesso: {valor}")
                        break
                        
                    except Exception as e:
                        if attempt == max_field_attempts - 1:
                            raise Exception(f"Erro ao preencher campo {campo_id}: {str(e)}")
                        time.sleep(1)
                        continue

            # Aguardar um pouco antes de clicar no botão
            time.sleep(1)

            # Clicar no botão de registrar com retry
            max_button_attempts = 3
            for attempt in range(max_button_attempts):
                try:
                    # Primeiro tentar encontrar o botão
                    botao = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='btEnviar'][value='Registrar Item']"))
                    )
                    
                    # Scroll até o botão
                    driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                    time.sleep(0.5)
                    
                    # Tentar clicar normalmente primeiro
                    try:
                        botao.click()
                    except:
                        # Se falhar, usar JavaScript
                        driver.execute_script("arguments[0].click();", botao)
                    
                    logger.info("Botão registrar clicado com sucesso")
                    
                    # Aguardar feedback de sucesso (ícone verde ou mensagem)
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Item Gravado']"))
                        )
                        logger.info("Item registrado com sucesso")
                    except:
                        logger.warning("Não foi possível confirmar o registro do item")
                    
                    break
                    
                except Exception as e:
                    if attempt == max_button_attempts - 1:
                        raise Exception(f"Erro ao clicar no botão registrar: {str(e)}")
                    time.sleep(1)
                    continue

            # Aguardar processamento do registro
            time.sleep(3)
            
            return True

        except Exception as e:
            logger.error(f"Erro ao preencher campos do item: {str(e)}")
            return False

    @staticmethod
    def preencher_proposta_precos(driver):
        """Preenche a proposta de preços para todos os itens"""
        logger.info("Iniciando preenchimento da proposta de preços")
        
        itens_processados = set()  # Conjunto para rastrear itens já processados
        tentativas_maximas = 3  # Número máximo de tentativas por item

        while True:
            try:
                # Encontrar próximo item não cadastrado
                numero_item, linha_item = AutomationRules.get_proximo_item_nao_cadastrado(driver)
                
                if numero_item is None:
                    logger.info("Não há mais itens para cadastrar")
                    return True  # Retorna True para indicar sucesso
                    
                if numero_item in itens_processados:
                    if len(itens_processados) >= tentativas_maximas:
                        logger.warning(f"Item {numero_item} já processado {tentativas_maximas} vezes, pulando...")
                        continue
                        
                logger.info(f"Preenchendo item {numero_item}")
                itens_processados.add(numero_item)
                
                # Clicar no ícone de editar do item
                editar_btn = linha_item.find_element(By.CSS_SELECTOR, "a.actionIcons[title='Editar Item']")
                driver.execute_script("arguments[0].click();", editar_btn)
                
                # Aguardar o formulário aparecer e estar pronto
                try:
                    form = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "insideTableForm"))
                    )
                    # Aguardar mais um pouco para garantir que o form está pronto
                    time.sleep(2)
                except:
                    logger.error("Erro ao aguardar formulário do item")
                    continue
                
                # Preencher os campos do item
                try:
                    AutomationRules.preencher_campos_item(driver)
                except Exception as e:
                    logger.error(f"Erro ao preencher campos: {str(e)}")
                    continue
                
                # Clicar em Registrar Item
                try:
                    registrar_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.buttonDefault[value='Registrar Item']"))
                    )
                    driver.execute_script("arguments[0].click();", registrar_btn)
                    time.sleep(2)
                except:
                    logger.error("Erro ao clicar em Registrar Item")
                    continue
                
                # Aguardar e clicar no botão OK do popup
                try:
                    # Aguardar o popup aparecer
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "infoModalBlock"))
                    )
                    time.sleep(1)
                    
                    # Tentar clicar no botão OK
                    popup_ok = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.confirmLink.enterLink"))
                    )
                    
                    driver.execute_script("arguments[0].click();", popup_ok)
                    logger.info("Botão OK do popup clicado com sucesso")
                    time.sleep(2)
                    
                except Exception as e:
                    logger.warning(f"Erro ao clicar no botão OK do popup: {str(e)}")
                    continue
                
            except Exception as e:
                logger.error(f"Erro ao preencher item: {str(e)}")
                continue
                
        return True

    @staticmethod
    def processar_campos_proposta(self, driver):
        """
        Processa campos dinâmicos da proposta, aguardando o carregamento de novos campos
        conforme o preenchimento avança.
        """
        logger.info("Iniciando processamento dos campos da proposta")
        try:
            while True:
                # Aguarda carregamento inicial dos grupos
                WebDriverWait(driver, self.WAIT_TIMEOUT).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id^="Grupo"]'))
                )
                
                # Encontra todos os grupos visíveis
                grupos = driver.find_elements(By.CSS_SELECTOR, 'div[id^="Grupo"]:not([style*="display: none"])')
                
                if not grupos:
                    logger.info("Nenhum grupo visível encontrado. Verificando se finalizou...")
                    # Verifica se chegou ao fim do processo
                    if driver.find_elements(By.CSS_SELECTOR, '.mensagem-sucesso'):
                        logger.info("Processo finalizado com sucesso!")
                        break
                    time.sleep(1)
                    continue

                for grupo in grupos:
                    grupo_id = grupo.get_attribute("id")
                    logger.info(f"Processando grupo: {grupo_id}")

                    # Aguarda elementos interativos do grupo atual
                    self._aguardar_elementos_grupo(driver, grupo)

                    # Processa campos do grupo atual
                    if self._processar_grupo_especifico(driver, grupo, grupo_id):
                        # Se retornou True, significa que finalizou o processamento
                        return True

                    # Aguarda processamento do grupo atual
                    time.sleep(1)

        except Exception as e:
            logger.error(f"Erro ao processar campos da proposta: {str(e)}")
            raise

    def _aguardar_elementos_grupo(self, driver, grupo):
        """Aguarda elementos interativos do grupo ficarem visíveis e interativos"""
        try:
            WebDriverWait(driver, self.WAIT_TIMEOUT).until(
                lambda d: grupo.find_elements(By.CSS_SELECTOR, 
                    'input:not([type="hidden"]), select, textarea, button, a.modal-link-reload, .linkButtonDefault6'
                )
            )
        except:
            logger.warning(f"Timeout aguardando elementos do grupo {grupo.get_attribute('id')}")

    def _processar_grupo_especifico(self, driver, grupo, grupo_id):
        """Processa um grupo específico baseado em seu ID"""
        try:
            if "Declaracoes" in grupo_id:
                self._processar_declaracoes(grupo)
            elif "Complementar" in grupo_id:
                self._processar_complementar(grupo)
            elif "ComprovanteGarantiaProposta" in grupo_id:
                self._processar_comprovante(grupo)
            elif "Documentos" in grupo_id:
                self._processar_documentos(grupo)
            elif "Proposta" in grupo_id:
                return self._processar_proposta_final(grupo)
            else:
                self._processar_grupo_generico(grupo)
            return False
        except Exception as e:
            logger.error(f"Erro ao processar grupo {grupo_id}: {str(e)}")
            return False

    def _processar_declaracoes(self, grupo):
        """Processa o grupo de declarações"""
        checkboxes = grupo.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        
        submit = grupo.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        if submit:
            submit.click()
            logger.info("Declarações enviadas")

    def _processar_complementar(self, grupo):
        """Processa informações complementares"""
        campos_texto = grupo.find_elements(By.CSS_SELECTOR, 'input[type="text"], textarea')
        for campo in campos_texto:
            if not campo.get_attribute("value"):
                campo.send_keys("Conforme edital")
        
        submit = grupo.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        if submit:
            submit.click()
            logger.info("Informações complementares enviadas")

    def _processar_comprovante(self, grupo):
        """Processa o comprovante de garantia"""
        link = grupo.find_element(By.CSS_SELECTOR, 'a.modal-link-reload')
        if link:
            link.click()
            logger.info("Modal de comprovante aberto")

    def _processar_documentos(self, grupo):
        """Processa o grupo de documentos"""
        botao = grupo.find_element(By.CSS_SELECTOR, '.linkButtonDefault6')
        if botao:
            botao.click()
            logger.info("Documentos processados")

    def _processar_proposta_final(self, grupo):
        """Processa o grupo final da proposta"""
        logger.info("Proposta de Preços finalizada")
        return True

    def _processar_grupo_generico(self, grupo):
        """Processa grupos não identificados"""
        # Processa campos de texto
        for campo in grupo.find_elements(By.CSS_SELECTOR, 'input[type="text"], textarea'):
            if not campo.get_attribute("value"):
                campo.send_keys("Conforme edital")
        
        # Processa selects
        for select_elem in grupo.find_elements(By.TAG_NAME, 'select'):
            select = Select(select_elem)
            if not select.first_selected_option.text:
                select.select_by_index(1)

        # Processa checkboxes
        for checkbox in grupo.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]'):
            if not checkbox.is_selected():
                checkbox.click()

        logger.info(f"Grupo genérico processado: {grupo.get_attribute('id')}")

    @staticmethod
    def iniciar_automacao(driver):
        """Inicia o processo de automação"""
        try:
            logger.info("Iniciando processo de automação...")
            
            # Salvar critérios
            if not AutomationRules.salvar_criterios(driver):
                logger.error("Erro ao salvar critérios")
                return False
            
            # Registrar todos os itens
            if not AutomationRules.registrar_todos_itens(driver):
                logger.error("Erro ao registrar todos os itens")
                return False
            
            logger.info("Automação concluída com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar automação: {str(e)}")
            return False
