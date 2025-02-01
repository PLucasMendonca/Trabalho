class DownloadProcessor:
    def __init__(self):
        pass
    
    def iniciar_processo(self):
        print("Exportação iniciada!")
        
    def aguardar_download():
        # Aguarda o download do arquivo
        print("Aguardando download do arquivo...")
        download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Procura por arquivos que começam com 'exportacao_' e terminam com '.xlsx'
            files = [f for f in os.listdir(download_dir) if f.startswith('exportação_') and f.endswith('.xlsx')]
            if files:
                # Pega o arquivo mais recente
                newest_file = max([os.path.join(download_dir, f) for f in files], key=os.path.getctime)
                print(f"Arquivo exportado encontrado: {newest_file}")
                time.sleep(2)  # Garante que o arquivo terminou de ser baixado)
                
                # Após encontrar o arquivo, inicia o processamento
                print("\nIniciando processamento do arquivo...")
                from excel_processor import processar_arquivo_exportado
                
                resultado = self.processar_arquivo_exportado(newest_file)
                if resultado and isinstance(resultado, dict):
                    print("\nArquivos gerados:")
                    print(f"Excel processado: {resultado.get('excel', 'Não gerado')}")
                    print(f"JSON gerado: {resultado.get('json', 'Não gerado')}")
                    
                    # Remove o arquivo Excel original após processamento
                    try:
                        os.remove(newest_file)
                        print(f"\nArquivo Excel original removido: {newest_file}")
                    except Exception as e:
                        print(f"Aviso: Não foi possível remover o arquivo original: {str(e)}")
                    
                    # Gera o documento Word
                    from word_processor import criar_tabela_word
                    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'word', 'MUNDIAL PROPOSTA 447338.docx')
                    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proposta_final.docx')
                    
                    # Tenta com diferentes variações do marcador
                    marcadores = [
                        "{{TABELA_AQUI}}",
                        "{{tabela_aqui}}",
                        "{TABELA_AQUI}",
                        "{tabela_aqui}",
                        "TABELA_AQUI",
                        "tabela_aqui"
                    ]
                    
                    documento_word = None
                    for marcador in marcadores:
                        print(f"\nTentando com marcador: {marcador}")
                        documento_word = criar_tabela_word(
                            json_file=resultado['json'],
                            template_file=template_path,
                            marcador_tabela=marcador,
                            output_file=output_path
                        )
                        if documento_word:
                            print(f"Documento Word gerado com sucesso usando marcador: {marcador}")
                            break
                    
                    if documento_word:
                        print(f"Documento Word gerado: {documento_word}")
                    else:
                        print("Não foi possível gerar o documento Word com nenhum dos marcadores tentados")
                    
                    print("\nProcessamento concluído com sucesso!")
                    return {
                        'excel': resultado['excel'],
                        'json': resultado['json'],
                        'word': documento_word
                    }
                else:
                    print("Erro: Não foi possível processar o arquivo Excel")
                
            time.sleep(1)
        
        print("Tempo limite de download excedido!")

