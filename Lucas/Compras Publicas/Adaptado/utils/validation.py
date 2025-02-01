import logging
import time
import requests
from functools import wraps
from config.settings import DEBUG_MODE, VALIDATIONS, PORTAL_URL
from selenium.common.exceptions import WebDriverException
import urllib3
import re
from datetime import datetime

# Desabilitar avisos de SSL inseguro em desenvolvimento
if DEBUG_MODE:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

def validate_action(action_type):
    """
    Decorador para validar e logar ações
    :param action_type: Tipo da ação (ex: 'login', 'pesquisa', etc)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not DEBUG_MODE:
                return func(*args, **kwargs)
            
            start_time = time.time()
            
            try:
                # Log detalhado
                if VALIDATIONS["log_detalhado"]:
                    logger.info(f"Iniciando ação: {action_type}")
                    logger.info(f"Argumentos: {args}, {kwargs}")
                
                # Verificar conexão
                if VALIDATIONS["verificar_conexao"]:
                    try:
                        # Em desenvolvimento, ignorar verificação SSL
                        verify = not DEBUG_MODE
                        requests.get(PORTAL_URL, timeout=5, verify=verify)
                    except requests.RequestException as e:
                        logger.error(f"Erro de conexão: {e}")
                        raise ConnectionError("Não foi possível conectar ao portal")
                
                # Simular ação
                if VALIDATIONS["simular_acoes"]:
                    logger.info(f"Simulando ação: {action_type}")
                    return None
                
                # Tempo de espera
                if VALIDATIONS["tempo_espera"] > 0:
                    time.sleep(VALIDATIONS["tempo_espera"])
                
                # Executar função
                result = func(*args, **kwargs)
                
                # Log de sucesso
                if VALIDATIONS["log_acoes"]:
                    duration = time.time() - start_time
                    logger.info(f"Ação {action_type} completada em {duration:.2f}s")
                
                return result
            
            except Exception as e:
                logger.error(f"Erro na ação {action_type}: {e}")
                raise
            
        return wrapper
    return decorator

def validate_form_data(data, required_fields=None, field_types=None):
    """
    Valida dados de formulário
    :param data: Dicionário com os dados
    :param required_fields: Lista de campos obrigatórios
    :param field_types: Dicionário com tipos esperados para cada campo
    """
    if not DEBUG_MODE:
        return True
    
    errors = []
    
    # Validar campos obrigatórios
    if VALIDATIONS["campos_obrigatorios"] and required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Campo obrigatório não preenchido: {field}")
    
    # Validar formato dos dados
    if VALIDATIONS["formato_dados"] and field_types:
        for field, expected_type in field_types.items():
            if field in data and data[field]:
                try:
                    # Tentar converter para o tipo esperado
                    expected_type(data[field])
                except (ValueError, TypeError):
                    errors.append(f"Formato inválido para {field}")
    
    if errors:
        raise ValueError("\n".join(errors))
    
    return True

def validate_webdriver(func):
    """
    Decorador para validar operações do WebDriver
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not DEBUG_MODE:
            return func(*args, **kwargs)
        
        try:
            # Verificar se o WebDriver está respondendo
            driver = args[0].driver  # Assume que o primeiro argumento é self com driver
            driver.current_url
            
            result = func(*args, **kwargs)
            
            # Log da ação
            if VALIDATIONS["log_acoes"]:
                logger.info(f"Operação do WebDriver concluída: {func.__name__}")
            
            return result
            
        except WebDriverException as e:
            logger.error(f"Erro no WebDriver: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            raise
    
    return wrapper

def validate_connection(url):
    """
    Valida a conexão com uma URL
    """
    if not DEBUG_MODE or not VALIDATIONS["verificar_conexao"]:
        return True
    
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"Erro ao verificar conexão com {url}: {e}")
        return False

