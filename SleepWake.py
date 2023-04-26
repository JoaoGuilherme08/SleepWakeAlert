import cv2
import numpy as np
import dlib
import pygame
import time

# inicializar Pygame para emitir alertas sonoros
pygame.init()
alert_sound = pygame.mixer.Sound('alert.wav')

# inicializar detector de faces e marcos faciais do dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# calcular a relação de aspecto do olho (EAR)
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# inicializar captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# inicializar variáveis de detecção de piscadas e estacionamento
blink_start_time = None
blink_duration = 0
blink_counter = 0
start_time_closed = None
time_closed = 0
parking_detected = False
last_midpoint = None

# loop principal
while True:
    # capturar frame da webcam
    ret, frame = cap.read()
    # detectar faces no frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    # percorrer todas as faces detectadas
    for rect in rects:
        # detectar marcos faciais da face
        landmarks = predictor(gray, rect)
        landmarks = np.array([(p.x, p.y) for p in landmarks.parts()])

        # extrair olhos dos marcos faciais
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]

        # calcular EAR para cada olho
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2

        # verificar se os olhos estão fechados há muito tempo
        if ear < 0.2:
            if start_time_closed is None:
                # começou a fechar os olhos
                start_time_closed = time.time()
            else:
                # olhos ainda fechados
                time_closed = time.time() - start_time_closed
                if time_closed >= 3 and not parking_detected:
                    # olhos fechados por tempo suficiente
                    print('Acorda')
                    alert_sound.play()
                    parking_detected = True
                elif time_closed >= 3 and parking_detected:
                    # alerta contínuo
                    alert_sound.play()
        else:
            # olhos abertos
            start_time_closed = None
            time_closed = 0
            parking_detected = False

    # exibir frame com os marcos faciais e EAR
    for eye in [left_eye, right_eye]:
        cv2.polylines(frame, [eye], True, (0, 255, 255), 1)
    cv2.putText(frame, f'EAR: {ear:.2f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow('Frame', frame)

    # verificar se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) == ord('q'):
        break

# liberar recursos
cap.release()
cv2.destroyAllWindows()