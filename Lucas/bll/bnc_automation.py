from logging import root
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pywinauto import Application
from pywinauto.keyboard import send_keys
from openpyxl import Workbook
import time
import win32com.client
import json
from datetime import datetime
import os
import glob
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def wait_for_login(driver, number="999", state="DF", city="", is_me=None):
    try:
        print("\nIniciando automação...")
        
        # Configura o diretório de download para a pasta do projeto
        project_dir = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": project_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Atualiza as opções do driver
        driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow',
            'downloadPath': project_dir
        })
        
        # Navega para a página desejada mantendo a sessão
        driver.get("https://bllcompras.com/Participant/ProcessSearch?param1=0")
        
        # Espera o botão estar visível e clicável
        wait = WebDriverWait(driver, 10)
        botao = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/table/tbody/tr[1]/td/table/tbody/tr/th[7]/a')))
        botao.click()
        
        # Preenche os campos do formulário
        fill_form(driver, number, state, city)
        
        # Localiza o número na tabela e retorna a linha
        row_info = find_number_in_table(driver, number)
        print("\nResultado da busca:")
        print(row_info)
        
        # Após entrar no pregão, seleciona a opção ME/EPP
        if row_info == "✓ Busca concluída!" and is_me is not None:
            table_info = select_me_epp_option(driver, is_me)
            if table_info:
                headers, rows = table_info
                print("\nDados da tabela:")
                for row in rows:
                    print(row)
                # Tenta clicar no botão Importar
                if click_import_button(driver):
                    print("✓ Botão 'Importar' clicado com sucesso!")
                    # Baixa o arquivo Excel
                    excel_file = download_excel_model(driver)
                    if excel_file:
                        print("✓ Excel baixado com sucesso")
                        # Processa o Excel
                        modified_excel = process_excel(excel_file)
                        if modified_excel:
                            print("✓ Excel processado com sucesso")
                            # Faz o upload do arquivo modificado
                            if upload_excel(driver, modified_excel):
                                print("✓ Upload do Excel concluído com sucesso")
                                # Clica no botão Enviar
                                if click_send_button(driver):
                                    print("✓ Proposta enviada com sucesso")
                                    if click_documents_button(driver):
                                        print("✓ Botão Documentos clicado com sucesso")
                                        # Adiciona a chamada para processar_documentos
                                        caminho_arquivo = os.path.join(project_dir, "vazio.pdf")
                                        processar_documentos(driver, caminho_arquivo)
                                        if salvar_proposta(driver):
                                            print("✓ Proposta salva com sucesso")
                                        else:
                                            print("⚠ Erro ao salvar a proposta")
                                    else:
                                        print("⚠ Erro ao clicar no botão Documentos")
                                else:
                                    print("⚠ Erro ao enviar a proposta")
                            else:
                                print("⚠ Erro ao fazer upload do Excel")
                        else:
                            print("⚠ Erro ao processar Excel")
                    else:
                        print("⚠ Erro ao baixar Excel")
                else:
                    print("⚠ Não foi possível clicar no botão 'Importar'")
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")
        raise e

def fill_form(driver, number, state, city):
    try:
        print(f"\nPreenchendo formulário - Número: {number}, Estado: {state}, Cidade: {city}")
        
        # Espera o campo número ficar visível e preenche com o número fornecido
        number_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Number"]'))
        )
        number_field.clear()
        number_field.send_keys(number)
        
        # Espera o campo estado ficar visível e seleciona o estado fornecido
        state_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fkState"]'))
        )
        select = Select(state_select)
        select.select_by_visible_text(state)

        # Preenche o campo cidade
        city_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="City"]'))
        )
        city_field.clear()
        city_field.send_keys(city)
        
        print("Campos preenchidos, iniciando busca...")
        
        # Aguarda um momento para garantir que todos os campos foram preenchidos
        time.sleep(1)
        
        # Procura e clica no botão de pesquisa
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnProcessSearch"]'))
        )
        search_button.click()
        
        print("Aguardando resultados da busca...")
        
        # Aguarda um momento para os resultados carregarem
        time.sleep(5)
              
        print("Busca realizada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao preencher o formulário: {e}")
        raise e

def select_me_epp_option(driver, is_me):
    try:
        print("\nSelecionando opção ME/EPP...")
        # Espera a página carregar completamente
        time.sleep(2)
        
        # Tenta diferentes seletores para encontrar o radio button
        selectors = [
            (By.NAME, "DeclaracaoME"),
            (By.ID, "optionsRadios1" if is_me else "optionsRadios2"),
            (By.XPATH, f"//input[@type='radio'][@value='{str(is_me).lower()}']"),
            (By.CSS_SELECTOR, f"input[type='radio'][value='{str(is_me).lower()}']")
        ]
        
        radio = None
        wait = WebDriverWait(driver, 3)
        
        # Tenta cada seletor até encontrar o elemento
        for by, selector in selectors:
            try:
                print(f"Tentando localizar elemento com {by}: {selector}")
                radio = wait.until(
                    EC.presence_of_element_located((by, selector))
                )
                if radio:
                    print(f"✓ Elemento encontrado usando {by}: {selector}")
                    break
            except Exception as e:
                print(f"Não foi possível encontrar com {by}: {selector}")
                continue
        
        if not radio:
            raise Exception("Não foi possível encontrar o radio button ME/EPP")
        
        # Tenta diferentes métodos para clicar no elemento
        click_methods = [
            lambda: radio.click(),
            lambda: driver.execute_script("arguments[0].click();", radio),
            lambda: ActionChains(driver).move_to_element(radio).click().perform(),
            lambda: driver.execute_script("arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change'));", radio)
        ]
        
        for i, click_method in enumerate(click_methods, 1):
            try:
                print(f"Tentativa {i} de clicar no elemento...")
                click_method()
                print("✓ Clique realizado com sucesso!")
                break
            except Exception as e:
                print(f"Tentativa {i} falhou: {str(e)}")
                if i == len(click_methods):
                    raise Exception("Todas as tentativas de clique falharam")
                continue
        
        # Aguarda um momento para a página processar o clique
        time.sleep(2)
        
        # Verifica se a seleção foi bem sucedida
        try:
            if radio.is_selected():
                print("✓ Opção ME/EPP selecionada com sucesso!")
            else:
                print("⚠ O elemento foi clicado mas não está selecionado")
        except:
            print("⚠ Não foi possível verificar o estado da seleção")
        
        # Captura os dados da tabela após a seleção
        return get_table_data(driver, process_number=driver.current_url.split('/')[-1])
            
    except Exception as e:
        print(f"Erro ao selecionar opção ME/EPP: {str(e)}")
        # Tenta capturar os dados mesmo se houver erro na seleção
        try:
            return get_table_data(driver, process_number=driver.current_url.split('/')[-1])
        except:
            return None

def get_table_data(driver, process_number=""):
    try:
        print("\nCapturando dados das tabelas...")
        # Espera a primeira tabela carregar
        first_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        
        # Captura os dados da segunda tabela (tabela de itens)
        items_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tableItems"))
        )
        
        # Captura os cabeçalhos da tabela de itens
        headers = []
        header_cells = items_table.find_elements(By.TAG_NAME, "th")
        for cell in header_cells:
            headers.append(cell.text.strip())
        
        # Captura as linhas de dados da tabela de itens
        rows_data = []
        rows = items_table.find_elements(By.TAG_NAME, "tr")[1:]  # Pula o cabeçalho
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text.strip() for cell in cells]
            if any(row_data):  # Só adiciona se tiver algum dado
                rows_data.append(row_data)
        
        # Cria um dicionário com os dados
        table_data = {
            "processo": process_number,
            "data_captura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "headers": headers,
            "items": [dict(zip(headers, row)) for row in rows_data]
        }
        
        # Salva os dados em um arquivo JSON
        filename = f"itens_processo_{process_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(table_data, f, ensure_ascii=False, indent=4)
        
        print(f"\n✓ Dados dos itens salvos em {filename}")
        return headers, rows_data
    except Exception as e:
        print(f"Erro ao capturar dados da tabela: {e}")
        return [], []

def click_href_link(driver, element):
    """
    Clicks on any href link safely, handling both direct clicks and JavaScript-based redirects
    """
    try:
        href = element.get_attribute('href')
        if href:
            # Try direct click first
            try:
                element.click()
            except:
                # If direct click fails, try JavaScript
                driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print(f"Erro ao clicar no link: {e}")
        return False

