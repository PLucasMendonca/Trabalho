import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Modo de desenvolvimento
DEBUG_MODE = True  # Mudar para False em produção

# Configurações do Portal
PORTAL_URL = "https://operacao.portaldecompraspublicas.com.br/18/loginext/"
WAIT_TIMEOUT = 20  # Aumentado para dar mais tempo para elementos carregarem
RETRY_ATTEMPTS = 3
CACHE_DURATION = 300  # 5 minutos em segundos

# Diretórios do projeto
JSON_DIR = BASE_DIR / 'json'
LOGS_DIR = BASE_DIR / 'logs'

# Configurações do Chrome
CHROME_OPTIONS = [
    '--start-maximized',           # Maximizar janela
    '--disable-gpu',              # Desabilitar aceleração GPU
    '--no-sandbox',               # Necessário para alguns ambientes
    '--disable-dev-shm-usage',    # Evitar problemas de memória
    '--ignore-certificate-errors', # Ignorar erros de certificado
    '--ignore-ssl-errors',        # Ignorar erros SSL
    '--allow-insecure-localhost', # Permitir localhost inseguro
    '--disable-blink-features=AutomationControlled',  # Evitar detecção de automação
    '--disable-notifications',    # Desabilitar notificações
    '--disable-extensions',       # Desabilitar extensões
    '--disable-infobars',        # Desabilitar infobar
    '--disable-popup-blocking',   # Desabilitar bloqueio de popups
    '--window-position=0,0',     # Posicionar janela no canto superior esquerdo
    '--window-size=1920,1080'    # Tamanho da janela em Full HD
]

# Configurações de validação
VALIDATIONS = {
    "log_detalhado": True,     # Log detalhado de ações
    "verificar_conexao": True, # Verificar conexão antes das ações
    "simular_acoes": False,    # Modo simulação (não executa ações)
    "tempo_espera": 1,         # Tempo de espera entre ações (segundos)
    "log_acoes": True         # Log de todas as ações
}

# Configurações de tema
THEME = {
    "light": {
        "fg_color": ["#f2f2f2", "#2b2b2b"],
        "text_color": ["#000000", "#ffffff"],
        "button_color": ["#3b8ed0", "#1f6aa5"],
        "entry_color": ["#ffffff", "#343638"]
    },
    "dark": {
        "fg_color": ["#2b2b2b", "#f2f2f2"],
        "text_color": ["#ffffff", "#000000"],
        "button_color": ["#1f6aa5", "#3b8ed0"],
        "entry_color": ["#343638", "#ffffff"]
    }
}

# Atalhos de teclado
KEYBOARD_SHORTCUTS = {
    "<Control-l>": "abrir_login_gui",     # Ctrl+L para abrir login
    "<Control-p>": "abrir_portal_gui",    # Ctrl+P para abrir portal
    "<Control-s>": "abrir_pesquisa_gui",  # Ctrl+S para abrir pesquisa
    "<Control-q>": "on_closing",          # Ctrl+Q para sair
    "<F5>": "atualizar_interface",        # F5 para atualizar
    "<F1>": "mostrar_ajuda"              # F1 para ajuda
}

# Configurações de backup
BACKUP = {
    "enabled": True,
    "interval": 3600,  # 1 hora em segundos
    "max_backups": 5,
    "backup_dir": "backups"
}

# Configurações de arquivos
CREDENTIALS_FILE = JSON_DIR / 'credentials.json'
SEARCH_HISTORY_FILE = JSON_DIR / 'search_history.json'
LOG_FILE = LOGS_DIR / 'portal.log'

# Configurações de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOG_FILE),
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Criar diretórios necessários
JSON_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
