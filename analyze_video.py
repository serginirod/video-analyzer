import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

def analizar_altura_bote(lm, tolerancia=0.05):
    hip_y = (lm[mp_pose.PoseLandmark.LEFT_HIP].y + lm[mp_pose.PoseLandmark.RIGHT_HIP].y) / 2
    wrist_y = (lm[mp_pose.PoseLandmark.LEFT_WRIST].y + lm[mp_pose.PoseLandmark.RIGHT_WRIST].y) / 2
    altura_bote = abs(wrist_y - hip_y)
    return altura_bote <= tolerancia

def analizar_rodillas_adelante(lm, tolerancia=0.05):
    left_knee_x = lm[mp_pose.PoseLandmark.LEFT_KNEE].x
    right_knee_x = lm[mp_pose.PoseLandmark.RIGHT_KNEE].x
    left_hip_x = lm[mp_pose.PoseLandmark.LEFT_HIP].x
    right_hip_x = lm[mp_pose.PoseLandmark.RIGHT_HIP].x

    alineacion_izquierda = abs(left_knee_x - left_hip_x)
    alineacion_derecha = abs(right_knee_x - right_hip_x)

    return alineacion_izquierda < tolerancia and alineacion_derecha < tolerancia

def evaluar_criterios(video_path, criterios):
    resultados = []
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    bote_ok = []
    rodillas_ok = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            for criterio in criterios:
                nombre = criterio.get("nombre", "").lower()

                if "cadera" in nombre:
                    cumple = analizar_altura_bote(lm)
                    bote_ok.append(cumple)
                elif "rodilla" in nombre:
                    cumple = analizar_rodillas_adelante(lm)
                    rodillas_ok.append(cumple)

    cap.release()

    for criterio in criterios:
        nombre = criterio.get("nombre", "").lower()
        peso = criterio.get("peso", 1)

        if "cadera" in nombre:
            cumplido = sum(bote_ok) / len(bote_ok) > 0.7 if bote_ok else False
        elif "rodilla" in nombre:
            cumplido = sum(rodillas_ok) / len(rodillas_ok) > 0.7 if rodillas_ok else False
        else:
            cumplido = None

        resultados.append({
            "nombre": criterio.get("nombre"),
            "peso": peso,
            "cumplido": cumplido
        })

    return {
        "total_frames": total_frames,
        "resultados": resultados
    }
