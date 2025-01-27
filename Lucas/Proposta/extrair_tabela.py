import pdfplumber
import pandas as pd

def verificar_tabela(df):
    """
    Função para verificar se a tabela contém uma coluna 'ID' e
    se há alguma linha onde o 'ID' é igual a 123.
    """
    if 'ID' in df.columns:
        if (df['ID'] == '123').any():
            return True
    return False

# Caminho para o arquivo PDF
caminho_pdf = "C:\Users\Windows 11\Desktop\Proposta\pdf\proposta_447338.pdf"

# Abrir o arquivo PDF
with pdfplumber.open(caminho_pdf) as pdf:
    # Iterar por todas as páginas do PDF
    for numero_pagina, pagina in enumerate(pdf.pages, start=1):
        # Extrair tabelas da página atual
        tabelas = pagina.extract_tables()
        # Iterar por cada tabela extraída
        for numero_tabela, tabela in enumerate(tabelas, start=1):
            # Converter a tabela para um DataFrame do pandas
            df = pd.DataFrame(tabela[1:], columns=tabela[0])
            # Verificar se a tabela atende aos critérios desejados
            if verificar_tabela(df):
                print(f"Tabela desejada encontrada na página {numero_pagina}, tabela {numero_tabela}")
                # Salvar a tabela em um arquivo CSV
                df.to_csv(f"tabela_desejada_pagina_{numero_pagina}_tabela_{numero_tabela}.csv", index=False)
                # Se desejar parar após encontrar a primeira tabela correspondente, descomente a linha abaixo
                # break