def click_import_button(driver):
    try:
        print("\nProcurando botão 'Importar'...")
        # Espera o botão estar presente e clicável
        wait = WebDriverWait(driver, 10)
        
        # Tenta diferentes métodos para encontrar o botão
        selectors = [
            (By.CSS_SELECTOR, "button.btn.btn-primary.btn-sm[title='Importar Proposta']"),
            (By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@title, 'Importar Proposta')]"),
            (By.XPATH, "//button[contains(text(), 'Importar')]")
        ]
        
        button = None
        for by, selector in selectors:
            try:
                button = wait.until(EC.element_to_be_clickable((by, selector)))
                if button:
                    print(f"✓ Botão encontrado usando {by}: {selector}")
                    break
            except:
                continue
        
        if not button:
            raise Exception("Não foi possível encontrar o botão 'Importar'")
        
        # Tenta diferentes métodos para clicar no botão
        click_methods = [
            lambda: button.click(),
            lambda: driver.execute_script("arguments[0].click();", button),
            lambda: ActionChains(driver).move_to_element(button).click().perform(),
            lambda: driver.execute_script("doAction(false,'POST','Proposal','ProposalImport', ['[gkz]w2IUB5bc32hQzrvmCR_SRDnb/Yzq7MZSW1QzbP/jIsKRmIjcdANp/hMuB3lpYQMPvVw9NKSJP_s2ds48eRcsZev3x4MThYva15dYA6JwPO0=']);")
        ]
        
        for i, click_method in enumerate(click_methods, 1):
            try:
                print(f"Tentativa {i} de clicar no botão...")
                click_method()
                print("✓ Clique realizado com sucesso!")
                return True
            except Exception as e:
                print(f"Tentativa {i} falhou: {str(e)}")
                if i == len(click_methods):
                    raise Exception("Todas as tentativas de clique falharam")
                continue
                
    except Exception as e:
        print(f"Erro ao clicar no botão 'Importar': {str(e)}")
        return False

def find_number_in_table(driver, number):
    try:
        print("\nLocalizando o processo na tabela...")
        # Espera a tabela específica carregar
        print("Aguardando tabela carregar...")
        table_wrapper = WebDriverWait(driver, 20).until(  # Increased timeout to 20 seconds
            EC.presence_of_element_located((By.XPATH, '//*[@id="tableProcessData_wrapper"]'))
        )
        print("✓ Tabela encontrada")
        
        # Encontra a tabela dentro do wrapper
        print("Buscando dados da tabela...")
        table = WebDriverWait(driver, 10).until(  # Added explicit wait for table
            EC.presence_of_element_located((By.ID, "tableProcessData"))
        )
        
        # Dá um tempo extra para garantir que os dados carregaram
        time.sleep(3)  # Increased wait time
        
        # Espera explicitamente pelas linhas da tabela
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tableProcessData tr"))
        )
        print(f"Encontradas {len(rows)} linhas na tabela")
        
        # Procura o número em cada linha
        print(f"\nProcurando processo número {number}...")
        for index, row in enumerate(rows, start=1):
            try:
                # Espera explicitamente pelas células de cada linha
                cells = WebDriverWait(driver, 5).until(
                    lambda d: row.find_elements(By.TAG_NAME, "td")
                )
                
                if not cells:  # Skip if no cells found (likely header row)
                    continue
                    
                print(f"\nAnalisando linha {index} - Células encontradas: {len(cells)}")
                
                for cell_index, cell in enumerate(cells):
                    try:
                        cell_text = cell.text.strip()  # Added strip() to clean the text
                        if not cell_text:  # Skip empty cells
                            continue
                            
                        print(f"Verificando célula {cell_index + 1}: {cell_text}")
                        if number in cell_text:
                            print(f"\n✓ Processo {number} encontrado na linha {index}, célula {cell_index + 1}")
                            
                            print("\nBuscando botão de ação...")
                            try:
                                # Espera explicitamente pelo botão
                                link = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable(
                                        (By.CSS_SELECTOR, "td.tablebutton > a.btn.btn-primary.btn-sm")
                                    )
                                )
                                
                                if click_href_link(driver, link):
                                    print("✓ Link clicado com sucesso!")
                                else:
                                    print("❌ Não foi possível clicar no link")
                            except Exception as btn_error:
                                print(f"\n⚠ Erro ao buscar botão: {btn_error}")
                            
                            return "✓ Busca concluída!"
                    except Exception as cell_error:
                        print(f"⚠ Erro ao ler célula {cell_index + 1}: {cell_error}")
                        continue
                        
            except Exception as row_error:
                print(f"⚠ Erro ao analisar linha {index}: {row_error}")
                continue
        
        print("\n❌ Processo não encontrado após verificar todas as linhas")
        return f"❌ Processo número {number} não foi encontrado na tabela."
        
    except Exception as e:
        print(f"\n⚠ Erro durante a busca: {e}")
        return f"⚠ Erro ao procurar na tabela: {e}"

