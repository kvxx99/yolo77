import cv2

# URL do stream do scrcpy
stream_url = "tcp://127.0.0.1:8888"

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(stream_url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Exibe o vídeo em tempo real

    buffer = cv2.imencode('.jpg', frame)
    response = requests.post("https://9cd4-35-233-149-23.ngrok-free.app", files={"frame": buffer.tobytes()})
    print(response.json())

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
