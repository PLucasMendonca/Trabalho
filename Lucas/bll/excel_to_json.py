import pandas as pd
import json
from datetime import datetime
import os
import glob

def main():
    # Obtém o diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Procura por arquivos Excel (.xlsx) na pasta atual
    excel_files = glob.glob(os.path.join(current_dir, "*.xlsx"))
    
    if not excel_files:
        print("Nenhum arquivo Excel (.xlsx) encontrado na pasta.")
        return
    
    # Pega o arquivo Excel mais recente
    excel_file = max(excel_files, key=os.path.getctime)
    print(f"\nArquivo Excel encontrado: {os.path.basename(excel_file)}")

    try:
        print("\nConvertendo Excel para JSON...")
        
        # Lê o arquivo Excel
        print("Lendo arquivo Excel...")
        df = pd.read_excel(excel_file)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Extrai o número do processo do nome do arquivo
        process_number = os.path.splitext(os.path.basename(excel_file))[0]
        
        # Lista para armazenar os dados
        data = []
        
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
            data.append(row_dict)
        
        # Cria o nome do arquivo JSON
        json_filename = os.path.join(current_dir, f"proposta_{process_number}.json")
        
        # Salva o JSON
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✓ Arquivo JSON salvo como: {json_filename}")
        
        # Remove o arquivo Excel original após a conversão
        os.remove(excel_file)
        print(f"✓ Arquivo Excel original removido: {os.path.basename(excel_file)}")
        
    except Exception as e:
        print(f"Erro ao converter para JSON: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
