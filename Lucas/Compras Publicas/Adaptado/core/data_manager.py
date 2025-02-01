import json
from pathlib import Path
from datetime import datetime

class DataManager:
    def __init__(self):
        self.data_dir = Path.home() / "portal_compras_data"
        self.data_dir.mkdir(exist_ok=True)
        self.credentials_file = self.data_dir / "credentials.json"
        self.search_history_file = self.data_dir / "search_history.json"
        
    def save_credentials(self, profile_name, username, password):
        """Salva as credenciais de um perfil"""
        data = self._load_json(self.credentials_file)
        
        data[profile_name] = {
            "usuario": username,
            "senha": password,
            "ultima_atualizacao": datetime.now().isoformat()
        }
        
        self._save_json(self.credentials_file, data)
        
    def get_credentials(self, profile_name):
        """Recupera as credenciais de um perfil"""
        data = self._load_json(self.credentials_file)
        return data.get(profile_name)
        
    def get_all_profiles(self):
        """Retorna todos os perfis salvos"""
        return list(self._load_json(self.credentials_file).keys())
        
    def save_search_data(self, profile_name, search_data):
        """Salva os dados de pesquisa de um perfil"""
        data = self._load_json(self.search_history_file)
        
        if profile_name not in data:
            data[profile_name] = []
            
        # Adiciona os novos dados com timestamp
        search_entry = {
            **search_data,
            "timestamp": datetime.now().isoformat()
        }
        
        data[profile_name].append(search_entry)
        
        # Mantém apenas as últimas 10 pesquisas
        data[profile_name] = data[profile_name][-10:]
        
        self._save_json(self.search_history_file, data)
        
    def get_search_history(self, profile_name):
        """Recupera o histórico de pesquisa de um perfil"""
        data = self._load_json(self.search_history_file)
        return data.get(profile_name, [])
        
    def get_last_search(self, profile_name):
        """Recupera a última pesquisa de um perfil"""
        history = self.get_search_history(profile_name)
        return history[-1] if history else None
        
    def _load_json(self, file_path):
        """Carrega dados de um arquivo JSON"""
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
        
    def _save_json(self, file_path, data):
        """Salva dados em um arquivo JSON"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
