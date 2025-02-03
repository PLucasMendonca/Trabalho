from main import FormularioBase

def processar_arquivo_excel():
    formulario = FormularioBase("", "")
    arquivo_excel = formulario.encontrar_ultimo_excel()
    if arquivo_excel:
        print(f"Arquivo Excel encontrado: {arquivo_excel}")
        
        # Processa o Excel
        arquivo_processado = formulario.processar_excel(arquivo_excel)
        if arquivo_processado:
            # Converte para JSON
            arquivo_json = formulario.excel_para_json(arquivo_processado)
            if arquivo_json:
                print(f"Conversão para JSON concluída: {arquivo_json}")
                # Exclui os arquivos Excel temporários
                formulario.excluir_excel_temporario(arquivo_excel)
                formulario.excluir_excel_temporario(arquivo_processado)
                print("\nProcesso finalizado com sucesso!")
            else:
                print("Erro ao converter para JSON")
        else:
            print("Erro ao processar o Excel")
    else:
        print("Arquivo Excel não encontrado na pasta de downloads")

if __name__ == "__main__":
    processar_arquivo_excel()
