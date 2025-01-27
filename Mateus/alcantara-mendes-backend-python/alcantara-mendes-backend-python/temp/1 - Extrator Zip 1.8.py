import shutil
import PyPDF2
import os
import zipfile
import subprocess
import win32com.client
import time

def extrair_arquivo(arquivo, pasta_destino):
    try:
        if arquivo.endswith('.zip'):
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(pasta_destino)
        elif arquivo.endswith('.rar'):
            comando = ['C:\\Program Files\\7-Zip\\7z.exe', 'x', arquivo, '-o' + pasta_destino]
            subprocess.run(comando, check=True)
    except Exception as e:
        print(f"Erro ao extrair {arquivo}: {e}")

def extrair_zip_recursivo(caminho_arquivo, pasta_destino):
    extrair_arquivo(caminho_arquivo, pasta_destino)
    for nome_arquivo in os.listdir(pasta_destino):
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        if nome_arquivo.endswith(('.zip', '.rar')) and os.path.isfile(caminho_completo):
            nova_pasta_destino = os.path.join(pasta_destino, os.path.splitext(nome_arquivo)[0])
            os.makedirs(nova_pasta_destino, exist_ok=True)
            extrair_zip_recursivo(caminho_completo, nova_pasta_destino)
            os.remove(caminho_completo)

def extrair_arquivos_zip(pasta_origem, pasta_destino):
    for arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        if arquivo.endswith(('.zip', '.rar')):
            nova_pasta_destino = os.path.join(pasta_destino, os.path.splitext(arquivo)[0])
            os.makedirs(nova_pasta_destino, exist_ok=True)
            extrair_zip_recursivo(caminho_arquivo, nova_pasta_destino)
            mover_arquivos_para_pasta_principal(nova_pasta_destino)
            converter_e_excluir_arquivos(nova_pasta_destino)
            juntar_pdfs(nova_pasta_destino)
            extrair_arquivos_zip(nova_pasta_destino, nova_pasta_destino)

def mover_arquivos_para_pasta_principal(pasta_destino):
    for raiz, pastas, arquivos in os.walk(pasta_destino, topdown=False):
        if raiz == pasta_destino:
            continue
        for nome in arquivos:
            origem = os.path.join(raiz, nome)
            destino = os.path.join(pasta_destino, nome)
            if not os.path.exists(destino):
                shutil.move(origem, destino)
            else:
                if os.path.getsize(origem) == os.path.getsize(destino):
                    os.remove(origem)
                else:
                    base, extensao = os.path.splitext(nome)
                    contador = 1
                    novo_nome = f"{base}_{contador}{extensao}"
                    novo_destino = os.path.join(pasta_destino, novo_nome)
                    while os.path.exists(novo_destino):
                        contador += 1
                        novo_nome = f"{base}_{contador}{extensao}"
                        novo_destino = os.path.join(pasta_destino, novo_nome)
                    shutil.move(origem, novo_destino)
    for raiz, pastas, _ in os.walk(pasta_destino, topdown=False):
        for nome in pastas:
            caminho_pasta = os.path.join(raiz, nome)
            if not os.listdir(caminho_pasta):
                os.rmdir(caminho_pasta)

def ajustar_configuracoes_impressao(origem):
    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    workbook = excel.Workbooks.Open(origem)
    for sheet in workbook.Sheets:
        sheet.PageSetup.Zoom = False
        sheet.PageSetup.FitToPagesWide = 1
        sheet.PageSetup.FitToPagesTall = 1
    workbook.Close(SaveChanges=True)
    excel.Quit()

def converter_xlsm_para_pdf(origem, destino):
    excel = None
    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(origem)
        workbook.ExportAsFixedFormat(0, destino)
    finally:
        if excel:
            workbook.Close(SaveChanges=False)
            excel.Quit()

def converter_para_pdf(origem, destino):
    extensao = origem.lower().split('.')[-1]
    if extensao in ['xls', 'xlsx', 'xlsm']:
        excel = win32com.client.DispatchEx("Excel.Application")
        try:
            workbook = excel.Workbooks.Open(origem)
            workbook.ExportAsFixedFormat(0, destino)
        finally:
            workbook.Close(SaveChanges=False)
            excel.Quit()
    elif extensao in ['doc', 'docx']:
        if origem.startswith('~$'):
            return  # Ignore temporary files
        word = win32com.client.Dispatch("Word.Application")
        try:
            doc = word.Documents.Open(origem)
            doc.SaveAs(destino, FileFormat=17)
        finally:
            doc.Close()
            word.Quit()
    else:
        print("Formato de arquivo não suportado para conversão.")

def remover_paginas_em_branco(pdf_origem, pdf_destino):
    leitor = PyPDF2.PdfReader(pdf_origem)
    escritor = PyPDF2.PdfWriter()
    for pagina in leitor.pages:
        if pagina.extract_text() and len(pagina.extract_text().strip()) > 50:
            escritor.add_page(pagina)
    with open(pdf_destino, 'wb') as f:
        escritor.write(f)

def converter_e_excluir_arquivos(pasta):
    for arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, arquivo)
        nome_arquivo, extensao = os.path.splitext(arquivo)
        if extensao.lower() in ['.xls', '.xlsx', '.xlsm', '.doc', '.docx']:
            novo_caminho_pdf = os.path.join(pasta, nome_arquivo + '.pdf')
            converter_para_pdf(caminho_completo, novo_caminho_pdf)
            time.sleep(1)  # Espera 1 segundo antes de tentar remover
            try:
                os.remove(caminho_completo)
            except PermissionError as e:
                print(f"Erro ao tentar remover o arquivo {caminho_completo}: {e}")

def juntar_pdfs(pasta):
    for subpasta in [d for d in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, d))]:
        subpasta_caminho = os.path.join(pasta, subpasta)
        arquivos_pdf = [arquivo for arquivo in os.listdir(subpasta_caminho) if arquivo.endswith('.pdf')]
        escritor = PyPDF2.PdfWriter()
        for arquivo_pdf in arquivos_pdf:
            caminho_completo = os.path.join(subpasta_caminho, arquivo_pdf)
            if os.path.getsize(caminho_completo) > 0:
                leitor = PyPDF2.PdfReader(caminho_completo)
                for pagina in leitor.pages:
                    escritor.add_page(pagina)
        if len(escritor.pages) > 0:
            nome_arquivo_saida = f"{subpasta}.pdf"
            with open(os.path.join(subpasta_caminho, nome_arquivo_saida), 'wb') as arquivo_saida:
                escritor.write(arquivo_saida)
            for arquivo_pdf in arquivos_pdf:
                os.remove(os.path.join(subpasta_caminho, arquivo_pdf))

if __name__ == "__main__":
    pasta_origem = r'C:\Users\MSI Pulse\Documents\Chatpdf\Alcantara Mendes\RESUMIDOR\ARQUIVO'
    pasta_destino = r'C:\Users\MSI Pulse\Documents\Chatpdf\Alcantara Mendes\RESUMIDOR\FEITO'
    extrair_arquivos_zip(pasta_origem, pasta_destino)
    juntar_pdfs(pasta_destino)
