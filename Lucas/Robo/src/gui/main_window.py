from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit,
                               QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.bot import LicitacaoBot
from config.settings import CREDENTIALS, PORTAIS, BOT_CONFIG

class BotThread(QThread):
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, portal, criterios):
        super().__init__()
        self.portal = portal
        self.criterios = criterios
        self.bot = None
        
    def run(self):
        try:
            self.bot = LicitacaoBot()
            self.status_signal.emit("Iniciando bot...")
            
            # Seleciona o portal
            self.status_signal.emit(f"Conectando ao portal {self.portal}...")
            self.bot.set_portal(self.portal)
            
            # Login
            sucesso_login = self.bot.login(
                PORTAIS[self.portal],
                CREDENTIALS[self.portal]['USUARIO'],
                CREDENTIALS[self.portal]['SENHA']
            )
            
            if not sucesso_login:
                self.error_signal.emit(f"Falha ao fazer login no portal {self.portal}")
                return
                
            self.status_signal.emit("Login realizado com sucesso!")
            
            # Monitora licitações
            self.status_signal.emit("Buscando licitações...")
            licitacoes = self.bot.monitorar_licitacoes(self.criterios)
            
            if not licitacoes:
                self.status_signal.emit("Nenhuma licitação encontrada com os critérios especificados.")
            else:
                self.status_signal.emit(f"Foram encontradas {len(licitacoes)} licitações!")
                
        except Exception as e:
            self.error_signal.emit(f"Erro durante a execução: {str(e)}")
        finally:
            if self.bot:
                self.bot.finalizar()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robô de Licitações")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        
    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Grupo de Configurações
        config_group = QGroupBox("Configurações")
        config_layout = QVBoxLayout()
        
        # Portal
        portal_layout = QHBoxLayout()
        portal_label = QLabel("Portal:")
        self.portal_combo = QComboBox()
        self.portal_combo.addItems(["BLL", "BNC"])
        portal_layout.addWidget(portal_label)
        portal_layout.addWidget(self.portal_combo)
        config_layout.addLayout(portal_layout)
        
        # Critérios
        criterios_group = QGroupBox("Critérios de Busca")
        criterios_layout = QVBoxLayout()
        
        # Categoria
        categoria_layout = QHBoxLayout()
        categoria_label = QLabel("Categoria:")
        self.categoria_input = QLineEdit()
        categoria_layout.addWidget(categoria_label)
        categoria_layout.addWidget(self.categoria_input)
        criterios_layout.addLayout(categoria_layout)
        
        # Valor Máximo
        valor_layout = QHBoxLayout()
        valor_label = QLabel("Valor Máximo (R$):")
        self.valor_input = QDoubleSpinBox()
        self.valor_input.setMaximum(1000000000)
        self.valor_input.setValue(50000)
        valor_layout.addWidget(valor_label)
        valor_layout.addWidget(self.valor_input)
        criterios_layout.addLayout(valor_layout)
        
        # Região
        regiao_layout = QHBoxLayout()
        regiao_label = QLabel("Região:")
        self.regiao_input = QLineEdit()
        regiao_layout.addWidget(regiao_label)
        regiao_layout.addWidget(self.regiao_input)
        criterios_layout.addLayout(regiao_layout)
        
        criterios_group.setLayout(criterios_layout)
        config_layout.addWidget(criterios_group)
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Botões de Controle
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Iniciar Monitoramento")
        self.start_button.clicked.connect(self.iniciar_bot)
        self.stop_button = QPushButton("Parar")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.parar_bot)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        main_layout.addLayout(buttons_layout)
        
        # Log
        log_group = QGroupBox("Log de Execução")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Estilização
        self.setup_styles()
        
    def setup_styles(self):
        # Define estilos para os componentes
        style = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 6px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0px 5px 0px 5px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
            QTextEdit {
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """
        self.setStyleSheet(style)
        
    def add_log(self, message):
        self.log_text.append(message)
        
    def iniciar_bot(self):
        # Coleta os critérios
        criterios = {
            'categoria': self.categoria_input.text(),
            'valor_maximo': self.valor_input.value(),
            'regiao': self.regiao_input.text()
        }
        
        # Validações básicas
        if not criterios['categoria']:
            QMessageBox.warning(self, "Atenção", "Por favor, preencha a categoria.")
            return
            
        if not criterios['regiao']:
            QMessageBox.warning(self, "Atenção", "Por favor, preencha a região.")
            return
        
        # Inicia o bot em uma thread separada
        self.bot_thread = BotThread(self.portal_combo.currentText(), criterios)
        self.bot_thread.status_signal.connect(self.add_log)
        self.bot_thread.error_signal.connect(self.handle_error)
        self.bot_thread.finished.connect(self.bot_finished)
        
        # Atualiza interface
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.add_log("Iniciando monitoramento...")
        
        # Inicia a thread
        self.bot_thread.start()
        
    def parar_bot(self):
        if hasattr(self, 'bot_thread') and self.bot_thread.isRunning():
            self.add_log("Parando o bot...")
            self.bot_thread.terminate()
            self.bot_thread.wait()
            self.bot_finished()
            
    def handle_error(self, error_message):
        QMessageBox.critical(self, "Erro", error_message)
        self.add_log(f"ERRO: {error_message}")
        
    def bot_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.add_log("Bot finalizado.")
