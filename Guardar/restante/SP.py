import os
import time
import datetime
import glob
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from src.util.mascaras import remover_mascara_cnpj
from src.modules.bitrix._anexar_arquivos import BitrixUploader

class Sintegra_SP:
    def __init__(self, url_uf, cnpj):
        self.url_uf = "https://www.cadesp.fazenda.sp.gov.br/(S(eewwynf23kaii5ydesfux1es))/Pages/Cadastro/Consultas/ConsultaPublica/ConsultaPublica.aspx"
        self.cnpj = cnpj
        self.driver = None
        self.root = None
        self.captcha_entry = None
        self.download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.certidoes_dir = os.path.join(self.download_dir, 'Certidoes')

        # Garante que a pasta Certidoes existe
        if not os.path.exists(self.certidoes_dir):
            os.makedirs(self.certidoes_dir)

    def configurar_chrome(self):
        """Configura o Chrome com as opções necessárias"""
        try:
            chrome_options = Options()
            
            # Configura o diretório de download
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            
        except Exception as e:
            print(f"Erro ao configurar o Chrome: {str(e)}")
            raise

    def continuar_automacao_sp(self, url_uf, cnpj):
        """Executa a automação para SP"""
        try:
            # Configura e abre o Chrome
            self.configurar_chrome()

            # Acessa a página
            print("Acessando a página do Sintegra SP...")
            self.driver.get(self.url_uf)
            time.sleep(3)

            # Passo 1: Selecionar a opção "CNPJ" no <select>
            print("Selecionando a opção CNPJ...")
            dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_tipoFiltroDropDownList"))
            )
            select = Select(dropdown)
            select.select_by_visible_text("CNPJ")

            # Cria janela para CAPTCHA
            self.root = tk.Tk()
            self.root.title("Insira o CAPTCHA")
            self.root.attributes('-topmost', True)

            # Label e entrada para o CAPTCHA
            tk.Label(self.root, text="Insira o CAPTCHA:").pack(pady=10)
            self.captcha_entry = tk.Entry(self.root)
            self.captcha_entry.pack(pady=10)

            # Botão para continuar a automação
            continuar_button = tk.Button(
                self.root, text="Continuar Automação", 
                command=lambda: self.iniciar_automacao(cnpj))
            continuar_button.pack(pady=20)

            self.root.mainloop()

        except Exception as e:
            print(f"Erro durante a automação do Sintegra SP: {str(e)}")
            if self.driver:
                self.driver.quit()
            if self.root:
                self.root.destroy()
            return False

    def iniciar_automacao(self, cnpj):
        """Inicia a automação após inserir o CAPTCHA"""
        try:
            captcha = self.captcha_entry.get()
            cnpj = remover_mascara_cnpj(cnpj)

            # Passo 2: Preencher o campo de CNPJ
            print("Preenchendo o CNPJ...")
            campo_cnpj = self.wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_valorFiltroTextBox"))
            )
            campo_cnpj.click()
            campo_cnpj.clear()
            campo_cnpj.send_keys(cnpj)

            # Passo 3: Preencher o campo de captcha
            print("Preenchendo o captcha...")
            campo_captcha = self.wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_imagemDinamicaTextBox"))
            )
            campo_captcha.click()
            campo_captcha.clear()
            campo_captcha.send_keys(captcha)

            # Passo 4: Clicar no botão "Consultar"
            print("Clicando no botão 'Consultar'...")
            botao_consultar = self.wait.until(
                EC.element_to_be_clickable((By.ID, "ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_consultaPublicaButton"))
            )
            botao_consultar.click()
            print("Botão 'Consultar' clicado com sucesso!")

            # Aguarda para observar o comportamento
            time.sleep(5)

            # Executa o script de impressão
            self.driver.execute_script("window.print();")

            # Verifica o download
            self.verificar_download(cnpj)

        except NoSuchElementException:
            messagebox.showerror("Erro", "Erro ao emitir certidão. Verifique os dados.")
            if self.root:
                self.root.destroy()
            if self.driver:
                self.driver.quit()

    def verificar_download(self, cnpj):
        """Verifica se o download foi concluído e move o arquivo"""
        try:
            # Define os caminhos
            padrao_arquivo = os.path.join(self.download_dir, "Consulta Pública ao Cadesp.pdf")
            nova_data = datetime.datetime.now() + datetime.timedelta(days=30)
            data_formatada = nova_data.strftime("%d.%m.%Y")
            novo_nome = f"DIF {data_formatada}.pdf"
            novo_caminho = os.path.join(self.certidoes_dir, novo_nome)

            def checar_arquivo():
                arquivo_encontrado = glob.glob(padrao_arquivo)
                if arquivo_encontrado:
                    arquivo_download = arquivo_encontrado[0]
                    if not os.path.exists(arquivo_download + '.crdownload'):
                        if os.path.exists(novo_caminho):
                            os.remove(novo_caminho)
                        time.sleep(2)
                        try:
                            print(f"Tentando mover {arquivo_download} para {novo_caminho}")
                            os.rename(arquivo_download, novo_caminho)
                            print(f"Arquivo movido para: {novo_caminho}")

                            # Upload para o Bitrix
                            try:
                                bitrix = BitrixUploader()
                                bitrix.set_cnpj_atual(self.cnpj)
                                card_id = bitrix.get_card_id_by_cnpj(self.cnpj)
                                
                                if card_id:
                                    bitrix.carregar_arquivo_para_cartao(card_id, novo_caminho, "ANEXO_SINTEGRA")
                                    print("Arquivo enviado para o Bitrix com sucesso!")
                                    messagebox.showinfo("Sucesso", "Certidão do Sintegra SP foi baixada e enviada para o Bitrix com sucesso!")
                                else:
                                    print("Cartão não encontrado no Bitrix para este CNPJ")
                                    messagebox.showerror("Erro", "Cartão não encontrado no Bitrix para este CNPJ")
                            except Exception as e:
                                print(f"Erro ao enviar arquivo para o Bitrix: {e}")
                                messagebox.showerror("Erro", f"Erro ao enviar arquivo para o Bitrix: {e}")

                        except Exception as e:
                            messagebox.showerror("Erro ao Mover Arquivo", f"Ocorreu um erro: {e}")
                            print(f"Erro ao mover o arquivo: {e}")

                        if self.root:
                            self.root.destroy()
                        if self.driver:
                            self.driver.quit()
                    else:
                        self.root.after(2000, checar_arquivo)

            checar_arquivo()

        except Exception as e:
            print(f"Erro ao verificar download: {str(e)}")
            if self.root:
                self.root.destroy()
            if self.driver:
                self.driver.quit()