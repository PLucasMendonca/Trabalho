from llama_index.core import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
)
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import nltk
import os
from pathlib import Path

# Certifique-se de que as stopwords e o tokenizador estão disponíveis
nltk.download('stopwords')
nltk.download('punkt')

# Assegure-se de que a chave API está definida no ambiente
os.environ['OPENAI_API_KEY'] = "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"
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Função de pré-processamento de perguntas
def preprocess_question(question):
    question = question.lower().translate(str.maketrans('', '', '.,;:!?()[]'))
    stop_words = set(stopwords.words('portuguese'))
    tokens = word_tokenize(question)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    stemmer = RSLPStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    processed_question = ' '.join(stemmed_tokens)
    return processed_question

# Configurações do modelo
Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo-0125")

# Configuração do contexto de serviço
service_context = ServiceContext.from_defaults(chunk_size=512)

# Diretório raiz onde estão as pastas com os arquivos a serem indexados
diretorio_raiz = Path(r'C:\Users\MSI Pulse\Documents\Chatpdf\Alcantara Mendes\RESUMIDOR\FEITO')

def process_documents(pasta, service_context):
    if not any(pasta.iterdir()):
        print(f"Nenhum documento encontrado em {pasta}. Pulando...")
        return

    print(f"Processando documentos em {pasta}")
    try:
        documents = SimpleDirectoryReader(str(pasta)).load_data()
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        pasta_destino_indices = pasta / "indices"
        pasta_destino_indices.mkdir(exist_ok=True)
        index.storage_context.persist(persist_dir=str(pasta_destino_indices))
        print(f"Índices salvos em {pasta_destino_indices}")
    except Exception as e:
        print(f"Erro ao processar documentos em {pasta}: {e}")

# Iterar sobre todas as subpastas do diretório raiz para processar documentos
for pasta in diretorio_raiz.iterdir():
    if pasta.is_dir():
        process_documents(pasta, service_context)

print("Todos os documentos foram processados e os índices criados.")
