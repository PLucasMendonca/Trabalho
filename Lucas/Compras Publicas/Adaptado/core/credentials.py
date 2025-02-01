import json
import time
from pathlib import Path
from datetime import datetime
import shutil
from config.settings import JSON_DIR, CACHE_DURATION, CREDENTIALS_FILE
import logging

logger = logging.getLogger(__name__)

class CredentialsManager:
    _instance = None
    _cache = {}
    _last_read = 0
    
    def __new__(cls):
        """Implementa o padrão Singleton"""
        if cls._instance is None:
            cls._instance = super(CredentialsManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa o gerenciador de credenciais"""
        self.credentials_file = JSON_DIR / 'credentials.json'
        self.backup_dir = JSON_DIR / 'backups'
        self.credentials = self.load_credentials()
        self._cache = {}
        self._last_read = 0
        self.ensure_credentials_file()
        self.ensure_backup_dir()
    
    def ensure_credentials_file(self):
        """Garante que o arquivo de credenciais existe"""
        if not self.credentials_file.exists():
            self.credentials_file.parent.mkdir(parents=True, exist_ok=True)
            self.save_credentials({"empresas": {}})
    
    def ensure_backup_dir(self):
        """Garante que o diretório de backups existe"""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            logger.debug("Diretório de backups verificado")
        except Exception as e:
            logger.error(f"Erro ao criar diretório de backups: {e}")
    
    def create_backup(self):
        """
        Cria um backup das credenciais
        :return: Path do arquivo de backup ou None se falhar
        """
        try:
            # Criar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"credentials_backup_{timestamp}.json"
            
            # Copiar arquivo atual
            shutil.copy2(self.credentials_file, backup_file)
            
            # Limpar backups antigos (manter últimos 5)
            self.cleanup_old_backups()
            
            logger.info(f"Backup criado com sucesso: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return None
    
    def cleanup_old_backups(self, keep_last=5):
        """
        Limpa backups antigos mantendo apenas os N mais recentes
        :param keep_last: Número de backups para manter
        """
        try:
            # Listar todos os backups
            backups = sorted(
                self.backup_dir.glob("credentials_backup_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Remover backups antigos
            for backup in backups[keep_last:]:
                backup.unlink()
                logger.debug(f"Backup antigo removido: {backup}")
                
        except Exception as e:
            logger.error(f"Erro ao limpar backups antigos: {e}")
    
    def restore_backup(self, backup_file):
        """
        Restaura um backup específico
        :param backup_file: Path do arquivo de backup
        :return: True se sucesso, False se erro
        """
        try:
            # Verificar se backup existe
            backup_path = self.backup_dir / backup_file
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup não encontrado: {backup_file}")
            
            # Criar backup do arquivo atual antes de restaurar
            self.create_backup()
            
            # Restaurar backup
            shutil.copy2(backup_path, self.credentials_file)
            
            # Recarregar credenciais
            self.credentials = self.load_credentials()
            
            logger.info(f"Backup restaurado com sucesso: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {e}")
            return False
    
    def get_available_backups(self):
        """
        Retorna lista de backups disponíveis
        :return: Lista de nomes de arquivos de backup
        """
        try:
            return [
                x.name for x in sorted(
                    self.backup_dir.glob("credentials_backup_*.json"),
                    key=lambda x: x.stat().st_mtime,
                    reverse=True
                )
            ]
        except Exception as e:
            logger.error(f"Erro ao listar backups: {e}")
            return []
    
    def get_users(self):
        """Retorna a lista de usuários cadastrados"""
        try:
            # Recarregar se necessário
            if time.time() - self._last_read > CACHE_DURATION:
                self.load_credentials()
            
            # Retornar lista de empresas
            return list(self.credentials.get("empresas", {}).keys())
        except Exception as e:
            logger.error(f"Erro ao obter lista de usuários: {e}")
            return []
    
    def get_all_credentials(self):
        """
        Retorna todas as credenciais
        :return: Dicionário com todas as credenciais
        """
        try:
            # Recarregar se necessário
            if time.time() - self._last_read > CACHE_DURATION:
                self.load_credentials()
            return self.credentials
        except Exception as e:
            logger.error(f"Erro ao obter todas as credenciais: {e}")
            return {"empresas": {}}
    
    def get_credentials(self, empresa=None):
        """
        Retorna as credenciais de uma empresa específica ou todas as credenciais
        
        :param empresa: Nome da empresa (opcional)
        :return: Dicionário com credenciais da empresa ou todas as credenciais
        """
        try:
            # Recarregar se necessário
            if time.time() - self._last_read > CACHE_DURATION:
                self.load_credentials()
            
            if empresa is None:
                return self.credentials
            return self.credentials.get("empresas", {}).get(empresa)
        except Exception as e:
            logger.error(f"Erro ao obter credenciais: {e}")
            return None if empresa else {"empresas": {}}
    
    def load_credentials(self):
        """Recarrega as credenciais do arquivo"""
        try:
            with open(self.credentials_file, 'r', encoding='utf-8') as f:
                self.credentials = json.load(f)
            self._last_read = time.time()
            logger.debug("Credenciais recarregadas com sucesso")
            return self.credentials
        except FileNotFoundError:
            logger.warning("Arquivo de credenciais não encontrado. Criando novo...")
            self.credentials = {"empresas": {}}
            self.save_credentials()
            return self.credentials
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar arquivo de credenciais: {e}")
            raise ValueError("Arquivo de credenciais corrompido")
        except Exception as e:
            logger.error(f"Erro ao carregar credenciais: {e}")
            raise
    
    def save_credentials(self):
        """Salva as credenciais no arquivo"""
        try:
            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                json.dump(self.credentials, f, indent=4, ensure_ascii=False)
            self._last_read = time.time()
            logger.debug("Credenciais salvas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao salvar credenciais: {e}")
            raise
    
    def add_empresa(self, nome: str, login: str, senha: str, is_mei: bool = False) -> bool:
        """
        Adiciona ou atualiza credenciais de uma empresa
        
        :param nome: Nome da empresa
        :param login: Login da empresa
        :param senha: Senha da empresa
        :param is_mei: Se é MEI ou não
        :return: True se sucesso, False se erro
        """
        try:
            if not nome or not login or not senha:
                raise ValueError("Todos os campos são obrigatórios")
            
            # Criar backup antes de modificar
            self.create_backup()
            
            # Atualizar credenciais
            if "empresas" not in self.credentials:
                self.credentials["empresas"] = {}
            
            self.credentials["empresas"][nome] = {
                "login": login,
                "senha": senha,
                "usuario_mei": "sim" if is_mei else "não"
            }
            
            # Salvar no arquivo
            self.save_credentials()
            
            logger.info(f"Credenciais da empresa {nome} salvas com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar credenciais da empresa {nome}: {e}")
            return False
    
    def remove_empresa(self, nome: str) -> bool:
        """
        Remove as credenciais de uma empresa
        
        :param nome: Nome da empresa
        :return: True se sucesso, False se erro
        """
        try:
            if nome in self.credentials.get("empresas", {}):
                # Criar backup antes de remover
                self.create_backup()
                
                del self.credentials["empresas"][nome]
                self.save_credentials()
                logger.info(f"Empresa {nome} removida com sucesso")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover empresa {nome}: {e}")
            return False
    
    def get_empresa(self, nome):
        """
        Retorna as credenciais de uma empresa específica
        :param nome: Nome da empresa
        :return: Dicionário com as credenciais da empresa ou None se não encontrada
        """
        try:
            # Recarregar se necessário
            if time.time() - self._last_read > CACHE_DURATION:
                self.load_credentials()
            
            # Buscar nas empresas
            return self.credentials.get("empresas", {}).get(nome)
        except Exception as e:
            logger.error(f"Erro ao buscar empresa {nome}: {e}")
            return None
