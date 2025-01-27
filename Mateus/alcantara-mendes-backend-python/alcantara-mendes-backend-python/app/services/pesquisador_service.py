import json
from pathlib import Path
from app.services.messager_service import ERROR_MESSAGE, MessagerService
from app.utils.constants import BEST_MATCHES
from app.utils.constants import QUESTIONS
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import RetrieverQueryEngine


NO_ANSWER = "Nenhuma resposta clara fornecida."
ANSWER_MESSAGE = "Respostas foram salvas no arquivo: "


def execute(edital_folder: str):
    folder = Path(edital_folder)
    if not folder.exists():
        print(f"O diretório raiz '{edital_folder}' não é um diretório.")
        return

    index_source = folder / "index"
    answers_destination = folder / "answers"
    return processar_indices(index_source, answers_destination)


def chat_indexed(source: str, question: str):
    MessagerService().chat_with_gpt_indexed(source, question)


def processar_indices(source: str, destination: str):
    print(f"Processando as perguntas sobre o edital baseado no indice.")
    OpenAI(temperature=0, model="gpt-3.5-turbo-0125")
    source = Path(source)
    destination = Path(destination)
    destination.mkdir(exist_ok=True, parents=True)

    if source.exists():
        storage_context = StorageContext.from_defaults(persist_dir=str(source))
        index = load_index_from_storage(storage_context)
        retriever = index.as_retriever()
        retriever.similarity_top_k = BEST_MATCHES
        engine = RetrieverQueryEngine.from_args(retriever, response_mode='compact')
        respostas = []

        for pergunta in QUESTIONS:
            print(f"Respondendo a pergunta: '{pergunta}'")
            try:
                response = engine.query(pergunta)
                answer = str(response).strip() if response else NO_ANSWER
                respostas.append({"question": pergunta, "answer": answer})
            except Exception as e:
                print(f"{ERROR_MESSAGE} '{pergunta}': {str(e)}")
                respostas.append({"question": pergunta, "answer": f"Erro: {str(e)}"})

        filename_json = destination / f"{source.parent.name}.json"
        with open(filename_json, 'w', encoding='utf-8') as f:
            json.dump(respostas, f, ensure_ascii=False, indent=4)

        return respostas
