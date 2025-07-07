# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image
import google.generativeai as genai

# Carregar chave da API do .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ Chave da API não encontrada no .env")

genai.configure(api_key=API_KEY)

# Criar app Flask com suporte a arquivos estáticos
app = Flask(__name__, static_folder="static")
CORS(app)  # Libera para qualquer origem

# Modelos Gemini
modelo_texto = genai.GenerativeModel("models/gemini-1.5-flash")
modelo_imagem = genai.GenerativeModel("models/gemini-1.5-flash")

# Respostas fixas da LIA
faq = {
    "qual o horário da prefeitura?": "De segunda a sexta, das 7h às 13h.",
    "como tirar segunda via do iptu?": "No site da prefeitura ou no setor de tributos.",
    "qual o telefone da prefeitura?": "(86) 99999-9999.",
    "como agendar atendimento?": "Acesse o site ou ligue para a recepção da prefeitura.",
    "onde fica a secretar
