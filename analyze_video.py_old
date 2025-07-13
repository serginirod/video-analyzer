import mediapipe as mp
import cv2
import json
import logging

def analyze_video(video_path, criterios_json):
    criterios = json.loads(criterios_json)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    resultados = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(image_rgb)

        if result.pose_landmarks:
            altura_bote = analizar_altura_bote(result.pose_landmarks)
            if altura_bote:
                resultados.append('Bote a altura correcta')

    cap.release()
    pose.close()

    mensaje = f"🎥 Analizando: {video_path.split('/')[-1]}\n"
    mensaje += f"📊 Total de frames: {total_frames}\n"
    mensaje += "=== Evaluación de criterios ===\n"

    for criterio in criterios:
        descripcion = criterio.get('texto')
        peso = criterio.get('peso', 1)

        if not descripcion:
            logging.warning(f"Criterio inválido: {criterio}")
            continue  # salta al siguiente criterio

        if descripcion == "Bote hasta la altura de la cadera +/- 5cm":
            cumple = any("Bote a altura correcta" in r for r in resultados)
            estado = "✔️ Cumplido" if cumple else "❌ No cumplido"
        else:
            estado = "[pendiente de implementación]"

        mensaje += f"- {descripcion} (peso {peso}) → {estado}\n"

    return mensaje

def analizar_altura_bote(pose_landmarks):
    MUÑECA_DERECHA = 16
    CADERA_DERECHA = 24

    muñeca = pose_landmarks.landmark[MUÑECA_DERECHA]
    cadera = pose_landmarks.landmark[CADERA_DERECHA]

    altura_muñeca = muñeca.y
    altura_cadera = cadera.y

    diferencia = abs(altura_muñeca - altura_cadera)
    tolerancia = 0.05

    return diferencia <= tolerancia
