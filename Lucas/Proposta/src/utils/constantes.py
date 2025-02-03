# Dicionário com as modalidades por portal
MODALIDADES = {
    'bll': ['Selecione a modalidade', 'Pregão', 'Concorrência', 'Dispensa'],
    'comprasnet': ['Selecione a modalidade', 'Pregão', 'Concorrência', 'Dispensa'],
    'compraspublicas': ['Selecione a modalidade', 'Pregão', 'Concorrência', 'Dispensa'],
    'bnc': ['Selecione a modalidade', 'Pregão', 'Concorrência', 'Dispensa'],
    'comprasbr': ['Selecione a modalidade', 'Pregão', 'Concorrência', 'Dispensa'],
    'licitanet': ['Selecione a modalidade', 'Pregão', 'Concorrência', 'Dispensa']
}

# Mapeamento de valores das modalidades por portal
MODALIDADE_VALUES = {
    'bll': {'Selecione a modalidade': '0', 'Pregão': '1', 'Concorrência': '3', 'Dispensa': '10', 'Licitação 13.303': '16'},
    'comprasnet': {'Selecione a modalidade': '0', 'Pregão': '1', 'Concorrência': '3', 'Cotação': '15' , 'Dispensa': '10'},
    'compraspublicas': {'Selecione a modalidade': '0', 'Pregão': '1', 'Concorrência': '3', 'Dispensa': '10'},
    'bnc': {'Selecione a modalidade': '0', 'Pregão': '1', 'Concorrência': '3', 'Dispensa': '10','Licitação 13.303': '16'},
    'comprasbr': {'Selecione a modalidade': '0', 'Pregão': '1', 'Concorrência': '3', 'Dispensa': '10'},
    'licitanet': {'Selecione a modalidade': '0', 'Pregão': '1', 'Concorrência': '3', 'Dispensa': '10'}
}

# Valores dos portais no select
PORTAL_SELECT_VALUES = {
    'bll': '24',
    'comprasnet': '1',
    'compraspublicas': '3',
    'bnc': '1362',
    'comprasbr': '898',
    'licitanet': '28'
}

# Mapeamento de nomes de portais
PORTAL_MAPPING = {
    "ComprasNet": "comprasnet",
    "Comprasnet": "comprasnet",
    "COMPRASNET": "comprasnet",
    "COMPRAS GOV": "comprasnet",


    "Compras Públicas": "compraspublicas",
    "BNC - Bolsa Nacional de Compras": "bnc",
    "ComprasBR": "comprasbr",
    "Licitanet": "licitanet",
    "BLL": "bll",
    "BLL - Bolsa de Licitações e Leilões":"bll"
}