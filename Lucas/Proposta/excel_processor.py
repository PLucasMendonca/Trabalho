import pandas as pd
import json
import os

def ler_excel(arquivo):
    """
    Lê o arquivo Excel e retorna um DataFrame
    """
    try:
        df = pd.read_excel(arquivo, engine='openpyxl')
        print("\nEstrutura do Excel:")
        print(f"Colunas encontradas: {df.columns.tolist()}")
        print(f"Número de linhas: {len(df)}")
        return df
    except Exception as e:
        print(f"Erro ao ler Excel: {str(e)}")
        return None

def processar_excel(df):
    """
    Processa o DataFrame do Excel
    """
    try:
        print("\nProcessando o Excel...")
        
        # Verifica as colunas esperadas
        colunas_esperadas = [
            'Item',
            'Descrição Detalhada do Objeto Ofertado',
            'Marca/Fabricante',
            'Modelo/Versão',
            'Quantidade solicitada',
            'Unidade Fornecimento',
            'Valor Total'
        ]
        
        # Verifica se todas as colunas necessárias existem
        colunas_encontradas = df.columns.tolist()
        if len(colunas_encontradas) != len(colunas_esperadas):
            print(f"Atenção: O número de colunas no Excel ({len(colunas_encontradas)}) não bate com o esperado ({len(colunas_esperadas)})!")
            print(f"Colunas encontradas: {colunas_encontradas}")
            print("As colunas não serão renomeadas automaticamente.")
        
        print("Estrutura do Excel processada com sucesso.")
        return df
        
    except Exception as e:
        print(f"Erro ao processar Excel: {str(e)}")
        return None

def salvar_excel(df, arquivo_original):
    """
    Salva o DataFrame processado em um novo arquivo Excel
    """
    try:
        # Gera o nome do arquivo processado
        diretorio = os.path.dirname(arquivo_original)
        nome_base = os.path.splitext(os.path.basename(arquivo_original))[0]
        
        # Remove múltiplos "_processado" se existirem
        nome_base = nome_base.replace('_processado', '')
        novo_arquivo = os.path.join(diretorio, f"{nome_base}_processado.xlsx")
        
        # Salva o arquivo
        df.to_excel(novo_arquivo, index=False, engine='openpyxl')
        print(f"Arquivo Excel salvo com sucesso: {novo_arquivo}")
        return novo_arquivo
        
    except Exception as e:
        print(f"Erro ao salvar Excel: {str(e)}")
        return None

def salvar_json(df, arquivo_excel):
    """
    Salva o DataFrame em formato JSON
    """
    try:
        # Converte o DataFrame para JSON
        dados_json = df.to_dict('records')
        
        # Gera o nome do arquivo JSON baseado no Excel
        arquivo_json = os.path.splitext(arquivo_excel)[0] + '.json'
        
        # Salva o arquivo JSON
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=4)
        
        print(f"Arquivo JSON gerado com sucesso: {arquivo_json}")
        return arquivo_json
        
    except Exception as e:
        print(f"Erro ao salvar JSON: {str(e)}")
        return None

def processar_arquivo_exportado(arquivo_excel):
    """
    Processa o arquivo Excel exportado
    """
    try:
        print("\nIniciando processamento do arquivo...")
        
        # Lê o Excel
        df = ler_excel(arquivo_excel)
        if df is None:
            return None
            
        # Processa o Excel
        df_processado = processar_excel(df)
        if df_processado is None:
            return None
            
        # Salva o Excel processado
        novo_excel = salvar_excel(df_processado, arquivo_excel)
        if novo_excel is None:
            return None
            
        # Salva o JSON
        arquivo_json = salvar_json(df_processado, novo_excel)
        if arquivo_json is None:
            return None
            
        return {
            'excel': novo_excel,
            'json': arquivo_json
        }
        
    except Exception as e:
        print(f"Erro ao processar arquivo: {str(e)}")
        return None
