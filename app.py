# app.py
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

# Cargar las credenciales desde el archivo .env
load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

app = Flask(__name__)

class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api-free.deepl.com/v2/translate"

    def translate(self, text, source_lang='EN', target_lang='DE'):
        params = {
            'auth_key': self.api_key,
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        response = requests.post(self.api_url, data=params)
        response.raise_for_status()
        result = response.json()
        return result['translations'][0]['text']

translator = Translator(DEEPL_API_KEY)

@app.route('/api/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        translation = translator.translate(text)
        return jsonify({'translation': translation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
