from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "upload"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "🎬 Backend de análisis de vídeo funcionando correctamente."

@app.route('/analyze', methods=['POST'])
def analyze_video():
    try:
        print("✅ Petición recibida en /analyze")

        # 1. Verificamos que viene el vídeo
        if 'video' not in request.files:
            print("❌ No se encontró el archivo de vídeo en la petición")
            return jsonify({"error": "No se ha enviado el vídeo"}), 400

        # 2. Verificamos que vienen los criterios
        if 'criterios' not in request.form:
            print("❌ No se encontraron criterios en la petición")
            return jsonify({"error": "No se han enviado los criterios"}), 400

        video_file = request.files['video']
        criterios_json = request.form['criterios']

        # 3. Guardamos el vídeo
        video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(video_path)
        print(f"🎥 Vídeo guardado en: {video_path}")

        # 4. Guardamos los criterios como JSON
        criterios = json.loads(criterios_json)
        criterios_path = os.path.join(UPLOAD_FOLDER, "criterios.json")
        with open(criterios_path, "w") as f:
            json.dump(criterios, f, indent=2)
        print(f"📋 Criterios guardados en: {criterios_path}")

        # 5. Resultado simulado por ahora (aquí meteremos MediaPipe)
        analisis_resultado = {
            "video": video_file.filename,
            "frames_detectados": 176,  # Simulado
            "criterios": [
                {
                    "criterio": c["criterio"],
                    "peso": c["peso"],
                    "resultado": "[pendiente de implementación]"
                } for c in criterios
            ]
        }

        print("✅ Análisis simulado completado")
        return jsonify(analisis_resultado)

    except Exception as e:
        print(f"💥 Error inesperado: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
