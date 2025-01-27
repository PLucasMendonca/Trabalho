import os
import time
import datetime
import pyautogui
import webbrowser
from src.util.mascaras import remover_mascara_cnpj
from src.modules.bitrix._anexar_arquivos import BitrixUploader

class Sintegra_MG:
    def __init__(self, url_uf, cnpj):
        self.url_uf = url_uf
        self.cnpj = cnpj
        self.download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.certidoes_dir = os.path.join(self.download_dir, 'Certidoes')
        self.images_dir = os.path.join(os.path.dirname(__file__), 'images_mg')

        # Garante que a pasta Certidoes existe
        if not os.path.exists(self.certidoes_dir):
            os.makedirs(self.certidoes_dir)

        # Configura o PyAutoGUI para ser mais seguro
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 1

    def clicar_imagem(self, imagem, timeout=10):
        """Tenta clicar em uma imagem com timeout"""
        inicio = time.time()
        caminho_imagem = os.path.join(self.images_dir, imagem)
        
        # Verifica se a imagem existe
        if not os.path.exists(caminho_imagem):
            print(f"Imagem não encontrada: {caminho_imagem}")
            return False

        while time.time() - inicio < timeout:
            try:
                # Tenta localizar a imagem na tela
                localizacao = pyautogui.locateOnScreen(caminho_imagem, grayscale=True)
                if localizacao:
                    centro = pyautogui.center(localizacao)
                    pyautogui.click(centro)
                    return True
            except Exception as e:
                print(f"Tentando localizar imagem {imagem}...")
                time.sleep(1)
        return False

    def continuar_automacao_mg(self, url_uf, cnpj):
        """Executa a automação para MG usando pyautogui"""
        try:
            # Limpa a pasta Certidoes
            print("Pasta certidões limpa com sucesso!")

            # Abre o Chrome e acessa a URL
            print("Abrindo o navegador...")
            webbrowser.open(url_uf)
            time.sleep(5)  # Aguarda a página carregar

            # Clica no tipo de arquivo
            print("Selecionando tipo de arquivo...")
            if not self.clicar_imagem('tipo_arquivo.png'):
                print("Não foi possível encontrar o campo tipo de arquivo")
                return False

            # Clica em CNPJ
            print("Selecionando CNPJ...")
            if not self.clicar_imagem('cnpj.png'):
                print("Não foi possível encontrar o campo CNPJ")
                return False

            # Clica em identificação
            print("Clicando em identificação...")
            if not self.clicar_imagem('identificacao.png'):
                print("Não foi possível encontrar o campo identificação")
                return False

            # Digita o CNPJ
            print("Digitando CNPJ...")
            cnpj_limpo = remover_mascara_cnpj(cnpj)
            pyautogui.write(cnpj_limpo)
            time.sleep(1)

            # Clica em confirmar
            print("Clicando em confirmar...")
            if not self.clicar_imagem('confirmar.png'):
                print("Não foi possível encontrar o botão confirmar")
                return False
            time.sleep(2)

            # Clica em confirmar novamente
            print("Confirmando novamente...")
            if not self.clicar_imagem('confirmar_2.png'):
                print("Não foi possível encontrar o segundo botão confirmar")
                return False
            time.sleep(2)

            # Clica em imprimir
            print("Clicando em imprimir...")
            if not self.clicar_imagem('imprimir.png'):
                print("Não foi possível encontrar o botão imprimir")
                return False
            time.sleep(3)

            # Pressiona Ctrl + P
            print("Abrindo diálogo de impressão...")
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(3)

            # Gera o nome do arquivo com data de validade
            nova_data = datetime.datetime.now() + datetime.timedelta(days=30)
            nome_arquivo = f"SINTEGRA_MG_{nova_data.strftime('%d-%m-%Y')}.pdf"
            caminho_arquivo_downloads = os.path.join(self.download_dir, nome_arquivo)

            # Digita o nome do arquivo caractere por caractere
            print(f"Digitando nome do arquivo: {nome_arquivo}")
            for char in nome_arquivo:
                pyautogui.write(char)
                time.sleep(0.1)
            time.sleep(1)

            # Pressiona Enter para salvar
            pyautogui.press('enter')
            time.sleep(3)

            # Aguarda o download e verifica
            print("Aguardando download...")
            tempo_espera = 30
            intervalo = 1
            tempo_decorrido = 0

            while tempo_decorrido < tempo_espera:
                if os.path.exists(caminho_arquivo_downloads):
                    print(f"Arquivo encontrado: {nome_arquivo}")
                    
                    # Move o arquivo para a pasta Certidoes
                    novo_caminho = os.path.join(self.certidoes_dir, nome_arquivo)
                    if os.path.exists(novo_caminho):
                        os.remove(novo_caminho)
                    
                    os.rename(caminho_arquivo_downloads, novo_caminho)
                    print(f"Arquivo movido para: {novo_caminho}")

                    # Upload para o Bitrix
                    try:
                        bitrix = BitrixUploader()
                        bitrix.set_cnpj_atual(self.cnpj)
                        card_id = bitrix.get_card_id_by_cnpj(self.cnpj)
                        
                        if card_id:
                            bitrix.carregar_arquivo_para_cartao(card_id, novo_caminho, "ANEXO_SINTEGRA")
                            print("Arquivo enviado para o Bitrix com sucesso!")
                            return True
                        else:
                            print("Cartão não encontrado no Bitrix para este CNPJ")
                            return False
                            
                    except Exception as e:
                        print(f"Erro ao enviar arquivo para o Bitrix: {e}")
                        return False

                time.sleep(intervalo)
                tempo_decorrido += intervalo

            print("Tempo de espera excedido para o download do arquivo")
            return False

        except Exception as e:
            print(f"Erro durante a automação do Sintegra MG: {str(e)}")
            return False