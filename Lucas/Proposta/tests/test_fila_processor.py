import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_path)

from src.processors.fila_processor import FilaProcessor

def main():
    # Criar instância do FilaProcessor
    processor = FilaProcessor()
    
    # Função de callback para logs
    def log_callback(mensagem):
        print(f"LOG: {mensagem}")
    
    # Carregar dados do JSON
    print("\n=== Carregando dados do JSON ===")
    dados = processor.carregar_dados_json(callback_log=log_callback)
    
    if dados:
        print("\n=== Carregando cards aceitos ===")
        cards = processor.carregar_cards_aceitos(callback_log=log_callback)
        
        print("\n=== Cards Aceitos ===")
        for card in cards:
            print(f"\nPregão: {card['pregao']}")
            print(f"Portal: {card['portal']}")
            print(f"Empresa: {card['empresa']}")
            print(f"Cidade: {card['cidade']}")
            print(f"Estado: {card['estado']}")
            print(f"Objeto: {card['objeto']}")
            print("-" * 50)

if __name__ == "__main__":
    main() 