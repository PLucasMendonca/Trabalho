import unittest
from unittest.mock import MagicMock, patch
from core.automation_rules import AutomationRules
from core.credentials import CredentialsManager
from core.webdriver import WebDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAutomationRules(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_element = MagicMock()
        self.mock_driver.find_element.return_value = self.mock_element
        self.mock_wait = MagicMock()
        self.mock_wait.until.return_value = self.mock_element
        
    def test_realizar_login(self):
        """Testa o processo de login"""
        credenciais = {
            "login": "test_user",
            "senha": "test_pass",
            "usuario_mei": "não"
        }
        
        # Simular elementos encontrados
        self.mock_driver.find_element.return_value = self.mock_element
        
        with patch('selenium.webdriver.support.ui.WebDriverWait', return_value=self.mock_wait):
            AutomationRules.realizar_login(self.mock_driver, credenciais)
        
        # Verificar se os métodos corretos foram chamados
        self.mock_driver.get.assert_called_once()
        self.mock_element.send_keys.assert_any_call("test_user")
        self.mock_element.send_keys.assert_any_call("test_pass")
        self.mock_element.click.assert_called()
    
    def test_pesquisar_pregao(self):
        """Testa a pesquisa de pregão"""
        # Dados de teste
        numero = "123/2024"
        data = "19/01/2024"
        uf = "SP"
        orgao = "Prefeitura"
        
        with patch('selenium.webdriver.support.ui.WebDriverWait', return_value=self.mock_wait):
            AutomationRules.pesquisar_pregao(
                self.mock_driver,
                numero=numero,
                data=data,
                uf=uf,
                orgao=orgao
            )
        
        # Verificar chamadas
        self.mock_driver.find_element.assert_called()
        self.mock_element.send_keys.assert_any_call(numero)
        self.mock_element.send_keys.assert_any_call(data)
        self.mock_element.click.assert_called()
    
    def test_pesquisar_pregao_campos_opcionais(self):
        """Testa a pesquisa de pregão com campos opcionais vazios"""
        numero = "123/2024"
        data = "19/01/2024"
        
        with patch('selenium.webdriver.support.ui.WebDriverWait', return_value=self.mock_wait):
            AutomationRules.pesquisar_pregao(
                self.mock_driver,
                numero=numero,
                data=data,
                uf=None,
                orgao=None
            )
        
        # Verificar apenas campos obrigatórios
        self.mock_element.send_keys.assert_any_call(numero)
        self.mock_element.send_keys.assert_any_call(data)

class TestCredentialsManager(unittest.TestCase):
    def setUp(self):
        self.manager = CredentialsManager()
        self.manager.credentials = {"empresas": {}}
        self.manager.save_credentials = MagicMock()
    
    def test_add_empresa(self):
        """Testa adição de empresa"""
        result = self.manager.add_empresa(
            "Empresa Teste",
            "login_teste",
            "senha_teste",
            False
        )
        
        self.assertTrue(result)
        self.assertIn("Empresa Teste", self.manager.credentials["empresas"])
        self.assertEqual(
            self.manager.credentials["empresas"]["Empresa Teste"]["login"],
            "login_teste"
        )
    
    def test_add_empresa_campos_vazios(self):
        """Testa adição de empresa com campos vazios"""
        result = self.manager.add_empresa("", "", "", False)
        self.assertFalse(result)
    
    def test_remove_empresa(self):
        """Testa remoção de empresa"""
        # Adicionar empresa primeiro
        self.manager.credentials["empresas"]["Empresa Teste"] = {
            "login": "test",
            "senha": "test",
            "usuario_mei": "não"
        }
        
        result = self.manager.remove_empresa("Empresa Teste")
        self.assertTrue(result)
        self.assertNotIn("Empresa Teste", self.manager.credentials["empresas"])
    
    def test_backup_restore(self):
        """Testa backup e restauração"""
        # Criar backup
        backup_file = self.manager.create_backup()
        self.assertIsNotNone(backup_file)
        
        # Modificar dados
        self.manager.add_empresa("Nova Empresa", "login", "senha", False)
        
        # Restaurar backup
        result = self.manager.restore_backup(backup_file.name)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
