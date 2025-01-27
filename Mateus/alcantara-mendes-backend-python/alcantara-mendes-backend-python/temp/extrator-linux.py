import shutil
import PyPDF2
import os
import zipfile
import subprocess
# import pyoo
import time


def extrair_arquivo(file, destination):
    try:
        if file.endswith('.zip'):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(destination)
    except Exception as e:
        print(f"Erro ao extrair {file}: {e}")

# extrair_arquivo('/home/abenathar/Sistemas/python/alcantara-mendes-chat-python/teste.zip', '/home/abenathar/Sistemas/python/alcantara-mendes-chat-python/zip/')




























#
#
# def extrair_zip_recursivo(path, destination):
#     extrair_arquivo(path, destination)
#     for nome_arquivo in os.listdir(destination):
#         caminho_completo = os.path.join(destination, nome_arquivo)
#         if nome_arquivo.endswith(('.zip', '.rar')) and os.path.isfile(caminho_completo):
#             nova_pasta_destino = os.path.join(destination, os.path.splitext(nome_arquivo)[0])
#             os.makedirs(nova_pasta_destino, exist_ok=True)
#             extrair_zip_recursivo(caminho_completo, nova_pasta_destino)
#             os.remove(caminho_completo)
#
#
# def extrair_arquivos_zip(origin, destination):
#     for arquivo in os.listdir(origin):
#         caminho_arquivo = os.path.join(origin, arquivo)
#         if arquivo.endswith(('.zip', '.rar')):
#             nova_pasta_destino = os.path.join(destination, os.path.splitext(arquivo)[0])
#             os.makedirs(nova_pasta_destino, exist_ok=True)
#             extrair_zip_recursivo(caminho_arquivo, nova_pasta_destino)
#             mover_arquivos_para_pasta_principal(nova_pasta_destino)
#             converter_e_excluir_arquivos(nova_pasta_destino)
#             juntar_pdfs(nova_pasta_destino)
#             extrair_arquivos_zip(nova_pasta_destino, nova_pasta_destino)
#
#
# def mover_arquivos_para_pasta_principal(destination):
#     for raiz, pastas, arquivos in os.walk(destination, topdown=False):
#         if raiz == destination:
#             continue
#         for nome in arquivos:
#             origem = os.path.join(raiz, nome)
#             destino = os.path.join(destination, nome)
#             if not os.path.exists(destino):
#                 shutil.move(origem, destino)
#             else:
#                 if os.path.getsize(origem) == os.path.getsize(destino):
#                     os.remove(origem)
#                 else:
#                     base, extensao = os.path.splitext(nome)
#                     contador = 1
#                     novo_nome = f"{base}_{contador}{extensao}"
#                     novo_destino = os.path.join(destination, novo_nome)
#                     while os.path.exists(novo_destino):
#                         contador += 1
#                         novo_nome = f"{base}_{contador}{extensao}"
#                         novo_destino = os.path.join(destination, novo_nome)
#                     shutil.move(origem, novo_destino)
#     for raiz, pastas, _ in os.walk(destination, topdown=False):
#         for nome in pastas:
#             caminho_pasta = os.path.join(raiz, nome)
#             if not os.listdir(caminho_pasta):
#                 os.rmdir(caminho_pasta)
#
#
# def ajustar_configuracoes_impressao(origem):
#     desktop = pyoo.Desktop('localhost', 2002)
#     doc = desktop.open_spreadsheet(origem)
#     for sheet in doc.sheets:
#         sheet.set_print_scale(1, 1)
#     doc.save()
#     doc.close()
#
#
# def converter_xlsm_para_pdf(origem, destino):
#     desktop = pyoo.Desktop('localhost', 2002)
#     doc = desktop.open_spreadsheet(origem)
#     doc.export_as_pdf(destino)
#     doc.close()
#
#
# def converter_para_pdf(origem, destino):
#     extensao = origem.lower().split('.')[-1]
#     desktop = pyoo.Desktop('localhost', 2002)
#     if extensao in ['xls', 'xlsx', 'xlsm']:
#         doc = desktop.open_spreadsheet(origem)
#         doc.export_as_pdf(destino)
#         doc.close()
#     elif extensao in ['doc', 'docx']:
#         doc = desktop.open_text_document(origem)
#         doc.save_as(destino, pyoo.FILTER_PDF)
#         doc.close()
#     else:
#         print("Formato de arquivo não suportado para conversão.")
#
#
# def remover_paginas_em_branco(pdf_origem, pdf_destino):
#     leitor = PyPDF2.PdfReader(pdf_origem)
#     escritor = PyPDF2.PdfWriter()
#     for pagina in leitor.pages:
#         if pagina.extract_text() and len(pagina.extract_text().strip()) > 50:
#             escritor.add_page(pagina)
#     with open(pdf_destino, 'wb') as f:
#         escritor.write(f)
#
#
# def converter_e_excluir_arquivos(pasta):
#     for arquivo in os.listdir(pasta):
#         caminho_completo = os.path.join(pasta, arquivo)
#         nome_arquivo, extensao = os.path.splitext(arquivo)
#         if extensao.lower() in ['.xls', '.xlsx', '.xlsm', '.doc', '.docx']:
#             novo_caminho_pdf = os.path.join(pasta, nome_arquivo + '.pdf')
#             converter_para_pdf(caminho_completo, novo_caminho_pdf)
#             time.sleep(1)  # Espera 1 segundo antes de tentar remover
#             try:
#                 os.remove(caminho_completo)
#             except PermissionError as e:
#                 print(f"Erro ao tentar remover o arquivo {caminho_completo}: {e}")
#
#
# def juntar_pdfs(pasta):
#     for subpasta in [d for d in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, d))]:
#         subpasta_caminho = os.path.join(pasta, subpasta)
#         arquivos_pdf = [arquivo for arquivo in os.listdir(subpasta_caminho) if arquivo.endswith('.pdf')]
#         escritor = PyPDF2.PdfWriter()
#         for arquivo_pdf in arquivos_pdf:
#             caminho_completo = os.path.join(subpasta_caminho, arquivo_pdf)
#             if os.path.getsize(caminho_completo) > 0:
#                 leitor = PyPDF2.PdfReader(caminho_completo)
#                 for pagina in leitor.pages:
#                     escritor.add_page(pagina)
#         if len(escritor.pages) > 0:
#             nome_arquivo_saida = f"{subpasta}.pdf"
#             with open(os.path.join(subpasta_caminho, nome_arquivo_saida), 'wb') as arquivo_saida:
#                 escritor.write(arquivo_saida)
#             for arquivo_pdf in arquivos_pdf:
#                 os.remove(os.path.join(subpasta_caminho, arquivo_pdf))
#
#
# if __name__ == "__main__":
#     pasta_origem = r'C:\Users\MSI Pulse\Documents\Chatpdf\Alcantara Mendes\RESUMIDOR\ARQUIVO'
#     pasta_destino = r'C:\Users\MSI Pulse\Documents\Chatpdf\Alcantara Mendes\RESUMIDOR\FEITO'
#     extrair_arquivos_zip(pasta_origem, pasta_destino)
#     juntar_pdfs(pasta_destino)
