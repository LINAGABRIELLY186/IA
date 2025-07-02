# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image
import google.generativeai as genai

# Configurar ambiente
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Iniciar app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Modelos
modelo_texto = genai.GenerativeModel("gemini-pro")
modelo_imagem = genai.GenerativeModel("gemini-pro-vision")

# Respostas fixas
faq = {
    "qual o horário da prefeitura?": "De segunda a sexta, das 7h às 13h.",
    "como tirar segunda via do iptu?": "No site da prefeitura ou no setor de tributos.",
}

@app.route("/api/pergunta", methods=["POST"])
def responder_texto():
    data = request.get_json()
    pergunta = data.get("pergunta", "").lower().strip()

    if pergunta in faq:
        return jsonify({"resposta": faq[pergunta]})

    resposta = modelo_texto.generate_content(pergunta)
    return jsonify({"resposta": resposta.text})

@app.route("/api/imagem", methods=["POST"])
def responder_imagem():
    data = request.get_json()
    imagem_base64 = data.get("imagem")
    prompt = data.get("prompt", "Descreva esta imagem.")

    image_bytes = base64.b64decode(imagem_base64)
    image = Image.open(io.BytesIO(image_bytes))

    resposta = modelo_imagem.generate_content([prompt, image])
    return jsonify({"resposta": resposta.text})

if __name__ == "__main__":
    app.run(debug=True)
