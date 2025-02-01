import logging
import re
from datetime import datetime
from config.settings import DEBUG_MODE, VALIDATIONS

logger = logging.getLogger(__name__)

class PortalValidator:
    """
    Classe responsável por validar dados e operações do Portal de Compras
    """
    
    @staticmethod
    def validate_pregao(numero):
        """
        Valida o número do pregão
        Formato esperado: XX/YYYY onde XX são 2 dígitos e YYYY é o ano
        """
        if not DEBUG_MODE or not VALIDATIONS["campos_obrigatorios"]:
            return True, None
            
        if not numero:
            return False, "Número do pregão é obrigatório"
            
        # Remover caracteres não numéricos
        numero_limpo = ''.join(filter(str.isdigit, str(numero)))
        
        if len(numero_limpo) < 6:
            return False, "Número do pregão deve ter 6 dígitos (2 + 4)"
            
        # Validar formato XX/YYYY
        try:
            numero_parte = numero_limpo[:2]
            ano_parte = numero_limpo[2:6]
            ano = int(ano_parte)
            ano_atual = datetime.now().year
            
            if not (2000 <= ano <= ano_atual + 1):
                return False, f"Ano {ano} inválido"
                
            return True, f"{numero_parte}/{ano_parte}"
            
        except ValueError:
            return False, "Formato inválido. Use o padrão XX/YYYY"
    
    @staticmethod
    def validate_data(data):
        """
        Valida uma data no formato dd/mm/aaaa
        """
        if not DEBUG_MODE or not VALIDATIONS["formato_dados"]:
            return True, None
            
        if not data:
            return True, None  # Data não é obrigatória
            
        try:
            # Validar formato
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
                return False, "Data deve estar no formato dd/mm/aaaa"
                
            # Converter para datetime
            data_obj = datetime.strptime(data, '%d/%m/%Y')
            
            # Validar se é uma data futura
            if data_obj > datetime.now():
                return False, "Data não pode ser futura"
                
            # Validar se é muito antiga (mais de 20 anos)
            anos_atras = datetime.now().year - data_obj.year
            if anos_atras > 20:
                return False, "Data muito antiga"
                
            return True, data
            
        except ValueError:
            return False, "Data inválida"
    
    @staticmethod
    def validate_orgao(orgao):
        """
        Valida o nome do órgão
        """
        if not DEBUG_MODE or not VALIDATIONS["campos_obrigatorios"]:
            return True, None
            
        if not orgao:
            return True, None  # Órgão não é obrigatório
            
        # Remover espaços extras
        orgao = orgao.strip()
        
        if len(orgao) < 2:
            return False, "Nome do órgão muito curto"
            
        # Validar caracteres especiais
        if re.search(r'[^a-zA-Z0-9\s]', orgao):
            return False, "Nome do órgão contém caracteres inválidos"
            
        return True, orgao
    
    @staticmethod
    def validate_uf(uf):
        """
        Valida o código da UF
        """
        if not DEBUG_MODE or not VALIDATIONS["campos_obrigatorios"]:
            return True, None
            
        if not uf:
            return True, None  # UF não é obrigatória
            
        # Lista de UFs válidas
        ufs_validas = {
            "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
            "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
            "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"
        }
        
        uf = uf.upper()
        if uf not in ufs_validas:
            return False, "UF inválida"
            
        return True, uf
    
    @staticmethod
    def validate_credentials(credentials):
        """
        Valida as credenciais de login
        """
        if not DEBUG_MODE or not VALIDATIONS["campos_obrigatorios"]:
            return True, None
            
        if not credentials:
            return False, "Credenciais não fornecidas"
            
        required_fields = ["login", "senha"]
        missing_fields = [field for field in required_fields if not credentials.get(field)]
        
        if missing_fields:
            return False, f"Campos obrigatórios faltando: {', '.join(missing_fields)}"
            
        # Validar comprimento mínimo
        if len(credentials["login"]) < 3:
            return False, "Login deve ter pelo menos 3 caracteres"
            
        if len(credentials["senha"]) < 4:
            return False, "Senha deve ter pelo menos 4 caracteres"
            
        return True, None
    
    @staticmethod
    def validate_search_params(params):
        """
        Valida os parâmetros de pesquisa
        """
        if not DEBUG_MODE or not VALIDATIONS["campos_obrigatorios"]:
            return True, None
            
        # Validar se pelo menos um campo de pesquisa foi preenchido
        if not any(params.values()):
            return False, "Preencha ao menos um campo para pesquisar"
            
        validations = {}
        
        # Validar cada campo
        if params.get("numero_pregao"):
            validations["pregao"] = PortalValidator.validate_pregao(params["numero_pregao"])
            
        if params.get("data_pregao"):
            validations["data"] = PortalValidator.validate_data(params["data_pregao"])
            
        if params.get("orgao"):
            validations["orgao"] = PortalValidator.validate_orgao(params["orgao"])
            
        if params.get("uf"):
            validations["uf"] = PortalValidator.validate_uf(params["uf"])
            
        # Verificar se houve algum erro nas validações
        errors = []
        for field, (valid, msg) in validations.items():
            if not valid:
                errors.append(f"{field}: {msg}")
                
        if errors:
            return False, "\n".join(errors)
            
        return True, None
