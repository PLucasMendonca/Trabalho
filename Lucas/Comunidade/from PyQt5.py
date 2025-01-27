import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QPixmap
import os

class WhatsAppApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Aplicativo com Múltiplos WhatsApp Web")
        self.setGeometry(100, 100, 1000, 700)

        # Widget central e layout principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()

        # Layout lateral para botões
        side_layout = QVBoxLayout()
        self.button_whatsapp1 = QPushButton("Abrir WhatsApp 1", self)
        self.button_whatsapp2 = QPushButton("Abrir WhatsApp 2", self)

        side_layout.addWidget(self.button_whatsapp1)
        side_layout.addWidget(self.button_whatsapp2)
        

        # Conectando os botões
        self.button_whatsapp1.clicked.connect(self.show_whatsapp1)
        self.button_whatsapp2.clicked.connect(self.show_whatsapp2)

        # Adicionando o layout lateral ao principal
        layout.addLayout(side_layout)

        # Área de conteúdo principal
        self.content_area = QStackedWidget()
        layout.addWidget(self.content_area)

        # Configuração do WhatsApp Web (instância 1)
        self.browser1 = self.create_browser("profile1", "117.0.5938.132")
        # Configuração do WhatsApp Web (instância 2)
        self.browser2 = self.create_browser("profile2", "118.0.5993.88")

        # Adicionando widgets ao QStackedWidget
        self.content_area.addWidget(self.browser1)  # WhatsApp 1
        self.content_area.addWidget(self.browser2)  # WhatsApp 2

        # Configurando o layout principal
        central_widget.setLayout(layout)

        # Exibindo a janela
        self.show()

    def create_browser(self, profile_name, chrome_version):
        """Cria um navegador com um perfil de navegador exclusivo."""
        profile = QWebEngineProfile(profile_name, self)  # Nome único para cada perfil
        profile.setHttpUserAgent(
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
        )

        # Define caminhos exclusivos para cache e armazenamento persistente
        profile.setCachePath(os.path.join(os.getcwd(), f"{profile_name}_cache"))
        profile.setPersistentStoragePath(os.path.join(os.getcwd(), f"{profile_name}_storage"))

        browser = QWebEngineView()
        browser.setPage(QWebEnginePage(profile, browser))
        browser.setUrl(QUrl("https://web.whatsapp.com"))
        return browser

    def show_whatsapp1(self):
        self.content_area.setCurrentWidget(self.browser1)

    def show_whatsapp2(self):
        self.content_area.setCurrentWidget(self.browser2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhatsAppApp()
    sys.exit(app.exec_())
