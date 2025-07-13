from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import logging

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    logger.info("🔍 Petición recibida en /analyze")

    # Validar existencia de fichero de vídeo
    if "video" not in request.files:
        logger.warning("⚠️ No se recibió el archivo de vídeo")
        return jsonify({"error": "Faltan datos"}), 400

    video = request.files["video"]

    if video.filename == "":
        logger.warning("⚠️ El nombre del archivo está vacío")
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    # Guardar vídeo
    video_filename = f"{uuid.uuid4()}_{video.filename}"
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    video.save(video_path)
    logger.info(f"✅ Vídeo guardado en: {video_path}")

    # Procesar criterios
    criterios_json = request.form.get("criterios")
    if not criterios_json:
        logger.warning("⚠️ No se recibieron criterios")
        return jsonify({"error": "Faltan datos"}), 400

    logger.info(f"📄 Criterios recibidos: {criterios_json}")

    # Simulación de análisis
    resultado = f"""
    🎥 Analizando: {video.filename}
    === Evaluación de criterios ===
    (esto es una simulación, aquí irá el análisis real con MediaPipe y OpenCV)
    """

    logger.info("✅ Análisis simulado completo")

    return jsonify({"resultado": resultado.strip()}), 200


# 🔥 Punto de entrada principal compatible con Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
