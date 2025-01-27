import os
import nltk
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.routes import llma_routes
from app.configs.config import Config
from flask_cors import CORS

db = SQLAlchemy()
nltk.download('stopwords')
nltk.download('punkt')


def create_app():

    load_dotenv()

    API_KEY = os.getenv('OPENAI_API_KEY')
    TOKENIZERS_PARALLELISM = os.getenv('TOKENIZERS_PARALLELISM')

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, resources={r"/smart/chat": {"origins": "http://localhost:3000"}})
    CORS(app, resources={
         r"/smart/index": {"origins": "http://localhost:3000"}})

    os.environ['OPENAI_API_KEY'] = API_KEY
    os.environ['TOKENIZERS_PARALLELISM'] = TOKENIZERS_PARALLELISM

    with app.app_context():
        app.register_blueprint(llma_routes.bp)

    return app
