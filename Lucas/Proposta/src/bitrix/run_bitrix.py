from src.bitrix.informacoes_gerais import APIBitrix
import os
import json

def run_bitrix():
    """Executa o processo do Bitrix e retorna os dados"""
    try:
        # Executar API Bitrix
        api = APIBitrix()
        dados = api.iniciar_processamento()
        
        # Verificar se o arquivo de dados existe
        json_path = os.path.join('data', 'json', 'dados_operacao.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            # Se os dados foram carregados com sucesso, retornar
            if dados:
                return dados
                
        return None
    except Exception as e:
        print(f"Erro ao executar Bitrix: {str(e)}")
        return None

if __name__ == '__main__':
    run_bitrix()
