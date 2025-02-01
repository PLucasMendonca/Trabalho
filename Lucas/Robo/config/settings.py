from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Bot
BOT_CONFIG = {
    'TEMPO_ENTRE_LANCES': 30,  # segundos
    'TEMPO_MONITORAMENTO': 300,  # segundos
    'VALOR_MINIMO_LANCE': 100.0,
    'PERCENTUAL_DECREMENTO': 0.01,  # 1%
}

# Credenciais (devem ser definidas em arquivo .env)
CREDENTIALS = {
    'BLL': {
        'USUARIO': os.getenv('BLL_USER'),
        'SENHA': os.getenv('BLL_PASS'),
    },
    'BNC': {
        'USUARIO': os.getenv('BNC_USER'),
        'SENHA': os.getenv('BNC_PASS'),
    }
}

# URLs dos portais de licitação
PORTAIS = {
    'BLL': 'https://bllcompras.com/Home/Login',
    'BNC': 'https://bnc.org.br/sistema/',
}

# Configurações de Logs
LOG_CONFIG = {
    'PATH': 'logs/',
    'LEVEL': 'INFO',
    'FORMAT': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
}
