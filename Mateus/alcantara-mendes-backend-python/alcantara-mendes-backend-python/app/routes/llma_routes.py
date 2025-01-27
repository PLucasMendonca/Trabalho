import os
import json
from pathlib import Path
from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from app.utils.validators import allowed_file
from app.services.indexador_service import indexed_file
from app.services.messager_service import MessagerService
from app.services.pesquisador_service import execute
from app.utils.constants import ROOT_FOLDER
import datetime

bp = Blueprint('smart', __name__, url_prefix='/smart')


@bp.route('/', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"}), 200


@bp.route('/index', methods=['POST'])
def index_pdf():
    print("---------------------------------")
    print("Iniciado em:", datetime.datetime.now())
    print("---------------------------------")
    print(" ")
    print(" ")


    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    if file and allowed_file(file.filename):

        # Process file
        filename = secure_filename(file.filename)
        filepath = os.path.join(ROOT_FOLDER, filename)
        file.save(filepath)

        index_name = filename.split('.')[0]

        # Index file
        filepath = indexed_file(filename)

        # Execute the search engine
        results = execute(filepath.parent)

        print(" ")
        print(" ")
        print("---------------------------------")
        print("Termino em:", datetime.datetime.now())
        print("---------------------------------")

        # Return success message
        return jsonify({"message": "File indexed successfully!", "data": results, "index": index_name}), 200

    return jsonify({"message": "Invalid file type"}), 400


@bp.route('/document/<path:filename>')
def get_asset(filename):

    return send_from_directory('asset/processed/PE_54_24_-_SITE_PREFEITURA_-_Edital', filename)


@bp.route('/answers', methods=['GET'])
def get_answers():
    answers = Path(ROOT_FOLDER + '/PE_54_24_-_SITE_PREFEITURA_-_Edital/answers/PE_54_24_-_SITE_PREFEITURA_-_Edital.json')
    # Read the JSON file
    with open(answers, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Return the JSON data
    return jsonify(data)


@bp.route('/chat', methods=['POST'])
def chat():
    edital = request.form.get('edital')
    question = request.form.get('question')
    if not edital or not question:
        return jsonify({"message": "Invalid data"}), 400
    folder = Path(ROOT_FOLDER + '/' + edital + '/index')
    response = MessagerService().chat_with_gpt_indexed(folder, question)
    results = [{"question": question, "answer": str(response)}]

    return jsonify({"message": "File indexed successfully!", "data": results, "index": edital}), 200
