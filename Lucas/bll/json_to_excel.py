import pandas as pd
import json
import os
import glob

def main():
    # Obtém o diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Procura por arquivos JSON na pasta atual
    json_files = glob.glob(os.path.join(current_dir, "proposta_*.json"))
    
    if not json_files:
        print("Nenhum arquivo JSON de proposta encontrado na pasta.")
        return
    
    # Pega o arquivo JSON mais recente
    json_file = max(json_files, key=os.path.getctime)
    print(f"\nArquivo JSON encontrado: {os.path.basename(json_file)}")

    try:
        print("\nConvertendo JSON para Excel...")
        
        # Lê o arquivo JSON
        print("Lendo arquivo JSON...")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Converte a lista de dicionários para DataFrame
        df = pd.DataFrame(data)
        
        print("Estrutura do arquivo:")
        print(f"Colunas: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        
        # Extrai o número do processo do nome do arquivo JSON
        process_number = os.path.basename(json_file).replace('proposta_', '').replace('.json', '')
        
        # Cria o nome do arquivo Excel
        excel_filename = os.path.join(current_dir, f"proposta_modificada_{process_number}.xlsx")
        
        # Salva como Excel
        df.to_excel(excel_filename, index=False)
        print(f"✓ Arquivo Excel salvo como: {excel_filename}")
        
    except Exception as e:
        print(f"Erro ao converter para Excel: {str(e)}")
        print("Detalhes do erro:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
