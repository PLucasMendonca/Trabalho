import pdfplumber
import pandas as pd
import os
from typing import List, Set, Optional

def palavras_chave_padrao() -> Set[str]:
    """
    Retorna um conjunto de palavras-chave comumente usadas em tabelas de valores.
    
    Returns:
        Set[str]: Conjunto de palavras-chave normalizadas (minúsculas)
    """
    return {
        'valor mínimo', 'valor máximo', 'valor unitário', 'valor total',
        'valor estimado', 'preço', 'custo', 'quantidade', 'qtd', 'qtde',
        'valor mensal', 'valor anual', 'total', 'subtotal', 'preço unitário',
        'valor global', 'valor limite'
    }

def verificar_tabela(df: pd.DataFrame, palavras_chave: Optional[Set[str]] = None) -> bool:
    """
    Verifica se a tabela contém alguma das palavras-chave especificadas.

    Args:
        df (pd.DataFrame): DataFrame a ser verificado
        palavras_chave (Set[str], optional): Conjunto de palavras-chave para buscar.
            Se None, usa o conjunto padrão.

    Returns:
        bool: True se encontrou alguma palavra-chave, False caso contrário
    """
    if palavras_chave is None:
        palavras_chave = palavras_chave_padrao()
    
    try:
        # Converte todas as colunas para string e normaliza
        colunas_normalizadas = [str(col).lower().strip() for col in df.columns]
        
        # Verifica nas colunas
        for coluna in colunas_normalizadas:
            for palavra in palavras_chave:
                if palavra in coluna:
                    return True
        
        # Verifica no conteúdo da tabela
        for coluna in df.columns:
            # Converte a coluna para string e procura as palavras-chave
            valores = df[coluna].fillna('').astype(str)
            for valor in valores:
                valor_lower = valor.lower().strip()
                if any(palavra in valor_lower for palavra in palavras_chave):
                    return True
                
        return False
    except Exception as e:
        print(f"Erro ao verificar tabela: {str(e)}")
        return False

def extrair_tabelas_pdf(caminho_pdf: str, palavras_chave: Optional[Set[str]] = None, salvar_csv: bool = True) -> List[pd.DataFrame]:
    """
    Extrai tabelas de um arquivo PDF que contenham as palavras-chave especificadas.

    Args:
        caminho_pdf (str): Caminho para o arquivo PDF
        palavras_chave (Set[str], optional): Conjunto de palavras-chave para buscar.
            Se None, usa o conjunto padrão.
        salvar_csv (bool): Se True, salva as tabelas encontradas em arquivos CSV

    Returns:
        List[pd.DataFrame]: Lista com as tabelas encontradas
    """
    tabelas_encontradas = []
    
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(caminho_pdf):
            raise FileNotFoundError(f"O arquivo {caminho_pdf} não foi encontrado")

        with pdfplumber.open(caminho_pdf) as pdf:
            for numero_pagina, pagina in enumerate(pdf.pages, start=1):
                try:
                    tabelas = pagina.extract_tables()
                    for numero_tabela, tabela in enumerate(tabelas, start=1):
                        if not tabela or not tabela[0]:  # Verifica se a tabela está vazia
                            continue
                            
                        df = pd.DataFrame(tabela[1:], columns=tabela[0])
                        
                        if verificar_tabela(df, palavras_chave):
                            print(f"Tabela encontrada na página {numero_pagina}, tabela {numero_tabela}")
                            tabelas_encontradas.append(df)
                            
                            if salvar_csv:
                                nome_arquivo = f"tabela_valores_pagina_{numero_pagina}_tabela_{numero_tabela}.csv"
                                df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
                                print(f"Tabela salva em: {nome_arquivo}")
                                
                except Exception as e:
                    print(f"Erro ao processar página {numero_pagina}: {str(e)}")
                    continue
                    
    except Exception as e:
        print(f"Erro ao processar o PDF: {str(e)}")
        
    return tabelas_encontradas

if __name__ == "__main__":
    # Caminho para o arquivo PDF
    caminho_pdf = r"C:\Users\Windows 11\Documents\Repositórios\Lucas\Proposta\pdf\448406.pdf"
    
    # Você pode especificar suas próprias palavras-chave ou usar as padrão
    palavras_chave_customizadas = {
        'valor unitário', 'valor total', 'preço', 'quantidade'
    }
    
    try:
        # Usando palavras-chave customizadas
        tabelas = extrair_tabelas_pdf(
            caminho_pdf=caminho_pdf,
            palavras_chave=palavras_chave_customizadas,
            salvar_csv=True
        )
        print(f"Total de tabelas encontradas: {len(tabelas)}")
        
        # Para cada tabela encontrada, mostra um resumo
        for i, df in enumerate(tabelas, 1):
            print(f"\nTabela {i}:")
            print("Colunas encontradas:", ", ".join(df.columns))
            print("Dimensões:", df.shape)
            
    except Exception as e:
        print(f"Erro ao executar o programa: {str(e)}")
