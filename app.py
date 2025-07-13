from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from analyze_video import analyze_video

app = Flask(__name__)
CORS(app)

# Configurar logs
logging.basicConfig(level=logging.INFO)

# Ruta para analizar vídeo
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'Falta el archivo de vídeo'}), 400

        video_file = request.files['video']
        if video_file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400

        video_path = os.path.join('uploads', video_file.filename)
        os.makedirs('uploads', exist_ok=True)
        video_file.save(video_path)

        criterios = request.form.get('criterios')
        if not criterios:
            return jsonify({'error': 'Faltan criterios'}), 400

        logging.info(f"📹 Recibido: {video_path}")
        logging.info(f"📋 Criterios: {criterios}")

        resultado = analyze_video(video_path, criterios)
        return jsonify({'resultado': resultado})
    except Exception as e:
        logging.exception("💥 Error en la API:")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
