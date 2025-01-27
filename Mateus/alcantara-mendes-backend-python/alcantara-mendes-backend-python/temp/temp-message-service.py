from app.utils.constants import BEST_MATCHES
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import RetrieverQueryEngine


class MessagerService:
    def __init__(self):
        self.context = ""

    def send_message(self, message):
        self.context += message
        response = self.chat_with_gpt(self.context)

        return response

    def chat_with_gpt(self, context):
        OpenAI.ChatCompletion.create(
            temperature=0,
            model="gpt-3.5-turbo-0125",
            messages=self
        )

        return str(response).strip() if response else "Nenhuma resposta clara fornecida."
