from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', '')

    if lang == 'en':
        translated_text = GoogleTranslator(source='en', target='fr').translate(text)
    elif lang == 'fr':
        translated_text = GoogleTranslator(source='fr', target='en').translate(text)
    else:
        translated_text = ""

    return jsonify({'translated_text': translated_text})

@app.route('/audio', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', '')

    if not text.strip():
        return jsonify({'error': 'Text is empty'}), 400

    try:
        tts = gTTS(text=text, lang=lang)
        file_name = f'{lang}_audio.mp3'
        file_path = os.path.join('static', file_name)
        tts.save(file_path)
        return jsonify({'audio_path': f'/static/{file_name}', 'file_name': file_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<lang>')
def download_audio(lang):
    file_name = f'{lang}_audio.mp3'
    file_path = os.path.join('static', file_name)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=file_name)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)  # Ensure 'static' folder exists for audio files
    app.run(debug=True)
