import json
import os
from typing import List, Dict, Any
from src.utils.word_processor import criar_tabela_word
from src.processors.direto_api import ProcessadorAPI

class FilaProcessor:
    def __init__(self, callback_log=None):
        self.callback_log = callback_log
        self.api_processor = ProcessadorAPI(callback_log)

    def log(self, mensagem: str, tipo: str = "info"):
        """Função auxiliar para logging"""
        if self.callback_log:
            self.callback_log(mensagem, tipo)
        else:
            print(mensagem)

    def carregar_dados_json(self, callback_log=None):
        """Carrega os dados do arquivo JSON"""
        try:
            # Usar caminho absoluto
            diretorio_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            arquivo_json = os.path.join(diretorio_base, 'data', 'json', 'dados_operacao.json')
            
            if callback_log:
                callback_log(f"Tentando carregar arquivo: {arquivo_json}")
            
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                dados_json = json.load(f)
                if callback_log:
                    callback_log(f"Arquivo JSON carregado. Total de empresas: {len(dados_json)}")
                return dados_json
                
        except Exception as e:
            if callback_log:
                callback_log(f"Erro ao carregar arquivo JSON: {str(e)}")
            return None
            
    def carregar_cards_aceitos(self, callback_log=None):
        """Carrega apenas os cards em estado ACEITAS"""
        dados_json = self.carregar_dados_json(callback_log)
        if not dados_json:
            if callback_log:
                callback_log("Nenhum dado JSON carregado")
            return []
            
        if callback_log:
            callback_log("Iniciando processamento de cards aceitos...")
            
        cards_aceitos = []
        
        # Primeiro, coletar todos os cards aceitos
        for empresa_id, empresa_data in dados_json.items():
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
                            'ID': card.get('ID', 'N/A'),
                            'pregao': pregao,
                            'portal': portal,
                            'empresa': nome_empresa,
                            'empresa_id': empresa_id,
                            'status': 'ACEITAS',
                            'Número do pregão': card.get('Número do pregão', 'N/A'),
                            'Objeto': card.get('Objeto', 'N/A'),
                            'Data': card.get('Data', 'N/A'),
                            'Cidade': card.get('Cidade', 'N/A'),
                            'Estado': card.get('Estado', 'N/A'),
                            'Validade da proposta': card.get('Validade da proposta', 'N/A'),
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

    def processar_cards_aceitos(self, cards_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processa os cards aceitos do JSON"""
        cards_aceitos = []
        empresas_processadas = set()

        for empresa_data in cards_data:
            nome_empresa = empresa_data.get('empresa', '')
            empresa_id = empresa_data.get('empresa_id', '')
            cards = empresa_data.get('cards', [])
            cards_empresa = []

            for card in cards:
                if card.get('status') == 'ACEITAS':
                    portal = card.get('portal', '')
                    pregao = card.get('Número do pregão', '')

                    card_processado = {
                        'ID': card.get('ID', 'N/A'),
                        'pregao': pregao,
                        'portal': portal,
                        'empresa': nome_empresa,
                        'empresa_id': empresa_id,
                        'status': 'ACEITAS',
                        'Número do pregão': card.get('Número do pregão', 'N/A'),
                        'Objeto': card.get('Objeto', 'N/A'),
                        'Data': card.get('Data', 'N/A'),
                        'Cidade': card.get('Cidade', 'N/A'),
                        'Estado': card.get('Estado', 'N/A'),
                        'Validade da proposta': card.get('Validade da proposta', 'N/A'),
                        'dados_completos': card
                    }
                    cards_empresa.append(card_processado)

            if cards_empresa:
                cards_aceitos.extend(cards_empresa)
                if nome_empresa not in empresas_processadas:
                    self.log(f"Empresa {nome_empresa}: {len(cards_empresa)} cards aceitos")
                    empresas_processadas.add(nome_empresa)

        self.log(f"\nTotal de cards aceitos encontrados: {len(cards_aceitos)}")
        return cards_aceitos

    def verificar_campos_obrigatorios(self, item):
        """Verifica se o card possui todos os campos obrigatórios"""
        campos_obrigatorios = {
            'portal': 'Portal',
            'pregao': 'Número do Pregão'
        }
        
        campos_faltantes = []
        
        # Verificar portal
        portal = item.get('portal', '')
        if not portal:
            campos_faltantes.append('Portal (inválido)')
            
        # Verificar outros campos
        for campo, nome in campos_obrigatorios.items():
            if campo != 'portal':  # Portal já foi verificado
                valor = item.get(campo)
                if not valor or valor == 'N/A':
                    campos_faltantes.append(nome)
        
        return campos_faltantes

    def processar_proximo(self, cards_data, callback_log=None):
        """Processa o próximo item da fila"""
        if not cards_data:
            return []

        self.callback_log = callback_log
        cards_aceitos = self.processar_cards_aceitos(cards_data)
        self.log(f"\nTotal de cards aceitos: {len(cards_aceitos)}")

        # Primeiro tenta processar todos os cards via API/JSON
        for card in cards_aceitos:
            # Tenta processar via API primeiro
            processado_api = self.api_processor.processar_portal(card)
            
            # Se não conseguiu via API, verifica os campos obrigatórios
            if not processado_api:
                campos_faltantes = self.verificar_campos_obrigatorios(card)
                if campos_faltantes:
                    self.log(f"Card inválido - ID {card.get('ID', 'N/A')} - Campos faltantes: {', '.join(campos_faltantes)}", "error")
                    continue

                # Se os campos estão ok mas não achou via API, loga que precisa usar Firefox
                self.log(f"Card {card.get('ID', 'N/A')} precisa ser processado via Firefox", "info")

        # Após processar todos os cards, gera o documento Word
        if self.api_processor.pilha_processamento:
            self.api_processor.processar_pilha_word()

        return cards_aceitos
