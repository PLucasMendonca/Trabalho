import pandas as pd
import json
import os

def verificar_json_pregao(numero_pregao, uasg=None, orgao=None):
    """
    Verifica se existe um pregão correspondente nos arquivos JSON e retorna suas informações
    """
    json_dir = os.path.join(os.path.dirname(__file__), 'json')
    if not os.path.exists(json_dir):
        return None
    
    for json_file in os.listdir(json_dir):
        if not json_file.endswith('.json'):
            continue
            
        try:
            with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Verifica no formato ComprasNet
            if 'contratacao' in data:
                if data['id_compra'] == numero_pregao or data['contratacao']['resultado'][0]['numeroCompra'] == numero_pregao:
                    if 'itens' in data and 'resultado' in data['itens']:
                        return data['itens']['resultado']
                        
            # Verifica no formato PNCP
            elif 'licitacao' in data:
                pregao_match = (data['licitacao']['numeroCompra'] == numero_pregao or 
                              data['licitacao']['numeroControlePNCP'].split('-')[-1] == numero_pregao)
                
                if pregao_match:
                    if 'itens' in data:
                        return data['itens']
                    
        except Exception as e:
            print(f"Erro ao processar arquivo JSON {json_file}: {str(e)}")
            continue
    
    return None

def atualizar_valores_excel(df, itens_json):
    """
    Atualiza o DataFrame com os valores encontrados no JSON
    """
    if not itens_json:
        return df
        
    # Cria uma cópia do DataFrame para não modificar o original
    df_updated = df.copy()
    
    # Para cada item no JSON
    for item in itens_json:
        valor_total = None
        valor_unitario = None
        
        # Tenta obter os valores do formato ComprasNet
        if isinstance(item, dict):
            if 'valorTotal' in item:
                valor_total = item.get('valorTotal')
            elif 'valorTotalEstimado' in item:
                valor_total = item.get('valorTotalEstimado')
                
            if 'valorUnitario' in item:
                valor_unitario = item.get('valorUnitario')
            elif 'valorUnitarioEstimado' in item:
                valor_unitario = item.get('valorUnitarioEstimado')
        
        # Se encontrou valores, atualiza o DataFrame
        if valor_total is not None or valor_unitario is not None:
            # Tenta encontrar o item correspondente no DataFrame
            # Isso pode precisar ser ajustado dependendo da estrutura do seu Excel
            item_desc = item.get('descricao', '').lower()
            
            for idx, row in df_updated.iterrows():
                # Verifica se a descrição do item do Excel corresponde ao item do JSON
                if 'Descrição' in row and str(row['Descrição']).lower() in item_desc or item_desc in str(row['Descrição']).lower():
                    if valor_unitario is not None:
                        df_updated.at[idx, 'Valor Unitário'] = valor_unitario
                    if valor_total is not None:
                        df_updated.at[idx, 'Valor Total'] = valor_total
    
    return df_updated

def processar_arquivo_exportado(arquivo_excel, numero_pregao=None, uasg=None, orgao=None):
    """
    Processa o arquivo Excel exportado do ComprasNet e retorna os dados processados
    """
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(arquivo_excel)
        
        # Se tiver número do pregão, verifica nos JSONs
        if numero_pregao:
            itens_json = verificar_json_pregao(numero_pregao, uasg, orgao)
            if itens_json:
                df = atualizar_valores_excel(df, itens_json)
        
        # Gera o nome do arquivo JSON baseado no nome do Excel
        base_name = os.path.splitext(arquivo_excel)[0]
        json_file = f"{base_name}_processado.json"
        excel_file = f"{base_name}_processado.xlsx"
        
        # Salva o DataFrame processado em Excel
        df.to_excel(excel_file, index=False)
        
        # Converte para JSON
        dados_json = df.to_json(orient='records', force_ascii=False)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json.loads(dados_json), f, ensure_ascii=False, indent=4)
        
        return {
            'excel': excel_file,
            'json': json_file
        }
        
    except Exception as e:
        print(f"Erro ao processar arquivo Excel: {str(e)}")
        return None
