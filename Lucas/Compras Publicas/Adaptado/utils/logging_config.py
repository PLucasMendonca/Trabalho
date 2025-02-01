import logging
import logging.handlers
from pathlib import Path
from config.settings import LOG_FILE, LOGGING

def setup_logging():
    """
    Configura o sistema de logging com rotação de arquivos e formatação melhorada
    """
    # Criar diretório de logs se não existir
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formato detalhado
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo com rotação
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=5*1024*1024,  # 5MB por arquivo
        backupCount=5,         # Manter 5 arquivos de backup
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configurar logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remover handlers existentes
    root_logger.handlers = []
    
    # Adicionar novos handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configurar níveis específicos para alguns loggers
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado com sucesso")
