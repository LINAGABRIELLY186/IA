# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image
import google.generativeai as genai

# Carregar chave da API do arquivo .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ Chave da API não encontrada no .env")

# Configurar acesso à API do Gemini
genai.configure(api_key=API_KEY)

# Iniciar o app Flask
app = Flask(__name__)

# Liberar acesso ao frontend (HTML local via Live Server)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Modelos do Gemini
modelo_texto = genai.GenerativeModel("models/gemini-1.5-flash")
modelo_imagem = genai.GenerativeModel("models/gemini-1.5-flash")

# Dicionário de perguntas frequentes (respostas fixas da LIA)
faq = {
    "qual o horário da prefeitura?": "De segunda a sexta, das 7h às 13h.",
    "como tirar segunda via do iptu?": "No site da prefeitura ou no setor de tributos.",
    "qual o telefone da prefeitura?": "(86) 99999-9999.",
    "como agendar atendimento?": "Acesse o site ou ligue para a recepção da prefeitura.",
    "onde fica a secretaria de saúde?": "Rua Central, nº 123, ao lado do posto de saúde.",
    "tem concurso aberto?": "Consulte o site oficial da prefeitura para editais e prazos.",
    "quem é o prefeito atual?": "A prefeita atual é Rejane Barros.",
    "onde fica a câmara municipal?": "Na Rua Principal, próximo à praça central.",
}

#Rota de pergunta com texto e add de contexto
@app.route("/api/pergunta", methods=["POST"])
def responder_texto():
    data = request.get_json()
    pergunta = data.get("pergunta", "").lower().strip()

    if pergunta in faq:
        return jsonify({"resposta": f"LIA responde: {faq[pergunta]}"})

    try:
        # Adiciona o contexto fixo da assistente
        contexto = (
            "Você é LIA, a assistente virtual oficial da Prefeitura Municipal de Lagoa do Piauí. "
            "Responda como uma funcionária pública, com informações objetivas, educadas e focadas nos serviços municipais. "
            "Se a pergunta for sobre concursos, impostos, saúde, educação, eventos ou localização de órgãos públicos, "
            "responda como se estivesse prestando atendimento oficial da prefeitura."
        )

        prompt_completo = contexto + "\n\nUsuário perguntou: " + pergunta
        resposta = modelo_texto.generate_content(prompt_completo)

        return jsonify({"resposta": f"LIA responde:\n{resposta.text}"})
    except Exception as e:
        return jsonify({"resposta": f"LIA encontrou um erro ao gerar a resposta: {str(e)}"}), 500


# Rota para perguntas com imagem
@app.route("/api/imagem", methods=["POST"])
def responder_imagem():
    data = request.get_json()
    imagem_base64 = data.get("imagem")
    prompt = data.get("prompt", "Descreva esta imagem.")

    try:
        image_bytes = base64.b64decode(imagem_base64)
        image = Image.open(io.BytesIO(image_bytes))
        resposta = modelo_imagem.generate_content([prompt, image])
        return jsonify({"resposta": f"LIA analisou a imagem:\n{resposta.text}"})
    except Exception as e:
        return jsonify({"resposta": f"LIA encontrou um erro ao analisar a imagem: {str(e)}"}), 500

# Iniciar o servidor
if __name__ == "__main__":
    app.run(debug=True)