def download_excel_model(driver):
    try:
        print("Procurando botão 'Baixar Modelo'...")
        
        # Tenta diferentes métodos para encontrar o botão
        selectors = [
            (By.XPATH, "//*[@id='vzk3kwmtqContentModal']/div[2]/button"),
            (By.CSS_SELECTOR, "#vzk3kwmtqContentModal > div.modal-body > button"),
            (By.XPATH, "//button[contains(@onclick, 'ProposalExportModel')]"),
            (By.CSS_SELECTOR, "button.btn.btn-primary.btn-sm[onclick*='ProposalExportModel']"),
            (By.XPATH, "//button[@class='btn btn-primary btn-sm' and contains(@onclick, 'ProposalExportModel')]")
        ]
        
        button = None
        wait = WebDriverWait(driver, 10)
        
        for by, selector in selectors:
            try:
                button = wait.until(
                    EC.presence_of_element_located((by, selector))
                )
                print(f"✓ Botão encontrado usando {by}: {selector}")
                break
            except:
                continue
        
        if not button:
            print("⚠ Botão 'Baixar Modelo' não encontrado")
            return None
        
        print("Clicando no botão 'Baixar Modelo'...")
        
        # Configura o diretório de download
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Lista os arquivos antes do download
        before = set(glob.glob(os.path.join(project_dir, "*.xlsx")))
        
        # Clica no botão
        button.click()
        
        print("Aguardando download do arquivo...")
        
        # Espera até 60 segundos pelo download
        max_wait = 60
        downloaded_file = None
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            # Lista os arquivos após o download
            after = set(glob.glob(os.path.join(project_dir, "*.xlsx")))
            new_files = after - before
            
            if new_files:
                # Pega o arquivo mais recente
                downloaded_file = max(new_files, key=os.path.getctime)
                
                # Verifica se o arquivo está completamente baixado (não tem extensão .tmp ou .crdownload)
                if not (downloaded_file.endswith('.tmp') or downloaded_file.endswith('.crdownload')):
                    # Tenta abrir o arquivo para garantir que está completo
                    try:
                        with open(downloaded_file, 'rb') as f:
                            pd.read_excel(f)
                        print(f"✓ Arquivo baixado com sucesso: {downloaded_file}")
                        break
                    except Exception:
                        print("Arquivo ainda está sendo baixado...")
                        time.sleep(1)
                        continue
            
            time.sleep(1)
        
        if not downloaded_file:
            # Se não encontrou o arquivo, tenta procurar por nome específico
            possible_files = glob.glob(os.path.join(project_dir, "*Proposta*.xlsx"))
            if possible_files:
                downloaded_file = max(possible_files, key=os.path.getctime)
                print(f"✓ Arquivo encontrado por nome: {downloaded_file}")
            else:
                raise TimeoutError("Arquivo não foi baixado")
        
        # Espera um pouco para garantir que o arquivo foi completamente baixado
        time.sleep(2)
        
        return downloaded_file
        
    except Exception as e:
        print(f"Erro ao baixar Excel: {str(e)}")
        return None


    try:
        print("\nCriando novo arquivo Excel com modificações...")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Lê o arquivo original usando pandas
        print("Lendo arquivo original...")
        df = pd.read_excel(original_file)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Modifica todos os valores da terceira coluna para 0
        # third_column = df.columns[2]  # Pega o nome da terceira coluna
        # print(f"Modificando valores da coluna: {third_column}")
        
        # Cria uma cópia do DataFrame
        new_df = df.copy()
        
        # Modifica os valores da terceira coluna para 0, mantendo o cabeçalho
        # new_df.iloc[1:, 2] = 0
        
        # Salva o novo arquivo
        new_filename = os.path.join(project_dir, f"proposta_{process_number}.xlsx")
        final_sheet_name = f"{sheet_name} {process_number}"  # Define o nome personalizado da aba

         # Cria um novo arquivo Excel com openpyxl
        wb = Workbook()
        ws = wb.active
        ws.title = final_sheet_name  # Renomeia a aba
        
        # Escreve os dados do DataFrame na aba
        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)
        
        # Salva o arquivo Excel
        wb.save(new_filename)
        print(f"✓ Novo arquivo salvo como: {new_filename} (Aba: {final_sheet_name})")
        
        return new_filename
        
    except Exception as e:
        print(f"Erro ao criar novo Excel: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return None

    excel = None
    workbook = None
    
    try:
        print("\nCriando novo arquivo Excel com modificações...")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Carrega as configurações
        items_file = os.path.join(project_dir, "items_data.json")
        mark_all_as_proprio = False
        if os.path.exists(items_file):
            with open(items_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                mark_all_as_proprio = config.get("mark_all_as_proprio", False)
        
        # Lê o arquivo original usando pandas
        print("Lendo arquivo original...")
        df = pd.read_excel(original_file)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Cria uma cópia do DataFrame
        new_df = df.copy()
        
        # Só zera os valores se não estiver marcado para marcar todos
        if not mark_all_as_proprio:
            # Modifica todos os valores da terceira coluna para 0
            third_column = df.columns[2] # Pega o nome da terceira coluna
            print(f"Modificando valores da coluna: {third_column}")
            new_df.iloc[1:, 2] = 0
            print("✓ Valores zerados na terceira coluna")
        else:
            print("✓ Mantendo valores originais (marcar todos ativo)")
        
        # Preenche automaticamente os campos marca e modelo com "Própria"
        if 'marca' in [col.lower() for col in new_df.columns]:
            marca_col = next(col for col in new_df.columns if col.lower() == 'marca')
            new_df[marca_col] = 'Própria'
            print("✓ Campo 'marca' preenchido com 'Própria'")
            
        if 'modelo' in [col.lower() for col in new_df.columns]:
            modelo_col = next(col for col in new_df.columns if col.lower() == 'modelo')
            new_df[modelo_col] = 'Própria'
            print("✓ Campo 'modelo' preenchido com 'Própria'")
        
        # Salva o novo arquivo
        new_filename = os.path.join(project_dir, f"proposta_{process_number}.xlsx")
        new_df.to_excel(new_filename, index=False)
        print(f"✓ Novo arquivo salvo como: {new_filename}")

        # Aguarda um pouco antes de iniciar o Excel
        print("Aguardando 5 segundos antes de iniciar o Excel...")
        time.sleep(5)
        
        # Inicia o Excel usando win32com
        print("Iniciando Excel...")
        excel = win32com.client.Dispatch("Excel.Application")
        
        # Configura o Excel para abrir em primeiro plano
        excel.Visible = True
        excel.DisplayAlerts = False # Desativa alertas
        
        # Força o Excel a ficar em primeiro plano
        try:
            # Encontra a janela do Excel
            app = Application().connect(path="EXCEL.EXE")
            excel_window = app.window(title_re=".*Excel.*")
            excel_window.set_focus()
        except Exception as e:
            print(f"Aviso: Não foi possível trazer Excel para primeiro plano: {str(e)}")
        
        # Aguarda o Excel iniciar (5 segundos)
        print("Aguardando Excel inicializar...")
        time.sleep(5)
        
        print(f"Abrindo arquivo: {new_filename}")
        workbook = excel.Workbooks.Open(new_filename)
        
        # Aguarda o arquivo abrir (5 segundos)
        print("Aguardando arquivo abrir...")
        time.sleep(5)
        
        # Força foco na janela do Excel novamente antes de salvar
        try:
            excel_window = app.window(title_re=".*Excel.*")
            excel_window.set_focus()
        except:
            pass
        
        # Salva usando Ctrl+S
        print("Salvando arquivo...")
        send_keys('^s') # Simula Ctrl+S
        time.sleep(3) # Aguarda o salvamento
        
        # Fecha o Excel
        print("Fechando Excel...")
        workbook.Close(SaveChanges=True)
        time.sleep(2)
        excel.Quit()
        
        # Aguarda o Excel fechar completamente
        print("Aguardando Excel fechar completamente...")
        time.sleep(3)
        
        print("✓ Excel processado e salvo com sucesso!")
        return new_filename
        
    except Exception as e:
        print(f"Erro ao criar novo Excel: {str(e)}")
        try:
            # Tenta fechar o Excel em caso de erro
            if workbook:
                workbook.Close(SaveChanges=False)
            if excel:
                excel.Quit()
        except:
            pass
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return None

def create_modified_excel(original_file, process_number):
    excel = None
    workbook = None
    
    try:
        print("\nCriando novo arquivo Excel com modificações...")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Carrega as configurações
        items_file = os.path.join(project_dir, "items_data.json")
        mark_all_as_proprio = False
        if os.path.exists(items_file):
            with open(items_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                mark_all_as_proprio = config.get("mark_all_as_proprio", False)
        
        # Lê o arquivo original usando pandas
        print("Lendo arquivo original...")
        df = pd.read_excel(original_file)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Cria uma cópia do DataFrame
        new_df = df.copy()
        
        # Só zera os valores se não estiver marcado para marcar todos
        # if not mark_all_as_proprio:
        #     third_column = df.columns[2]
        #     print(f"Modificando valores da coluna: {third_column}")
        #     new_df.iloc[1:, 2] = 0
        #     print("✓ Valores zerados na terceira coluna")
        # else:
        #     print("✓ Mantendo valores originais (marcar todos ativo)")
        
        # Preenche automaticamente os campos marca e modelo
        if 'marca' in [col.lower() for col in new_df.columns]:
            marca_col = next(col for col in new_df.columns if col.lower() == 'marca')
            new_df[marca_col] = 'Própria'
            print("✓ Campo 'marca' preenchido com 'Própria'")
            
        if 'modelo' in [col.lower() for col in new_df.columns]:
            modelo_col = next(col for col in new_df.columns if col.lower() == 'modelo')
            new_df[modelo_col] = 'Própria'
            print("✓ Campo 'modelo' preenchido com 'Própria'")
        
        # Salva o novo arquivo
        new_filename = os.path.join(project_dir, f"proposta_{process_number}.xlsx")
        new_df.to_excel(new_filename, index=False)
        print(f"✓ Novo arquivo salvo como: {new_filename}")

        try:
            # Inicia o Excel de forma invisível
            print("Iniciando Excel...")
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            
            # Abre o arquivo
            print(f"Abrindo arquivo: {new_filename}")
            workbook = excel.Workbooks.Open(new_filename)
            
            # Salva usando método nativo do Excel
            print("Salvando arquivo...")
            workbook.Save()
            
            # Tenta salvar usando SendKeys como backup
            try:
                excel.Visible = True
                app = Application().connect(path="EXCEL.EXE")
                excel_window = app.window(title_re=".*Excel.*")
                if excel_window.exists():
                    excel_window.set_focus()
                    send_keys('^s')
                    time.sleep(1)
            except Exception as e:
                print(f"Aviso: Método alternativo de salvamento falhou: {str(e)}")
            
            # Salva novamente usando método nativo
            workbook.Save()
            
            # Fecha tudo
            workbook.Close(SaveChanges=True)
            excel.Quit()
            
            # Aguarda o arquivo ser liberado
            max_retries = 10
            while max_retries > 0 and is_file_locked(new_filename):
                time.sleep(1)
                max_retries -= 1
            
            print("✓ Excel processado e salvo com sucesso!")
            return new_filename
            
        except Exception as excel_error:
            print(f"Erro ao manipular Excel: {excel_error}")
            if workbook:
                try:
                    workbook.Close(SaveChanges=False)
                except:
                    pass
            if excel:
                try:
                    excel.Quit()
                except:
                    pass
            raise excel_error
            
    except Exception as e:
        print(f"Erro ao criar novo Excel: {str(e)}")
        try:
            if workbook:
                workbook.Close(SaveChanges=False)
            if excel:
                excel.Quit()
        except:
            pass
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return None

# def process_excel(excel_file, sheet_name="Proposta"):
    """
    Processa o arquivo Excel, preenchendo os valores conforme os itens cadastrados,
    priorizando os menores valores.
    """
    
    try:
        print("\nProcessando arquivo Excel...")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Verifica se o arquivo existe e está completo
        if not os.path.exists(excel_file):
            print(f"⚠ Arquivo não encontrado: {excel_file}")
            return None
            
        # Espera o arquivo estar completamente baixado
        max_retries = 10
        while max_retries > 0:
            try:
                with open(excel_file, 'rb') as f:
                    # Tenta ler o arquivo
                    pd.read_excel(f)
                break
            except Exception:
                time.sleep(1)
                max_retries -= 1
                if max_retries == 0:
                    print("⚠ Timeout aguardando arquivo ser liberado")
                    return None
        
        # Carrega os dados dos itens cadastrados
        items_file = os.path.join(project_dir, "items_data.json")
        if os.path.exists(items_file):
            with open(items_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                items_data = config.get("items_data", {})
                mark_all_as_proprio = config.get("mark_all_as_proprio", True)
        else:
            items_data = {}
            mark_all_as_proprio = False
        
        # Lê o arquivo Excel
        print("Lendo arquivo Excel...")
        df = pd.read_excel(excel_file)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Extrai o número do processo do nome do arquivo
        process_number = os.path.splitext(os.path.basename(excel_file))[0]
        
        # Remove qualquer arquivo Excel existente com o mesmo padrão de nome
        new_filename = os.path.join(project_dir, f"proposta_{process_number}.xlsx")
        if os.path.exists(new_filename):
            try:
                os.remove(new_filename)
                print(f"✓ Arquivo Excel anterior removido: {os.path.basename(new_filename)}")
            except Exception as e:
                print(f"⚠ Não foi possível remover o arquivo anterior: {str(e)}")
                # Se não conseguir remover, gera um nome único
                base_name = os.path.join(project_dir, f"proposta_{process_number}")
                counter = 1
                while os.path.exists(f"{base_name}_{counter}.xlsx"):
                    counter += 1
                new_filename = f"{base_name}_{counter}.xlsx"
        
        # Preenche automaticamente os campos marca e modelo com "Própria"
        if 'marca' in [col.lower() for col in df.columns]:
            marca_col = next(col for col in df.columns if col.lower() == 'marca')
            df[marca_col] = 'Própria'
            print("✓ Campo 'marca' preenchido com 'Própria'")
            
        if 'modelo' in [col.lower() for col in df.columns]:
            modelo_col = next(col for col in df.columns if col.lower() == 'modelo')
            df[modelo_col] = 'Própria'
            print("✓ Campo 'modelo' preenchido com 'Própria'")
        
        # Salva o arquivo Excel
        print(f"\nSalvando arquivo Excel: {new_filename}")
        writer = pd.ExcelWriter(new_filename, engine='openpyxl')
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()
        
        # Abre o Excel para edição manual
        print("\nAbrindo Excel para revisão manual...")
        os.startfile(new_filename)
        
        # Aguarda confirmação do usuário
        input("\nPressione ENTER após salvar e fechar o arquivo Excel...")
        
        print("✓ Arquivo Excel processado e salvo manualmente")
        return new_filename
        
    except Exception as e:
        print(f"Erro ao processar Excel: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return None
def process_excel(excel_file):
    """
    Processa o arquivo Excel, preenchendo os valores conforme os itens cadastrados,
    priorizando os menores valores.
    """
    try:
        # Extrai o número do processo do nome do arquivo
        process_number = os.path.splitext(os.path.basename(excel_file))[0]
        
        # Cria o novo arquivo Excel com as modificações
        modified_file = create_modified_excel(excel_file, process_number)
        
        if modified_file:
            print("✓ Excel processado com sucesso!")
            return modified_file
        else:
            print("⚠ Erro ao processar Excel")
            return None
            
    except Exception as e:
        print(f"Erro ao processar Excel: {str(e)}")
        return None

def excel_to_json(excel_file, process_number):

    try:
        print("\nConvertendo Excel para JSON...")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Lê o arquivo Excel
        print("Lendo arquivo Excel...")
        df = pd.read_excel(excel_file)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Converte o DataFrame para um dicionário de registros
        data = {
            "processo": process_number,
            "data_captura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "colunas": list(df.columns),
            "dados": []
        }
        
        # Itera sobre as linhas e cria a lista de dados
        for index, row in df.iterrows():
            row_dict = {}
            for col_num, (col_name, value) in enumerate(row.items()):
                # Se for a terceira coluna (índice 2) e não for a primeira linha (cabeçalho)
                if col_num == 2 and index > 0:
                    row_dict[col_name] = 0
                else:
                    # Converte para string se for NaN ou outro tipo não serializável
                    if pd.isna(value):
                        row_dict[col_name] = ""
                    else:
                        row_dict[col_name] = str(value)
            data["dados"].append(row_dict)
        
        # Salva o JSON
        json_filename = os.path.join(project_dir, f"proposta_{process_number}.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✓ Arquivo JSON salvo como: {json_filename}")
        return json_filename
        
    except Exception as e:
        print(f"Erro ao converter para JSON: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return None


    """
    Processa o arquivo Excel, preenchendo os valores conforme os itens cadastrados,
    priorizando os menores valores.
    """

def is_file_locked(file_path):
    """
    Verifica se um arquivo está bloqueado/em uso
    """
    try:
        with open(file_path, 'r+b'):
            return False
    except IOError:
        return True

def upload_excel(driver, excel_file):
    """
    Faz o upload do arquivo Excel modificado.
    """
    try:
        print("\nIniciando upload do arquivo Excel...")
        
        # Localiza o elemento de upload
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fileUpload"))
        )
        
        # Envia o arquivo
        upload_input.send_keys(excel_file)
        
        # Aguarda um momento após o upload
        time.sleep(2)
        
        print(f"✓ Arquivo enviado: {os.path.basename(excel_file)}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao fazer upload do arquivo: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return False

def click_send_button(driver):
    """
    Clica no botão de enviar após fazer o upload do arquivo.
    """
    try:
        print("\nClicando no botão Enviar...")
        
        # Aguarda o botão ficar visível e clicável
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnSend"))
        )
        
        # Clica no botão
        send_button.click()
        print("✓ Botão 'Enviar' clicado com sucesso")
        
        # Aguarda um pouco para garantir que o envio foi processado
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"Erro ao clicar no botão Enviar: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return False

# def click_button_documents(driver):
    try:
        print("\nProcurando botão Documentos...")

        # Lista de seletores para tentar encontrar o botão
        selector_buttons = [
            (By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Documentos')]"),
            (By.XPATH, "//*[@id='jsonForm1']/table/tbody/tr[5]/td/table/tbody/tr/td[4]/a"),
            (By.CSS_SELECTOR, "a.disableOnClick.btn.btn-primary"),
            (By.LINK_TEXT, "Documentos")
        ]

        documents_button = None

        # Tenta cada seletor até encontrar o botão
        for by, selector in selector_buttons:
            try:
                print(f"Tentando localizar botão com {by}: {selector}")
                documents_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((by, selector))
                )
                if documents_button and documents_button.is_displayed():
                    print(f"✓ Botão encontrado usando {by}: {selector}")
                    break
            except Exception as e:
                print(f"Não foi possível encontrar com {by}: {selector}")
                continue

        if not documents_button:
            raise Exception("Botão 'Documentos' não encontrado com nenhum dos seletores")

        # Clica no botão
        driver.execute_script("arguments[0].click();", documents_button)

        # Aguarda a abertura do modal
        time.sleep(3)

        # Captura os dados da tabela usando os XPaths fornecidos
        try:
            print("Extraindo informações de documentos...")

            # Verifica se a tabela existe
            table_xpath = "//*[@id='tableDocumentsAttached']"
            if not driver.find_elements(By.XPATH, table_xpath):
                print("Tabela de documentos não encontrada, fechando o modal...")
                close_button_xpath = "//*[@id='DocumentContentModal']/div[1]/button/span"
                driver.find_element(By.XPATH, close_button_xpath).click()
                return False

            # Captura os documentos
            documents_data = []
            rows = driver.find_elements(By.XPATH, "//*[@id='tableDocumentsAttached']/tbody/tr")
            for row in rows:
                name = row.find_element(By.XPATH, "./td[1]").text.strip()
                required = row.find_element(By.XPATH, "./td[5]").text.strip().lower() == "sim"
                documents_data.append({"name": name, "required": required})

            if not documents_data:
                print("Nenhum documento encontrado, fechando o modal...")
                close_button_xpath = "//*[@id='DocumentContentModal']/div[1]/button/span"
                driver.find_element(By.XPATH, close_button_xpath).click()
                return False

            # Chama a interface de documentos
            from gui import DocumentsDialog
            import tkinter as tk

            root = tk.Tk()
            root.withdraw()  # Oculta a janela principal
            DocumentsDialog(root, documents_data)
            root.mainloop()

            return True

        except Exception as e:
            print(f"Erro ao extrair informações de documentos: {str(e)}")
            return False

    except Exception as e:
        print(f"Erro ao clicar no botão Documentos: {str(e)}")
        return False

def click_documents_button(driver):
    """
    Clica no botão 'Documentos' após enviar a proposta usando múltiplas estratégias.
    """
    try:
        # Lista de seletores e estratégias para encontrar o botão
        strategies = [
            (By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Documentos')]"),
            (By.XPATH, "//*[@id='jsonForm1']/table/tbody/tr[5]/td/table/tbody/tr/td[4]/a"),
            (By.CSS_SELECTOR, "a.disableOnClick.btn.btn-primary"),
            (By.LINK_TEXT, "Documentos")
        ]

        for by, selector in strategies:
            try:
                # Tenta encontrar o elemento e aguardar até estar clicável
                documents_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((by, selector))
                )
                
                # Tenta diferentes métodos de clique
                try:
                    # Método 1: Clique direto
                    documents_button.click()
                    print("✓ Botão Documentos clicado com sucesso (clique direto)")
                    return True
                except:
                    try:
                        # Método 2: Clique via JavaScript
                        driver.execute_script("arguments[0].click();", documents_button)
                        print("✓ Botão Documentos clicado com sucesso (via JavaScript)")
                        return True
                    except:
                        try:
                            # Método 3: Simular clique via JavaScript modal
                            driver.execute_script("$('#DocumentModal').modal('show');")
                            print("✓ Modal de Documentos aberto com sucesso (via JavaScript)")
                            return True
                        except:
                            continue
            except:
                continue
        
        # Se chegou aqui, nenhuma estratégia funcionou
        print("⚠ Nenhuma estratégia de clique funcionou para o botão Documentos")
        return False
        
    except Exception as e:
        print(f"⚠ Erro ao tentar clicar no botão Documentos: {str(e)}")
        return False
        
# def processar_documentos(driver, caminho_arquivo):
    """
    Realiza o processo de clicar no botão 'Adicionar documento', fazer upload do arquivo vazio.pdf,
    fechar a aba de upload e salvar o documento.
    """
    # Localiza todos os botões "Adicionar documento"
    botoes_adicionar = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Adicionar documento']"))
    )

    contador = 0

    for botao in botoes_adicionar:
        if contador >= 3:
            break

        try:
            # Clica no botão "Adicionar documento"
            botao.click()
            time.sleep(2) # Aguarda a janela de upload abrir

            # Clica no botão "Upload de arquivos"
            botao_upload = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
            )
            botao_upload.click()
            time.sleep(2)

            # Seleciona o arquivo para upload
            input_arquivo = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "selectFile"))
            )
            input_arquivo.send_keys(caminho_arquivo)
            time.sleep(2)

            # Clica no botão "Fechar" para fechar a aba de upload
            botao_fechar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "btnUploadClose"))
            )
            botao_fechar.click()
            time.sleep(2)

            # Clica no botão "Salvar Documento"
            botao_salvar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "saveNewDoc"))
            )
            botao_salvar.click()
            time.sleep(5) # Aguarda salvar antes de passar para o próximo botão

        except Exception as e:
            print(f"Erro ao processar o documento: {e}")
            continue
    
    # Fecha a aba de documentos
    try:
        botao_fechar_modal = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
        )
        botao_fechar_modal.click()
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao fechar a aba de documentos: {e}")


    # Clica no botão Salvar Proposta
    try:
        botao_salvar_proposta = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSaveProposal']"))
        )
        botao_salvar_proposta.click()
        time.sleep(2)

        # Aguarda e clica no botão Sim para confirmar o salvamento
        botao_confirmar = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/button[2]"))
        )
        botao_confirmar.click()
        time.sleep(2)
        
    except Exception as e:
        print(f"Erro ao clicar no botão Salvar Proposta ou confirmar: {e}")
        
