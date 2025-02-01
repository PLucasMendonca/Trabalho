from datetime import datetime
import time

class PortalProcessor:
    def __init__(self, callback_log=None):
        self.callback_log = callback_log
        
    def log(self, mensagem):
        """Função auxiliar para logging"""
        if self.callback_log:
            self.callback_log(mensagem)
        
    def identificar_portal(self, card_data):
        """Identifica qual portal será processado"""
        portal = card_data.get('portal', '').lower()
        self.log(f"\nIdentificando portal: {portal}")
        
        portais_validos = {
            'bll': 'Bolsa de Licitações e Leilões',
            'comprasnet': 'ComprasNet',
            'compraspublicas': 'Compras Públicas',
            'bnc': 'Bolsa Nacional de Compras',
            'comprasbr': 'ComprasBR',
            'licitanet': 'LicitaNet'
        }
        
        portal_nome = None
        for key, nome in portais_validos.items():
            if key in portal:
                portal_nome = nome
                break
                
        if portal_nome:
            self.log(f"Portal identificado: {portal_nome}")
            return {
                'nome': portal_nome,
                'tipo': key,
                'url': self.get_portal_url(key),
                'pregao': card_data.get('pregao', ''),
                'empresa': card_data.get('empresa', ''),
                'card_id': card_data.get('id', '')
            }
        else:
            self.log(f"AVISO: Portal não reconhecido: {portal}")
            return None
            
    def get_portal_url(self, portal_tipo):
        """Retorna a URL base do portal"""
        urls = {
            'bll': 'https://bll.org.br',
            'comprasnet': 'https://www.comprasnet.gov.br',
            'compraspublicas': 'https://www.portaldecompraspublicas.com.br',
            'bnc': 'https://www.bnc.org.br',
            'comprasbr': 'https://comprasbr.com.br',
            'licitanet': 'https://www.licitanet.com.br'
        }
        return urls.get(portal_tipo, '')
