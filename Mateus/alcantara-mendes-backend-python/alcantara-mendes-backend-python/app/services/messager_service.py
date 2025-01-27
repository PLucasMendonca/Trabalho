from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.core.query_engine import RetrieverQueryEngine
from app.utils.constants import BEST_MATCHES

ERROR_MESSAGE = "Um erro ocorreu ao processar a pergunta."


class MessagerService:
    def __init__(self, temperature=0, model="gpt-3.5-turbo-0125"):
        self.model = model
        self.messages = []
        self.temperature = temperature

    def send_message(self, message: str):
        self.messages += message
        response = self.chat_with_gpt(self.messages)

        return response

    def chat_with_gpt(self, messages):
        self.messages.append({"role": "user", "content": messages})

        resposta = OpenAI.ChatCompletion.create(
            temperature=0,
            model=self.model,
            messages=self.messages
        )

        answer = resposta['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": answer})

        return answer

    def chat_query_engine(self, source: str, pergunta: str):
        source = Path(source)

        if source.exists():
            storage_context = StorageContext.from_defaults(persist_dir=source)
            index = load_index_from_storage(storage_context)
            retriever = index.as_retriever()
            retriever.similarity_top_k = BEST_MATCHES
            engine = RetrieverQueryEngine.from_args(retriever, response_mode='compact')
            try:
                response = engine.query(pergunta)
                return response
            except Exception as e:
                print(f"{ERROR_MESSAGE} '{pergunta}': {str(e)}")
        return None

    def chat_with_gpt_indexed(self, source: str, pergunta: str):
        response = self.chat_query_engine(source, pergunta)
        if response:
            return response

        return self.chat_with_gpt(pergunta)
