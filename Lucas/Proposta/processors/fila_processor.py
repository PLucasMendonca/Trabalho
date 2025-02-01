import json
import os
from datetime import datetime

class FilaProcessor:
    def __init__(self):
        self.dados_json = None
        self.cards_data = []
        
    def carregar_dados_json(self, callback_log=None):
        """Carrega os dados do arquivo JSON"""
        try:
            # Usar caminho absoluto
            diretorio_base = os.path.dirname(os.path.abspath(__file__))
            arquivo_json = os.path.join(diretorio_base, 'json', 'dados_operacao.json')
            
            if callback_log:
                callback_log(f"Tentando carregar arquivo: {arquivo_json}")
            
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                self.dados_json = json.load(f)
                if callback_log:
                    callback_log(f"Arquivo JSON carregado. Total de empresas: {len(self.dados_json)}")
                return self.dados_json
                
        except Exception as e:
            if callback_log:
                callback_log(f"Erro ao carregar arquivo JSON: {str(e)}")
            return None
            
    def carregar_cards_aceitos(self, callback_log=None):
        """Carrega apenas os cards em estado ACEITAS"""
        if not self.dados_json:
            if callback_log:
                callback_log("Nenhum dado JSON carregado")
            return []
            
        if callback_log:
            callback_log("Iniciando processamento de cards aceitos...")
            
        self.cards_data = []
        cards_aceitos = []
        
        # Primeiro, coletar todos os cards aceitos
        for empresa_id, empresa_data in self.dados_json.items():
            nome_empresa = empresa_data.get('nome_empresa', 'N/A')
            
            # Verificar se tem etapas e se tem cards ACEITOS
            etapas = empresa_data.get('etapas', {})
            if 'ACEITAS' in etapas and 'cards' in etapas['ACEITAS']:
                cards = etapas['ACEITAS']['cards']
                if cards:  # Verifica se a lista não está vazia
                    if callback_log:
                        callback_log(f"Empresa {nome_empresa}: {len(cards)} cards aceitos")
                    
                    # Processar cada card
                    for card in cards:
                        # Garantir que portal e pregão não sejam None
                        portal = card.get('Portal', '')
                        if portal is None:
                            portal = ''
                            
                        pregao = card.get('Número do pregão', '')
                        if pregao is None:
                            pregao = ''
                        
                        card_processado = {
                            'id': card.get('ID', 'N/A'),
                            'pregao': pregao,
                            'portal': portal,
                            'empresa': nome_empresa,
                            'empresa_id': empresa_id,
                            'status': 'ACEITAS',
                            'dados_completos': card
                        }
                        cards_aceitos.append(card_processado)
        
        # Ordenar cards por portal e depois por pregão
        def chave_ordenacao(x):
            portal = x['portal'].lower() if x['portal'] else ''
            pregao = x['pregao'].lower() if x['pregao'] else ''
            return (portal, pregao)
            
        cards_aceitos.sort(key=chave_ordenacao)
        
        if callback_log:
            callback_log(f"\nTotal de cards aceitos encontrados: {len(cards_aceitos)}")
            
        return cards_aceitos

    def processar_proximo(self, cards_data, callback_log=None):
        """Processa o próximo item da fila"""
        if not cards_data:
            if callback_log:
                callback_log("Fila vazia")
            return None, cards_data
            
        # Pegar o primeiro item
        proximo_item = cards_data[0]
        # Remover o item da fila
        cards_data = cards_data[1:]
        
        if callback_log:
            callback_log(f"Processando item: {proximo_item.get('pregao', 'N/A')}")
            
        return proximo_item, cards_data
