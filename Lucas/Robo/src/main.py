import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.bot import LicitacaoBot
from config.settings import CREDENTIALS, PORTAIS, BOT_CONFIG
import schedule
import time

def executar_bot():
    bot = LicitacaoBot()
    try:
        # Solicita ao usuário qual portal deseja utilizar
        portal_selecionado = bot.selecionar_portal()
        
        # Realiza login no portal selecionado
        sucesso_login = bot.login(
            PORTAIS[portal_selecionado],
            CREDENTIALS[portal_selecionado]['USUARIO'],
            CREDENTIALS[portal_selecionado]['SENHA']
        )
        
        if not sucesso_login:
            print(f"Falha ao fazer login no portal {portal_selecionado}")
            return
        
        # Critérios para monitoramento
        criterios = {
            'categoria': input("Digite a categoria de produtos desejada: "),
            'valor_maximo': float(input("Digite o valor máximo aceitável: ")),
            'regiao': input("Digite a região desejada (ex: SP): ")
        }
        
        # Monitora licitações
        licitacoes = bot.monitorar_licitacoes(criterios)
        
        if not licitacoes:
            print("Nenhuma licitação encontrada com os critérios especificados.")
        else:
            print(f"\nForam encontradas {len(licitacoes)} licitações.")
            
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        bot.finalizar()

if __name__ == "__main__":
    print("=== Robô de Licitações ===")
    print("1 - Executar uma vez")
    print("2 - Executar a cada 30 minutos")
    
    opcao = input("\nEscolha uma opção (1 ou 2): ").strip()
    
    if opcao == "1":
        executar_bot()
    elif opcao == "2":
        print("\nBot iniciado no modo agendado. Pressione Ctrl+C para encerrar.")
        schedule.every(30).minutes.do(executar_bot)
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nBot encerrado pelo usuário.")
    else:
        print("Opção inválida!")
