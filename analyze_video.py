import cv2
import mediapipe as mp
import json

mp_pose = mp.solutions.pose

def analizar_altura_bote(landmarks):
    try:
        mano_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
        cadera_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
        altura_relativa = abs(mano_y - cadera_y)
        return altura_relativa < 0.05  # margen de 5%
    except Exception:
        return False

def analizar_rodillas_frente(landmarks):
    try:
        rodilla_izq = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        rodilla_der = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        pie_izq = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        pie_der = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        rodillas_rectas = (
            abs(rodilla_izq.x - pie_izq.x) < 0.1 and
            abs(rodilla_der.x - pie_der.x) < 0.1
        )
        return rodillas_rectas
    except Exception:
        return False

def analyze_video(video_path, criterios_json="criterios.json"):
    resultados = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return ["❌ No se pudo abrir el vídeo."]

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with mp_pose.Pose(static_image_mode=False) as pose:
        success, frame = cap.read()
        while success:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                break  # usamos solo el primer frame válido
            success, frame = cap.read()

    cap.release()

    try:
        if isinstance(criterios_json, list):
            criterios = criterios_json
        else:
            with open(criterios_json, "r", encoding="utf-8") as f:
                criterios = json.load(f)
    except Exception as e:
       return [f"❌ Error al cargar criterios: {str(e)}"]

    for criterio in criterios:
        descripcion = criterio.get("texto")
        peso = criterio.get("peso", 1)

        if "cadera" in descripcion and "bote" in descripcion:
            cumplido = analizar_altura_bote(landmarks)
        elif "rodillas" in descripcion and "frente" in descripcion:
            cumplido = analizar_rodillas_frente(landmarks)
        else:
            resultados.append(f"- {descripcion} (peso {peso}) → [pendiente de implementación]")
            continue

        resultado = "✔️ Cumplido" if cumplido else "❌ Fallido"
        resultados.append(f"- {descripcion} (peso {peso}) → {resultado}")

    resultados.insert(0, f"📊 Total de frames: {total_frames}")
    return resultados