# def processar_documentos(driver, caminho_arquivo):

    """
    Processa os documentos com base nos elementos e seletores fornecidos no código original do usuário.
    Inclui lógica avançada para verificar obrigatoriedades e garantir o processamento correto.
    """
    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )
        
        # Coleta todas as linhas da tabela
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []

        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1):  # Ignora o cabeçalho
            try:
                # Obtém o valor do campo "Obrigatório"
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()

                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório - ignorando")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        # Se não houver documentos obrigatórios, fecha o modal e termina
        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado.")
            try:
                print("Fechando o modal...")
                botao_fechar_modal = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
                )
                botao_fechar_modal.click()
                print("✓ Modal fechado com sucesso.")
            except Exception as e:
                print(f"⚠ Erro ao fechar o modal: {str(e)}")
            return

        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")

        # Processa os documentos obrigatórios
        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"\n[{index}] Processando documento obrigatório: '{nome_documento}'")

                # Clica no botão "Adicionar documento"
                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                print(f"[{index}] Clicando no botão 'Adicionar documento'...")
                botao_adicionar.click()
                time.sleep(2)  # Aguarda a janela de upload abrir

                # Clica no botão "Upload de arquivos"
                botao_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                )
                botao_upload.click()
                time.sleep(2)

                # Seleciona o arquivo para upload
                input_arquivo = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "selectFile"))
                )
                input_arquivo.send_keys(caminho_arquivo)
                time.sleep(2)

                # Clica no botão "Fechar" para fechar a aba de upload
                botao_fechar_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                )
                botao_fechar_upload.click()
                time.sleep(2)

                # Clica no botão "Salvar Documento"
                botao_salvar = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                )
                botao_salvar.click()
                print(f"✓ [{index}] Documento '{nome_documento}' salvo com sucesso.")
                time.sleep(5)  # Aguarda salvar antes de passar para o próximo documento

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        # Fecha o modal principal
        try:
            print("\nFechando o modal principal...")
            botao_fechar_modal = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
            )
            botao_fechar_modal.click()
            print("✓ Modal principal fechado com sucesso.")
            time.sleep(5)
        except Exception as e:
            print(f"⚠ Erro ao fechar o modal principal: {str(e)}")
            return
        # Clica no botão "Salvar Proposta"
        try:
            print("\nSalvando a proposta...")
            botao_salvar_proposta = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSaveProposal']"))
            )

            print("Clicando no botão de fechar modal de errorContent")
            botao_fechar_modal_content_Error = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*//*[@id='btnClose']"))
            )
            botao_fechar_modal_content_Error.click()
             
            botao_salvar_proposta.click()
            time.sleep(2)

            # Aguarda e clica no botão "Sim" para confirmar o salvamento
            print("Confirmando o salvamento...")
            botao_confirmar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/button[2]"))
            )
            botao_confirmar.click()
            print("✓ Proposta salva com sucesso!")
            time.sleep(2)
        except Exception as e:
            print(f"⚠ Erro ao clicar no botão 'Salvar Proposta' ou confirmar: {str(e)}")

    except Exception as e:
        print(f"⚠ Erro geral no processamento dos documentos: {str(e)}")

    """
    Processa os documentos, verifica se há arquivo obrigatório e ajusta o fluxo conforme necessário.
    """
    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )
        
        # Coleta todas as linhas da tabela
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []

        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1):  # Ignora o cabeçalho
            try:
                # Obtém o valor do campo "Obrigatório"
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()

                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório - ignorando")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        # Se não houver documentos obrigatórios, processa o primeiro item
        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado. Processando o primeiro item da tabela...")
            try:
                primeiro_item = linhas[1]  # Primeiro item após o cabeçalho
                nome_documento = primeiro_item.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"Processando o primeiro item: '{nome_documento}'")

                # Clica no botão "Adicionar documento"
                botao_adicionar = primeiro_item.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                print("Clicando no botão 'Adicionar documento'...")
                botao_adicionar.click()
                time.sleep(2)

                # Realiza o upload do arquivo
                botao_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                )
                botao_upload.click()
                time.sleep(2)

                input_arquivo = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "selectFile"))
                )
                input_arquivo.send_keys(caminho_arquivo)
                time.sleep(2)

                # Fecha a aba de upload
                botao_fechar_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                )
                botao_fechar_upload.click()
                time.sleep(2)

                # Salva o documento
                botao_salvar = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                )
                botao_salvar.click()
                print("✓ Documento do primeiro item salvo com sucesso.")
                time.sleep(2)

                # Fecha o modal principal
                botao_fechar_modal = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
                )
                botao_fechar_modal.click()
                print("✓ Modal fechado com sucesso.")
                return  # Finaliza o processo, pois nenhum obrigatório foi encontrado
            except Exception as e:
                print(f"⚠ Erro ao processar o primeiro item: {str(e)}")
                return

        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")

        # Processa os documentos obrigatórios
        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"\n[{index}] Processando documento obrigatório: '{nome_documento}'")

                # Clica no botão "Adicionar documento"
                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                print(f"[{index}] Clicando no botão 'Adicionar documento'...")
                botao_adicionar.click()
                time.sleep(2)  # Aguarda a janela de upload abrir

                # Verifica se já existe um arquivo anexado
                try:
                    campo_arquivo = driver.find_element(By.XPATH, f"//*[@id='propDoc{index}']/td[1]").text.strip()
                    if "vazio.pdf" in campo_arquivo.lower():
                        print(f"[{index}] Documento 'vazio.pdf' já anexado. Selecionando...")
                        botao_selecionar = driver.find_element(By.XPATH, f"//*[@id='propDoc{index}']/td[5]/button")
                        botao_selecionar.click()
                        print(f"✓ [{index}] Documento selecionado com sucesso.")
                        time.sleep(2)
                        continue  # Passa para o próximo documento obrigatório
                except Exception as e:
                    print(f"[{index}] Erro ao verificar documento existente: {str(e)}")

                # Clica no botão "Upload de arquivos"
                botao_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                )
                botao_upload.click()
                time.sleep(2)

                # Seleciona o arquivo para upload
                input_arquivo = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "selectFile"))
                )
                input_arquivo.send_keys(caminho_arquivo)
                time.sleep(2)

                # Clica no botão "Fechar" para fechar a aba de upload
                botao_fechar_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                )
                botao_fechar_upload.click()
                time.sleep(2)

                # Clica no botão "Salvar Documento"
                botao_salvar = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                )
                botao_salvar.click()
                print(f"✓ [{index}] Documento '{nome_documento}' salvo com sucesso.")
                time.sleep(5)  # Aguarda salvar antes de passar para o próximo documento

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        # Fecha o modal principal
        try:
            print("\nFechando o modal principal...")
            botao_fechar_modal = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
            )
            botao_fechar_modal.click()
            print("✓ Modal principal fechado com sucesso.")
            time.sleep(2)
        except Exception as e:
            print(f"⚠ Erro ao fechar o modal principal: {str(e)}")
            return

        # Clica no botão "Salvar Proposta"
        try:
            print("\nSalvando a proposta...")
            botao_salvar_proposta = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSaveProposal']"))
            )
            botao_salvar_proposta.click()
            time.sleep(2)

            # Aguarda e clica no botão "Sim" para confirmar o salvamento
            print("Confirmando o salvamento...")
            botao_confirmar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/button[2]"))
            )
            botao_confirmar.click()
            print("✓ Proposta salva com sucesso!")
            time.sleep(2)
        except Exception as e:
            print(f"⚠ Erro ao clicar no botão 'Salvar Proposta' ou confirmar: {str(e)}")

    except Exception as e:
        print(f"⚠ Erro geral no processamento dos documentos: {str(e)}")

    """
    Processa os documentos com base nos elementos e seletores fornecidos no código original do usuário.
    Inclui lógica avançada para verificar obrigatoriedades e garantir o processamento correto.
    """
    def fechar_card_erro():
        try:
            card_erro = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='errorContentModal']"))
            )
            print("⚠ Card de erro detectado. Tentando fechar...")
            botao_fechar_card = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='errorContentModal']/div[1]/button"))
            )
            botao_fechar_card.click()
            print("✓ Card de erro fechado com sucesso.")
            return True
        except Exception as e:
            print(f"⚠ Nenhum card de erro detectado ou falha ao fechar: {str(e)}")
            return False

    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )

        # Coleta todas as linhas da tabela
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []

        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1):  # Ignora o cabeçalho
            try:
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()

                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório - ignorando")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado.")


        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")

        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"\n[{index}] Processando documento obrigatório: '{nome_documento}'")

                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                botao_adicionar.click()
                time.sleep(2)

                botao_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                )
                botao_upload.click()
                time.sleep(2)

                input_arquivo = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "selectFile"))
                )
                input_arquivo.send_keys(caminho_arquivo)
                time.sleep(2)

                botao_fechar_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                )
                botao_fechar_upload.click()
                time.sleep(2)

                botao_salvar = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                )
                botao_salvar.click()
                time.sleep(5)

                if fechar_card_erro():
                    print("Tentando salvar novamente após fechar o card de erro...")
                    botao_salvar.click()
                    time.sleep(5)

                print(f"✓ [{index}] Documento '{nome_documento}' salvo com sucesso.")

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        try:
            print("\nSalvando a proposta...")
            botao_salvar_proposta = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSaveProposal']"))
            )
            botao_salvar_proposta.click()
            time.sleep(2)

            print("Confirmando o salvamento...")
            botao_confirmar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/button[2]"))
            )
            botao_confirmar.click()
            print("✓ Proposta salva com sucesso!")
            time.sleep(2)

            if fechar_card_erro():
                print("Tentando salvar novamente a proposta após fechar o card de erro...")
                botao_salvar_proposta.click()
                time.sleep(2)

        except Exception as e:
            print(f"⚠ Erro ao clicar no botão 'Salvar Proposta' ou confirmar: {str(e)}")

    except Exception as e:
        print(f"⚠ Erro geral no processamento dos documentos: {str(e)}")


    """
    Processa os documentos com base nos elementos e seletores fornecidos no código original do usuário.
    Inclui lógica avançada para verificar obrigatoriedades e garantir o processamento correto.
    """
    def fechar_card_erro():
        try:
            card_erro = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='errorContentModal']"))
            )
            print("⚠ Card de erro detectado. Tentando fechar...")
            botao_fechar_card = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='errorContentModal']/div[1]/button"))
            )
            botao_fechar_card.click()
            print("✓ Card de erro fechado com sucesso.")
            return True
        except Exception as e:
            print(f"⚠ Nenhum card de erro detectado ou falha ao fechar: {str(e)}")
            return False

    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )

        # Coleta todas as linhas da tabela
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []

        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1):  # Ignora o cabeçalho
            try:
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()

                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório - ignorando")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado.")
            try:
                print("Fechando o modal...")
                botao_fechar_modal = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
                )
                botao_fechar_modal.click()
                print("✓ Modal fechado com sucesso.")
            except Exception as e:
                print(f"⚠ Erro ao fechar o modal: {str(e)}")
            return

        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")

        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"\n[{index}] Processando documento obrigatório: '{nome_documento}'")

                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                botao_adicionar.click()
                time.sleep(2)

                botao_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                )
                botao_upload.click()
                time.sleep(2)

                input_arquivo = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "selectFile"))
                )
                input_arquivo.send_keys(caminho_arquivo)
                time.sleep(2)

                botao_fechar_upload = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                )
                botao_fechar_upload.click()
                time.sleep(2)

                botao_salvar = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                )
                botao_salvar.click()
                time.sleep(5)

                if fechar_card_erro():
                    print("Tentando salvar novamente após fechar o card de erro...")
                    botao_salvar.click()
                    time.sleep(5)

                print(f"✓ [{index}] Documento '{nome_documento}' salvo com sucesso.")

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        try:
            print("\nFechando o modal principal...")
            botao_fechar_modal = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='DocumentContentModal']/div[1]/button"))
            )
            botao_fechar_modal.click()
            print("✓ Modal principal fechado com sucesso.")
            time.sleep(2)
        except Exception as e:
            print(f"⚠ Erro ao fechar o modal principal: {str(e)}")
            return

        try:
            print("\nSalvando a proposta...")
            botao_salvar_proposta = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSaveProposal']"))
            )
            botao_salvar_proposta.click()
            time.sleep(2)

            print("Confirmando o salvamento...")
            botao_confirmar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/button[2]"))
            )
            botao_confirmar.click()
            print("✓ Proposta salva com sucesso!")
            time.sleep(2)

            if fechar_card_erro():
                print("Tentando salvar novamente a proposta após fechar o card de erro...")
                botao_salvar_proposta.click()
                time.sleep(2)

        except Exception as e:
            print(f"⚠ Erro ao clicar no botão 'Salvar Proposta' ou confirmar: {str(e)}")

    except Exception as e:
        print(f"⚠ Erro geral no processamento dos documentos: {str(e)}")


