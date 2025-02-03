from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.utils.constantes import PORTAL_SELECT_VALUES, PORTAL_MAPPING
import time
import os
import json

class NavegadorProcessor:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fechar_popup_tour(self):
        """Fecha o popup de tour se estiver presente"""
        try:
            # Tenta encontrar o botão "Já sei usar"
            fechar_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-role='end']"))
            )
            fechar_btn.click()
            print("Popup de tour fechado!")
            return True
        except:
            print("Popup de tour não encontrado")
            return False

    def preencher_campo_orgao(self, dados, portal_key):
        """Preenche o campo órgão de acordo com o portal"""
        try:
            # Se for ComprasNet, retorna pois terá outra lógica
            if portal_key == 'comprasnet':
                print("Portal ComprasNet: campo órgão será preenchido em outra etapa")
                return True
                
            # Pegar o valor do campo ao_estimado_orgao
            orgao = dados.get('ao_estimado_orgao', '')
            if not orgao:
                print("Campo AO ESTIMADO ÓRGÃO não encontrado no JSON")
                return False
                
            # Para BNC e BLL, remover o que está entre colchetes
            if portal_key in ['bnc', 'bll']:
                # Encontrar a posição do colchete
                colchete_pos = orgao.find('[')
                if colchete_pos > -1:
                    # Pegar só o texto antes do colchete e remover espaços extras
                    orgao = orgao[:colchete_pos].strip()
                    print(f"Órgão após remover colchetes: {orgao}")
                    
            # Preencher o campo
            campo_orgao = self.wait.until(EC.presence_of_element_located((By.ID, "sel-organ")))
            campo_orgao.clear()
            campo_orgao.send_keys(orgao)
            print(f"Campo órgão preenchido com: {orgao}")
            
            return True
            
        except Exception as e:
            print(f"Erro ao preencher campo órgão: {str(e)}")
            return False

    def selecionar_portal(self, dados):
        """Seleciona o portal no dropdown"""
        try:
            # Mapear o nome do portal para a chave do select
            portal_key = PORTAL_MAPPING.get(dados['portal'], '').lower()
            if not portal_key:
                print(f"Portal não mapeado: {dados['portal']}")
                return False
                
            # Pegar o valor do select para este portal
            portal_value = PORTAL_SELECT_VALUES.get(portal_key)
            if not portal_value:
                print(f"Valor do portal não encontrado: {portal_key}")
                return False
                
            # Encontrar o select e selecionar o portal
            select_element = self.wait.until(
                EC.presence_of_element_located((By.ID, "sel-portal"))
            )
            select = Select(select_element)
            select.select_by_value(portal_value)
            print(f"Portal selecionado: {dados['portal']} (valor: {portal_value})")
            
            # Aguardar um pouco para o portal carregar
            time.sleep(2)
            
            # Selecionar a empresa
            empresa_select = self.wait.until(EC.presence_of_element_located((By.ID, "branch")))
            Select(empresa_select).select_by_value("1")
            print("Empresa selecionada!")
            
            # Aguardar um pouco para os campos carregarem
            time.sleep(2)
            
            # Preencher número da licitação
            print("Tentando preencher campo Licitação...")
            try:
                # Usar o ID correto do campo
                bidding_field = self.wait.until(EC.presence_of_element_located((By.ID, "sel-bidding")))
                bidding_field.clear()
                
                # Pegar o número do pregão do JSON usando o mesmo campo que é verificado
                numero_pregao = dados.get('pregao', '')
                if not numero_pregao:
                    print("Número do Pregão não encontrado no JSON")
                    return False
                    
                # Preencher o campo
                bidding_field.send_keys(numero_pregao)
                print(f"Campo Licitação preenchido com: {numero_pregao}")
                
            except Exception as e:
                print(f"Erro ao preencher campo de licitação: {str(e)}")
                return False
                
            # Preencher campo órgão
            if not self.preencher_campo_orgao(dados, portal_key):
                return False
            
            return True
            
        except Exception as e:
            print(f"Erro ao selecionar portal/empresa: {str(e)}")
            return False

    def preencher_formulario(self, dados):
        """Preenche o formulário com os dados fornecidos"""
        try:
            # Espera o formulário carregar
            form = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.proposal-form")))
            
            # Aguarda um pouco para os campos específicos do portal carregarem
            time.sleep(2)
            
            # Continua com o preenchimento dos outros campos...
            # Mapeia os campos específicos de cada portal
            portal_fields = {
                'comprasnet': {
                    'bidding': 'uasg',
                    'number': 'pregao'
                },
                'pncp': {
                    'bidding': 'id_pncp',
                    'number': 'numero_pncp'
                },
                'bnc': {
                    'bidding': 'id_bnc',
                    'number': 'numero_bnc'
                }
            }
            
            # Aguarda os campos específicos do portal carregarem
            if portal_fields.get(dados['portal'].lower()):
                self.fechar_popup_tour()
                
                if dados['portal'].lower() == 'comprasnet':
                    try:
                        # Campo UASG
                        uasg_field = self.wait.until(EC.presence_of_element_located((By.ID, portal_fields[dados['portal'].lower()]['bidding'])))
                        uasg_field.send_keys(dados['uasg'])
                        
                        # Campo Pregão
                        pregao_field = self.wait.until(EC.presence_of_element_located((By.ID, portal_fields[dados['portal'].lower()]['number'])))
                        pregao_field.send_keys(dados['pregao'])
                        
                    except Exception as e:
                        print(f"Erro ao preencher campos do ComprasNet: {str(e)}")
                        return False
                        
                else:
                    # Preenchimento padrão para outros portais
                    try:
                        # Campo ID
                        id_field = self.wait.until(EC.presence_of_element_located((By.ID, portal_fields[dados['portal'].lower()]['bidding'])))
                        id_field.send_keys(dados['id_licitacao'])
                        
                        # Campo Número
                        numero_field = self.wait.until(EC.presence_of_element_located((By.ID, portal_fields[dados['portal'].lower()]['number'])))
                        numero_field.send_keys(dados['pregao'])
                        
                    except Exception as e:
                        print(f"Erro ao preencher campos do portal {dados['portal']}: {str(e)}")
                        return False
                
                # Clica no botão Buscar
                try:
                    buscar_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-button")))
                    buscar_button.click()
                    print("Botão Buscar clicado!")
                    
                    # Aguarda os resultados
                    time.sleep(2)
                    
                    # Clica no botão Exportar planilha
                    try:
                        print("Procurando botão Exportar planilha...")
                        exportar = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Exportar planilha"]')))
                        self.driver.execute_script("arguments[0].click();", exportar)
                        print("Botão Exportar planilha clicado!")
                        return True
                        
                    except Exception as e:
                        print(f"Erro ao clicar no botão Exportar planilha: {str(e)}")
                        return False
                        
                except Exception as e:
                    print(f"Erro ao clicar no botão Buscar: {str(e)}")
                    return False
                    
            else:
                print(f"Portal {dados['portal']} não configurado")
                return False
                
        except Exception as e:
            print(f"Erro ao preencher formulário: {str(e)}")
            return False

    def iniciar_processo(self, dados):
        """Inicia o processo de automação"""
        url = "https://minha.effecti.com.br/#/proposta-minhas"
        self.driver.get(url)
        
        try:
            # Login mais rápido e direto
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "input-login")))
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "input-password")))
            
            # Preenche email e senha de uma vez
            email_field.send_keys("fernanda@alcantaramendes.com.br")
            password_field.send_keys("Alcantara@2025")
            
            # Clica no botão Entrar imediatamente
            entrar_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button-submit a.login-btn.l-button")))
            entrar_button.click()
            print("Login realizado com sucesso!")
            
            # Reduz o tempo de espera e já procura o botão Cadastrar Proposta
            print("Aguardando página carregar...")
            time.sleep(3)  # Aguarda a página carregar completamente
            
            # Espera o overlay desaparecer
            try:
                overlay = self.wait.until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.overlay.fullscreen"))
                )
            except:
                print("Aviso: Overlay não encontrado ou já invisível")
            
            print("Procurando botão Cadastrar Proposta...")
            try:
                # Primeira tentativa: esperar o botão estar clicável
                cadastrar_proposta_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-new-proposal"))
                )
                cadastrar_proposta_button.click()
                print("Botão Cadastrar Proposta clicado!")
                
                # Aguarda um pouco para o popup aparecer
                time.sleep(1)
                
                # Tenta fechar o popup de tour
                self.fechar_popup_tour()
                
                # Seleciona o portal
                if not self.selecionar_portal(dados):
                    print("Erro ao selecionar portal")
                    return False
                
                return True
                
            except:
                try:
                    # Segunda tentativa: usar JavaScript para remover overlay e clicar
                    self.driver.execute_script("""
                        // Remove qualquer overlay
                        var overlays = document.querySelectorAll('div.overlay');
                        overlays.forEach(function(overlay) {
                            overlay.remove();
                        });
                        
                        // Encontra e clica no botão
                        var botao = document.querySelector('button.btn-new-proposal');
                        if(botao) {
                            botao.click();
                        }
                    """)
                    print("Botão Cadastrar Proposta clicado!")
                    
                    # Aguarda um pouco para o popup aparecer
                    time.sleep(1)
                    
                    # Tenta fechar o popup de tour
                    self.fechar_popup_tour()
                    
                    # Seleciona o portal
                    if not self.selecionar_portal(dados):
                        print("Erro ao selecionar portal")
                        return False
                    
                    return True
                    
                except Exception as e:
                    print(f"Erro ao clicar no botão Cadastrar Proposta: {str(e)}")
                    return False

        except Exception as e:
            print(f"Erro durante o processo: {str(e)}")
            return False

    def processar_card(self, card):
        """Processa um card individual"""
        try:
            print(f"\nProcessando card: Pregão {card.get('pregao', 'N/A')}")
            
            # Iniciar processo passando o portal
            if not self.iniciar_processo(card):
                print("Falha ao iniciar processo")
                return False
            
            # Preencher formulário
            if not self.preencher_formulario(card):
                print("Falha ao preencher formulário")
                return False
                
            print("Card processado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao processar card: {str(e)}")
            return False

    def main(self):
        with open('dados.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        
        for card in dados:
            if not self.processar_card(card):
                print("Falha ao processar card")
                break

if __name__ == "__main__":
    driver = webdriver.Chrome()
    processor = NavegadorProcessor(driver)
    processor.main()