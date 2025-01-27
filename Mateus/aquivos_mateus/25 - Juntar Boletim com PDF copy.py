import os
from PyPDF2 import PdfReader, PdfWriter

def combinar_pdfs(pdf1, pdf2, destino):
    print(f"Combinando {pdf1} e {pdf2} em {destino}")
    escritor = PdfWriter()
    leitor1 = PdfReader(pdf1)
    for pagina in leitor1.pages:
        escritor.add_page(pagina)
    leitor2 = PdfReader(pdf2)
    for pagina in leitor2.pages:
        escritor.add_page(pagina)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'wb') as arquivo_saida:
        escritor.write(arquivo_saida)

# OPÇÃO QUANDO TEM PASTA
def achar_pdf_correspondente(pasta_indexar, nome_arquivo):
    for raiz, dirs, arquivos in os.walk(pasta_indexar):
        if nome_arquivo in dirs:
            arquivo_pdf = [f for f in os.listdir(os.path.join(raiz, nome_arquivo)) if f.endswith('.pdf')]
            if arquivo_pdf:
                return os.path.join(raiz, nome_arquivo, arquivo_pdf[0])
    return None

# OPÇÃO QUANDO NÃO TEM PASTA
# def achar_pdf_correspondente(pasta_indexar, nome_arquivo):
#     # Busca por um arquivo que tenha o mesmo nome, acrescido da extensão .pdf
#     possivel_arquivo = f"{nome_arquivo}.pdf"
#     # Lista todos os arquivos na pasta_indexar
#     for arquivo in os.listdir(pasta_indexar):
#         if arquivo == possivel_arquivo:
#             return os.path.join(pasta_indexar, arquivo)
#     return None


def processar_subpasta(pasta_origem, pasta_indexar, pasta_destino):
    for raiz, dirs, arquivos in os.walk(pasta_origem):
        for nome in dirs:
            subpasta_origem = os.path.join(raiz, nome)
            subpasta_destino = os.path.join(pasta_destino, os.path.relpath(subpasta_origem, pasta_origem))
            arquivos_pdf = [f for f in os.listdir(subpasta_origem) if f.endswith('.pdf')]
            
            for pdf in arquivos_pdf:
                pdf_origem = os.path.join(subpasta_origem, pdf)
                numero_pdf = os.path.splitext(pdf)[0]
                
                pdf_indexar = achar_pdf_correspondente(pasta_indexar, numero_pdf)
                if pdf_indexar:
                    arquivo_destino = os.path.join(subpasta_destino, pdf)
                    combinar_pdfs(pdf_origem, pdf_indexar, arquivo_destino)
                else:
                    print(f"PDF correspondente para {pdf_origem} não encontrado.")

if __name__ == "__main__":
    pasta_boletim = r'C:\Users\MSI Pulse\Documents\Chatpdf\Effecti\Boletim Resumo - Envio'
    pasta_indexar = r'C:\Users\MSI Pulse\Documents\Chatpdf\Effecti\Indexar'
    pasta_envio = r'C:\Users\MSI Pulse\Documents\Chatpdf\Effecti\Boletim Resumo - Envio'
    processar_subpasta(pasta_boletim, pasta_indexar, pasta_envio)