# oficial def processar_documentos(driver, caminho_arquivo):
    """
    Processa os documentos conforme o valor do campo 'Obrigatório'.
    Primeiro verifica todos os itens obrigatórios e depois processa apenas os que têm 'SIM'.
    Se não houver nenhum SIM, fecha o modal.
    """
    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )
        
        # Primeiro, vamos coletar todas as linhas que têm "SIM" no campo obrigatório
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []
        
        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1): # [1:] para pular o cabeçalho
            try:
                # Obtém o valor da coluna "Obrigatório"
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                
                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório - ignorando")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        # Se não houver documentos obrigatórios, fecha o modal e termina
        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado.")
            try:
                print("Fechando o modal...")
                botao_fechar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='close' and @data-dismiss='modal']"))
                )
                botao_fechar.click()
                print("✓ Modal fechado com sucesso")
            except Exception as e:
                print(f"⚠ Erro ao fechar o modal: {str(e)}")
            return

        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")
        
        # Agora processa apenas as linhas obrigatórias
        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"\n[{index}] Processando documento obrigatório: '{nome_documento}'")
                
                # Clica no botão "Adicionar documento"
                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                print(f"[{index}] Clicando no botão 'Adicionar documento'...")
                botao_adicionar.click()
                time.sleep(2) # Aguarda a janela de upload abrir

                # Verifica se a tabela de documentos está presente
                print(f"[{index}] Verificando documentos existentes...")
                linhas_vazio = []
                try:
                    tabela_docs = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "tableParticipantDocuments"))
                    )
                    linhas_vazio = tabela_docs.find_elements(By.XPATH, ".//tr[.//td[contains(text(), 'vazio.pdf')]]")
                except:
                    print(f"[{index}] Tabela de documentos não encontrada - assumindo que não há documentos existentes")
                    linhas_vazio = []

                if linhas_vazio:
                    print(f"[{index}] Documento vazio.pdf encontrado. Selecionando...")
                    botao_selecionar = linhas_vazio[0].find_element(By.XPATH, ".//button[@title='Selecionar documento']")
                    botao_selecionar.click()
                    print(f"✓ [{index}] Documento vazio.pdf selecionado com sucesso.")
                    time.sleep(2)
                else:
                    print(f"[{index}] Documento vazio.pdf não encontrado. Realizando upload...")
                    # Clica no botão "Upload de arquivos"
                    botao_upload = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                    )
                    botao_upload.click()
                    print(f"✓ [{index}] Botão de upload clicado")

                    # Envia o arquivo vazio.pdf
                    input_arquivo = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.ID, "selectFile"))
                    )
                    input_arquivo.send_keys(caminho_arquivo)
                    print(f"✓ [{index}] Arquivo vazio.pdf enviado")

                    # Aguarda 3 segundos antes de fechar
                    time.sleep(3)
                    print(f"[{index}] Aguardando 3 segundos antes de fechar...")

                    # Fecha a aba de upload
                    botao_fechar_upload = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                    )
                    botao_fechar_upload.click()
                    print(f"✓ [{index}] Aba de upload fechada")

                    # Salva o novo documento
                    botao_salvar = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                    )
                    botao_salvar.click()
                    print(f"✓ [{index}] Documento salvo com sucesso")
                    time.sleep(2)

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        print("\n✓ Processamento de todos os documentos obrigatórios concluído com sucesso!")

        # Fecha o modal principal
        try:
            print("\nFechando o modal principal...")
            botao_fechar_modal = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='close' and @data-dismiss='modal']"))
            )
            botao_fechar_modal.click()
            print("✓ Modal principal fechado com sucesso")
            time.sleep(2) # Aguarda o modal fechar
        except Exception as e:
            print(f"⚠ Erro ao fechar o modal principal: {str(e)}")
            return

    except Exception as e:
        print(f"⚠ Erro geral no processamento dos documentos: {str(e)}")