class ValidationContext:
    """
    Contexto para validação de operações
    """
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        if DEBUG_MODE and VALIDATIONS["log_detalhado"]:
            self.start_time = time.time()
            logger.info(f"Iniciando operação: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if DEBUG_MODE and VALIDATIONS["log_detalhado"]:
            duration = time.time() - self.start_time
            if exc_type:
                logger.error(f"Erro na operação {self.operation_name}: {exc_val}")
            else:
                logger.info(f"Operação {self.operation_name} completada em {duration:.2f}s")

class ValidationError(Exception):
    """Exceção para erros de validação"""
    pass

def validate_processo_number(numero):
    """
    Valida o número do processo
    Formato esperado: XXXXX/AAAA ou XXXXX.XXXXX/AAAA
    """
    pattern = r'^\d{1,5}(?:\.\d{1,5})?/\d{4}$'
    if not re.match(pattern, numero):
        raise ValidationError("Número do processo inválido. Use o formato: XXXXX/AAAA ou XXXXX.XXXXX/AAAA")
    return True

def validate_date(date_str):
    """
    Valida uma data no formato dd/mm/aaaa
    Verifica também se a data é futura
    """
    try:
        data = datetime.strptime(date_str, "%d/%m/%Y")
        if data < datetime.now():
            raise ValidationError("A data deve ser futura")
        return True
    except ValueError:
        raise ValidationError("Data inválida. Use o formato: dd/mm/aaaa")

def validate_uf(uf):
    """Valida UF brasileira"""
    ufs = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]
    if uf and uf not in ufs:
        raise ValidationError("UF inválida")
    return True

def validate_orgao(orgao):
    """
    Valida nome do órgão
    Regras:
    - Mínimo 3 caracteres
    - Apenas letras, números e espaços
    - Sem caracteres especiais
    """
    if orgao:
        if len(orgao) < 3:
            raise ValidationError("Nome do órgão deve ter no mínimo 3 caracteres")
        if not re.match(r'^[\w\s]+$', orgao):
            raise ValidationError("Nome do órgão contém caracteres inválidos")
    return True

def validate_credentials(credentials):
    """
    Valida credenciais de usuário
    Regras:
    - Login: mínimo 4 caracteres
    - Senha: mínimo 6 caracteres
    - Senha deve conter letras e números
    """
    if not credentials.get("login") or len(credentials["login"]) < 4:
        raise ValidationError("Login deve ter no mínimo 4 caracteres")
    
    senha = credentials.get("senha", "")
    if len(senha) < 6:
        raise ValidationError("Senha deve ter no mínimo 6 caracteres")
    
    if not (re.search(r'[A-Za-z]', senha) and re.search(r'\d', senha)):
        raise ValidationError("Senha deve conter letras e números")
    
    return True

def validate_mei(is_mei, cnpj):
    """
    Valida se o CNPJ é compatível com MEI
    Regras:
    - Se is_mei=True, CNPJ deve começar com 11
    - CNPJ deve ser válido
    """
    if not cnpj or len(cnpj) != 14:
        raise ValidationError("CNPJ inválido")
    
    if is_mei and not cnpj.startswith("11"):
        raise ValidationError("CNPJ não é de MEI")
    
    # Validação do dígito verificador do CNPJ
    if not validate_cnpj(cnpj):
        raise ValidationError("CNPJ inválido")
    
    return True

def validate_cnpj(cnpj):
    """Valida dígitos verificadores do CNPJ"""
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if len(set(cnpj)) == 1:
        return False
    
    # Primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    
    if int(cnpj[12]) != digito1:
        return False
    
    # Segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
    
    return int(cnpj[13]) == digito2

def validate_all(processo=None, data=None, uf=None, orgao=None, credentials=None, is_mei=None, cnpj=None):
    """Função helper para validar todos os campos de uma vez"""
    try:
        if processo:
            validate_processo_number(processo)
        if data:
            validate_date(data)
        if uf:
            validate_uf(uf)
        if orgao:
            validate_orgao(orgao)
        if credentials:
            validate_credentials(credentials)
        if is_mei is not None and cnpj:
            validate_mei(is_mei, cnpj)
        return True
    except ValidationError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise
