Tutorial: Como Configurar e Rodar Projetos Next.js e Flask

Configuração e Execução do Frontend (Next.js)

Passo 1: Instalação de Node.js e npm
1. Baixar e Instalar Node.js:
   - Acesse o site oficial do Node.js e baixe o instalador apropriado para seu sistema operacional.
   - Siga as instruções para instalar o Node.js, que inclui o npm (gerenciador de pacotes do Node.js).

2. Verificar a Instalação:
   - Abra o terminal (ou PowerShell no Windows) e digite os seguintes comandos para verificar se o Node.js e o npm foram instalados corretamente:
     node -v
     npm -v
   - Você deve ver as versões instaladas para ambos.

Passo 2: Instalar Dependências do Projeto
1. Navegar até a Pasta do Projeto:
   - No terminal, navegue até a pasta do projeto com o comando:
     cd caminho/para/sua/pasta/alcantara-acessoria-licitacoes-nextjs

2. Instalar Dependências:
   - Execute o comando para instalar as dependências listadas no package.json:
     npm install
   - Se houver problemas com dependências, tente atualizar o npm e instalar novamente:
     npm install -g npm@latest

Passo 3: Rodar o Servidor de Desenvolvimento
1. Iniciar o Servidor:
   - Com o terminal aberto na pasta do projeto, inicie o servidor de desenvolvimento com:
     npm run dev

2. Acessar o Frontend:
   - Abra um navegador e acesse http://localhost:3000. Você deve ver a aplicação Next.js em execução.

Configuração e Execução do Backend (Flask)

Passo 1: Instalação do Python e pip
1. Baixar e Instalar Python:
   - Acesse o site oficial do Python e baixe a versão mais recente para seu sistema operacional.
   - Siga as instruções para instalar o Python, garantindo que a opção para adicionar Python ao PATH esteja selecionada.

2. Verificar a Instalação:
   - Abra o terminal (ou PowerShell no Windows) e digite os seguintes comandos:
     python --version
     pip --version
   - Você deve ver as versões instaladas para ambos.

Passo 2: Instalar Dependências do Projeto
1. Instalar Pacotes Requeridos:
   - Se você tiver um arquivo requirements.txt na pasta do projeto, instale as dependências com:
     pip install -r requirements.txt
   - Se não tiver requirements.txt, você pode instalar as dependências manualmente com:
     pip install Flask==3.0.3
     pip install Flask-SQLAlchemy==3.1.1
     pip install python-dotenv==1.0.1
     pip install nltk==3.8.1
     pip install PyMySQL==1.1.1
     pip install llama-index==0.10.65
     pip install pymupdf==1.24.9
     pip install flask-cors

Passo 3: Rodar o Servidor Flask
1. Verificar o Código do run.py:
   - Certifique-se de que o arquivo run.py está configurado corretamente para executar a aplicação Flask.

2. Executar a Aplicação Flask:
   - No terminal, navegue até a pasta do projeto e execute:
     python run.py

3. Acessar o Backend:
   - Abra um navegador e acesse http://localhost:5000. Você deve ver que o backend Flask está funcionando.