# oficial V2 def processar_documentos(driver, caminho_arquivo):
    """
    Processa os documentos conforme o valor do campo 'Obrigatório'.
    Primeiro verifica todos os itens obrigatórios e depois processa apenas os que têm 'SIM'.
    Se não houver nenhum 'SIM', fecha o modal.
    """
    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )
        
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []

        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1):  # Ignora o cabeçalho
            try:
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()

                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório.")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório.")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        # Fecha o modal se não houver documentos obrigatórios
        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado. Fechando modal...")
            fechar_modal(driver, "//button[@class='close' and @data-dismiss='modal']")
            return

        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")

        # Processa documentos obrigatórios
        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"[{index}] Processando documento obrigatório: '{nome_documento}'")

                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                botao_adicionar.click()
                print(f"[{index}] Botão 'Adicionar documento' clicado.")
                time.sleep(2)

                # Verifica se a tabela de documentos já tem o vazio.pdf
                print(f"[{index}] Verificando documentos existentes...")
                try:
                    tabela_docs = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "tableParticipantDocuments"))
                    )
                    linhas_vazio = tabela_docs.find_elements(By.XPATH, ".//tr[.//td[contains(text(), 'vazio.pdf')]]")

                    if linhas_vazio:
                        print(f"[{index}] Documento vazio.pdf encontrado. Selecionando...")
                        botao_selecionar = linhas_vazio[0].find_element(By.XPATH, ".//button[@title='Selecionar documento']")
                        botao_selecionar.click()
                        print(f"✓ [{index}] Documento vazio.pdf selecionado com sucesso.")
                        time.sleep(2)
                    else:
                        print(f"[{index}] Documento vazio.pdf não encontrado. Realizando upload...")
                        # Clica no botão "Upload de arquivos"
                        botao_upload = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                        )
                        botao_upload.click()
                        print(f"✓ [{index}] Botão de upload clicado.")

                        # Envia o arquivo vazio.pdf
                        input_arquivo = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "selectFile"))
                        )
                        input_arquivo.send_keys(caminho_arquivo)
                        print(f"✓ [{index}] Arquivo vazio.pdf enviado.")

                        # Fecha a aba de upload
                        botao_fechar_upload = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                        )
                        botao_fechar_upload.click()
                        print(f"✓ [{index}] Aba de upload fechada.")

                        # Salva o novo documento
                        botao_salvar = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                        )
                        botao_salvar.click()
                        print(f"✓ [{index}] Documento salvo com sucesso.")
                        time.sleep(2)

                except Exception as e:
                    print(f"⚠ [{index}] Erro ao verificar tabela de documentos: {str(e)}")

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        print("\n✓ Processamento de todos os documentos obrigatórios concluído com sucesso!")

        # Fecha o modal principal
        try:
            print("\nFechando o modal principal...")
            botao_fechar_modal = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='close' and @data-dismiss='modal']"))
            )
            botao_fechar_modal.click()
            print("✓ Modal principal fechado com sucesso.")
            time.sleep(2)  # Aguarda o modal fechar
        except Exception as e:
            print(f"⚠ Erro ao fechar o modal principal: {str(e)}")
            return

    except Exception as e:
        print(f"⚠ Erro ao processar documentos: {str(e)}")

