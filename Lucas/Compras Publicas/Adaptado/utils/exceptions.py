class PortalException(Exception):
    """Exceção base para erros do Portal"""
    pass

class CredentialsError(PortalException):
    """Erro relacionado a credenciais"""
    pass

class AutomationError(PortalException):
    """Erro durante a automação"""
    pass

class WebDriverError(PortalException):
    """Erro relacionado ao WebDriver"""
    pass
