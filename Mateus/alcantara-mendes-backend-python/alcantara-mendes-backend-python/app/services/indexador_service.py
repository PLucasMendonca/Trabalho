from pathlib import Path
import fitz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    GPTVectorStoreIndex as GPTVectorStore,
    SimpleDirectoryReader,
    ServiceContext,
    Document,
)
from app.utils.constants import ROOT_FOLDER


def indexed_file(filename: str):
    file_process = ROOT_FOLDER+'/'+filename
    service_context = ServiceContext.from_defaults(chunk_size=512)
    return process_file(file_process, service_context)


def process_file(file: str, service: ServiceContext):
    print(f"Indexando o arquivo {file}.")
    file_path = Path(file)
    if not file_path.exists():
        print(f"O arquivo {file} não existe.")
        return

    try:
        with fitz.open(file_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()

        doc = Document(text=text)
        index = GPTVectorStore.from_documents([doc], service_context=service)

        destination = file_path.parent / file_path.stem
        path_index = destination / "index"
        file_move_path = destination / file_path.name
        path_index.mkdir(exist_ok=True, parents=True)
        index.storage_context.persist(persist_dir=str(path_index))
        file_path.rename(file_move_path)
        print(f"Índices salvos.")
        return file_move_path

    except Exception as e:
        print(f"Erro ao processar arquivo {file}: {e}")


def save(folder: Path):
    Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo-0125")
    service_context = ServiceContext.from_defaults(chunk_size=512)
    for pasta in folder.iterdir():
        if pasta.is_dir():
            process_documents(pasta, service_context)


def preprocess_question(question):
    question = question.lower().translate(str.maketrans('', '', '.,;:!?()[]'))
    stop_words = set(stopwords.words('portuguese'))
    tokens = word_tokenize(question)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    stemmer = RSLPStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    processed_question = ' '.join(stemmed_tokens)
    return processed_question


def process_documents(folder, service):
    if not any(folder.iterdir()):
        print(f"Nenhum documento encontrado em {folder}. Pulando...")
        return

    print(f"Processando documentos em {folder}")
    try:
        docs = SimpleDirectoryReader(str(folder)).load_data()
        index = GPTVectorStore.from_documents(docs, service_context=service)
        index_destination = folder / "indices"
        index_destination.mkdir(exist_ok=True)
        index.storage_context.persist(persist_dir=str(index_destination))
        print(f"Índices salvos em {index_destination}")
    except Exception as e:
        print(f"Erro ao processar documentos em {folder}: {e}")
