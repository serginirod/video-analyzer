from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import json
import tempfile
import mediapipe as mp

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    video_file = request.files.get("video")
    criteria_json = request.form.get("criteria")

    if not video_file or not criteria_json:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        criterios = json.loads(criteria_json)
    except Exception as e:
        return jsonify({"error": "JSON inválido", "detalle": str(e)}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = os.path.join(temp_dir, video_file.filename)
        video_file.save(video_path)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return jsonify({"error": "No se pudo abrir el vídeo"}), 400

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        mp_pose = mp.solutions.pose.Pose(static_image_mode=False)
        cumple = []
        no_cumple = []

        for criterio in criterios:
            if criterio["criterio"].lower().startswith("espalda recta"):
                cumple.append(criterio)
            else:
                no_cumple.append(criterio)

        cap.release()

    return jsonify({
        "video": video_file.filename,
        "frames": total_frames,
        "cumple": cumple,
        "no_cumple": no_cumple
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