def processar_documentos(driver, caminho_arquivo):
    """
    Processa os documentos conforme o valor do campo 'Obrigatório'.
    Primeiro verifica todos os itens obrigatórios e depois processa apenas os que têm 'SIM'.
    Se não houver nenhum 'SIM', fecha o modal.
    """
    import os

    try:
        # Localiza a tabela de documentos anexados
        tabela = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tableDocumentsAttached"))
        )
        
        linhas = tabela.find_elements(By.XPATH, ".//tr")
        linhas_obrigatorias = []

        print("Verificando documentos obrigatórios...")
        for index, linha in enumerate(linhas[1:], start=1):  # Ignora o cabeçalho
            try:
                obrigatorio = linha.find_element(By.XPATH, ".//td[5]").text.strip().upper()
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()

                if obrigatorio == "SIM":
                    print(f"[{index}] Documento '{nome_documento}' é obrigatório.")
                    linhas_obrigatorias.append((index, linha))
                else:
                    print(f"[{index}] Documento '{nome_documento}' não é obrigatório.")
            except Exception as e:
                print(f"⚠ [{index}] Erro ao verificar obrigatoriedade: {str(e)}")
                continue

        # Fecha o modal se não houver documentos obrigatórios
        if not linhas_obrigatorias:
            print("✓ Nenhum documento obrigatório encontrado. Fechando modal...")
            fechar_modal(driver, "//button[@class='close' and @data-dismiss='modal']")
            return

        print(f"\nProcessando {len(linhas_obrigatorias)} documento(s) obrigatório(s)...")

        # Processa documentos obrigatórios
        for index, linha in linhas_obrigatorias:
            try:
                nome_documento = linha.find_element(By.XPATH, ".//td[1]").text.strip()
                print(f"[{index}] Processando documento obrigatório: '{nome_documento}'")

                botao_adicionar = linha.find_element(By.XPATH, ".//a[@title='Adicionar documento']")
                botao_adicionar.click()
                print(f"[{index}] Botão 'Adicionar documento' clicado.")
                time.sleep(2)

                # Verifica se a tabela de documentos já tem o vazio.pdf
                print(f"[{index}] Verificando documentos existentes...")
                try:
                    tabela_docs = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "tableParticipantDocuments"))
                    )
                    linhas_vazio = tabela_docs.find_elements(By.XPATH, ".//tr[.//td[contains(text(), 'vazio.pdf')]]")

                    if linhas_vazio:
                        print(f"[{index}] Documento vazio.pdf encontrado. Selecionando...")
                        botao_selecionar = linhas_vazio[0].find_element(By.XPATH, ".//button[@title='Selecionar documento']")
                        botao_selecionar.click()
                        print(f"✓ [{index}] Documento vazio.pdf selecionado com sucesso.")
                        time.sleep(2)
                    else:
                        print(f"[{index}] Documento vazio.pdf não encontrado. Realizando upload...")
                        
                        # Clica no botão "Upload de arquivos"
                        botao_upload = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@title='Upload de arquivos']"))
                        )
                        botao_upload.click()
                        print(f"✓ [{index}] Botão de upload clicado.")

                        # Aguarda o elemento de upload estar disponível
                        input_arquivo = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='selectFile']"))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", input_arquivo)

                        # Obtém o caminho absoluto do arquivo
                        caminho_absoluto = os.path.abspath(caminho_arquivo)
                        input_arquivo.send_keys(caminho_absoluto)
                        print(f"✓ [{index}] Arquivo vazio.pdf enviado: {caminho_absoluto}")
                        time.sleep(2)
                        # Fecha a aba de upload
                        botao_fechar_upload = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.ID, "btnUploadClose"))
                        )
                        botao_fechar_upload.click()
                        print(f"✓ [{index}] Aba de upload fechada.")

                        # Salva o novo documento
                        botao_salvar = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.ID, "saveNewDoc"))
                        )
                        botao_salvar.click()
                        print(f"✓ [{index}] Documento salvo com sucesso.")
                        time.sleep(2)

                except Exception as e:
                    print(f"⚠ [{index}] Erro ao verificar tabela de documentos: {str(e)}")

            except Exception as e:
                print(f"⚠ [{index}] Erro ao processar documento '{nome_documento}': {str(e)}")
                continue

        print("\n✓ Processamento de todos os documentos obrigatórios concluído com sucesso!")

        # Fecha o modal principal
        try:
            print("\nFechando o modal principal...")
            botao_fechar_modal = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='close' and @data-dismiss='modal']"))
            )
            botao_fechar_modal.click()
            print("✓ Modal principal fechado com sucesso.")
            time.sleep(2)  # Aguarda o modal fechar
        except Exception as e:
            print(f"⚠ Erro ao fechar o modal principal: {str(e)}")
            return

    except Exception as e:
        print(f"⚠ Erro ao processar documentos: {str(e)}")


