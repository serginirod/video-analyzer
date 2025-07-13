import os
import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from analyze_video import analyze_video

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/analizar", methods=["POST"])
def analizar():
    if "video" not in request.files:
        logging.error("No se recibió ningún archivo de video.")
        return jsonify({"error": "Falta el archivo de video"}), 400

    file = request.files["video"]

    if file.filename == "":
        logging.error("El nombre del archivo está vacío.")
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if not allowed_file(file.filename):
        logging.error(f"Tipo de archivo no permitido: {file.filename}")
        return jsonify({"error": "Tipo de archivo no permitido"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    logging.info(f"Archivo guardado en {filepath}")

    # ✅ Leer criterios desde archivo fijo
    try:
        with open("criterios.json", "r", encoding="utf-8") as f:
            criterios_json = json.load(f)
    except Exception as e:
        logging.error(f"No se pudo leer criterios.json: {e}")
        return jsonify({"error": "No se pudo leer criterios"}), 500

    # Ejecutar análisis
    try:
        resultado = analyze_video(filepath, criterios_json)
        return jsonify({"mensaje": "Video analizado correctamente", "resultado": resultado})
    except Exception as e:
        logging.exception("Error al analizar el video")
        return jsonify({"error": "Error interno al analizar el video"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
