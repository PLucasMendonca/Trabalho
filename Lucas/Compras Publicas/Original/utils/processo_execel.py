def process_excel(excel_file):
    """
    Processa o arquivo Excel, preenchendo os valores conforme os itens cadastrados,
    priorizando os menores valores.
    """
    try:
        # Extrai o número do processo do nome do arquivo
        process_number = os.path.splitext(os.path.basename(excel_file))[0]
        
        # Cria o novo arquivo Excel com as modificações
        modified_file = create_modified_excel(excel_file, process_number)
        
        if modified_file:
            print("✓ Excel processado com sucesso!")
            return modified_file
        else:
            print("⚠ Erro ao processar Excel")
            return None
            
    except Exception as e:
        print(f"Erro ao processar Excel: {str(e)}")
        return None