# def salvar_proposta(driver):
    """
    Tenta salvar a proposta usando múltiplas estratégias para localizar e clicar nos botões.
    Retorna True se conseguir salvar com sucesso, False caso contrário.
    """
    try:
        # Lista de estratégias para encontrar o botão Salvar Proposta
        estrategias_salvar = [
            (By.XPATH, "//*[@id='btnSaveProposal']"),
            (By.ID, "btnSaveProposal"),
            (By.CSS_SELECTOR, "#btnSaveProposal"),
            (By.CLASS_NAME, "disableOnClick")
        ]

        # Tenta cada estratégia para clicar no botão Salvar
        for by, valor in estrategias_salvar:
            try:
                botao_salvar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, valor))
                )
                botao_salvar.click()
                print("✓ Botão Salvar Proposta encontrado e clicado")
                break
            except:
                continue

        time.sleep(2)  # Aguarda o diálogo de confirmação aparecer

        # Lista de estratégias para encontrar o botão Sim
        estrategias_confirmar = [
            (By.XPATH, "/html/body/div[5]/div/div/button[2]"),
            (By.CSS_SELECTOR, "button.btn.btn-primary[style*='margin-left: 10px']"),
            (By.XPATH, "//button[contains(@class, 'btn-primary') and text()='Sim']"),
            (By.XPATH, "//button[text()='Sim']")
        ]

        # Tenta cada estratégia para clicar no botão Sim
        for by, valor in estrategias_confirmar:
            try:
                botao_confirmar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, valor))
                )
                botao_confirmar.click()
                print("✓ Botão Sim encontrado e clicado")
                time.sleep(2)
                return True
            except:
                continue

        # Se chegou aqui, não conseguiu clicar em nenhum dos botões de confirmação
        print("⚠ Não foi possível encontrar o botão de confirmação")
        return False

    except Exception as e:
        print(f"⚠ Erro ao salvar proposta: {str(e)}")
        return False

def fechar_modal(driver, xpath_modal):
    """
    Fecha um modal com o botão fornecido pelo XPath.
    """
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_modal))
        )
        modal.click()
        print("✓ Modal fechado com sucesso.")
        time.sleep(2)  # Aguarda o modal fechar completamente
        return True
    except Exception as e:
        print(f"⚠ Erro ao fechar o modal: {str(e)}")
        return False


# def salvar_proposta(driver):
    """
    Tenta salvar a proposta usando múltiplas estratégias para localizar e clicar nos botões.
    Retorna True se conseguir salvar com sucesso, False caso contrário.
    """
    try:
        print("\nSalvando a proposta...")
        # Localiza e clica no botão de salvar proposta
        botao_salvar_proposta = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSaveProposal']"))
        )
        botao_salvar_proposta.click()
        time.sleep(2)

        # Tenta fechar o modal de erro se ele aparecer
        try:
            print("Verificando se há modal de erro...")
            botao_fechar_modal = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnClose']"))
            )
            print("Modal de erro encontrado, tentando fechar...")
            botao_fechar_modal.click()
            time.sleep(1)
        except:
            try:
                botao_fechar_modal = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/button"))
                )
                print("Modal de erro encontrado (xpath alternativo), tentando fechar...")
                botao_fechar_modal.click()
                time.sleep(1)
            except:
                print("Nenhum modal de erro encontrado ou já foi fechado.")

        # Aguarda e clica no botão "Sim" para confirmar o salvamento
        print("Procurando botão 'Sim' para confirmar o salvamento...")

        # Lista de estratégias para encontrar o botão Sim
        estrategias_confirmar = [
            (By.XPATH, "/html/body/div[5]/div/div/button[2]"),
            (By.CSS_SELECTOR, "button.btn.btn-primary[style*='margin-left: 10px']"),
            (By.XPATH, "//button[contains(@class, 'btn-primary') and text()='Sim']"),
            (By.XPATH, "//button[text()='Sim']")
        ]

        # Tenta cada estratégia para clicar no botão Sim
        for by, valor in estrategias_confirmar:
            try:
                print(f"Tentando localizar botão 'Sim' com: {by} - {valor}")
                botao_confirmar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, valor))
                )
                botao_confirmar.click()
                print("✓ Botão 'Sim' encontrado e clicado com sucesso!")
                time.sleep(2)
                return True
            except Exception as e:
                print(f"⚠ Tentativa com {by} - {valor} falhou: {str(e)}")
                continue

        print("⚠ Não foi possível localizar e clicar no botão 'Sim'.")
        return False

    except Exception as e:
        print(f"⚠ Erro ao salvar proposta: {str(e)}")
        return False
def salvar_proposta(driver):
    """
    Salva a proposta clicando no botão correspondente e lidando com possíveis interferências.
    """
    try:
        print("\nSalvando a proposta...")
        
        # Rola até o botão estar visível
        botao_salvar_proposta = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='btnSaveProposal']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_salvar_proposta)
        time.sleep(1)

        # Verifica se o botão está habilitado
        if not botao_salvar_proposta.is_enabled():
            print("⚠ O botão 'Salvar Proposta' está desabilitado. Verifique o estado da página.")
            return False

        # Verifica elementos sobrepostos
        is_obstructed = driver.execute_script(
            "return document.elementFromPoint(arguments[0], arguments[1]) !== arguments[2];",
            botao_salvar_proposta.location['x'],
            botao_salvar_proposta.location['y'],
            botao_salvar_proposta
        )
        if is_obstructed:
            print("⚠ Elemento sobreposto detectado. Tentando ajustar...")

        # Aguarda o desaparecimento de elementos bloqueadores
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element((By.CLASS_NAME, "modal-backdrop"))
        )
        print("✓ Elementos bloqueadores desapareceram.")

        # Tenta clicar no botão
        try:
            botao_salvar_proposta.click()
            print("✓ Botão 'Salvar Proposta' clicado com sucesso.")
        except Exception as e:
            print(f"⚠ Erro ao clicar no botão 'Salvar Proposta': {str(e)}")
            print("Tentando clicar usando JavaScript...")
            driver.execute_script("arguments[0].click();", botao_salvar_proposta)
            print("✓ Botão clicado com sucesso via JavaScript.")

        time.sleep(2)

        # Aguarda e clica no botão "Sim" para confirmar o salvamento
        print("Procurando botão 'Sim' para confirmar o salvamento...")
        estrategias_confirmar = [
            (By.XPATH, "/html/body/div[5]/div/div/button[2]"),
            (By.CSS_SELECTOR, "button.btn.btn-primary[style*='margin-left: 10px']"),
            (By.XPATH, "//button[contains(@class, 'btn-primary') and text()='Sim']"),
            (By.XPATH, "//button[text()='Sim']")
        ]

        for by, valor in estrategias_confirmar:
            try:
                botao_confirmar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, valor))
                )
                botao_confirmar.click()
                print("✓ Botão 'Sim' encontrado e clicado com sucesso.")
                time.sleep(2)
                return True
            except Exception as e:
                print(f"⚠ Tentativa com {by} - {valor} falhou: {str(e)}")
                continue

        print("⚠ Não foi possível localizar e clicar no botão 'Sim'.")
        return False

    except Exception as e:
        print(f"⚠ Erro ao salvar proposta: {str(e)}")
        return False
if __name__ == "__main__":
    wait_for_login(driver)
