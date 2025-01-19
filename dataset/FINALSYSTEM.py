import cv2
import numpy as np
from ultralytics import YOLO
import subprocess
import time
from datetime import datetime

# Configurações do dispositivo e modelo
MODEL_PATH = "runs/detect/bot-detection/weights/best.pt"  # Caminho para o modelo YOLO treinado
MODEL_RESOLUTION = (640, 640)  # Resolução do treinamento do modelo
SCREEN_RESOLUTION = (2400, 1080)  # Resolucão real da tela do celular (largura x altura)
MODEL_CONFIDENCE = 0.5  # Confiança mínima para considerar detecções
SWIPE_SPEED = 300  # Velocidade do swipe em milissegundos
LOG_FILE = "system_logs.txt"

# Inicializar o modelo YOLO
model = YOLO(MODEL_PATH)

# Função para registrar logs
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

# Função para capturar um frame da tela do celular
def capture_screen_frame():
    process = subprocess.Popen(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    image_data = process.stdout.read()  # Captura o stream completo
    frame = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    return frame

# Função para escalonar coordenadas (640x640 -> resolução da tela)
def scale_coordinates(x_min, y_min, x_max, y_max):
    scale_x = SCREEN_RESOLUTION[0] / MODEL_RESOLUTION[0]
    scale_y = SCREEN_RESOLUTION[1] / MODEL_RESOLUTION[1]
    return (
        int(x_min * scale_x),
        int(y_min * scale_y),
        int(x_max * scale_x),
        int(y_max * scale_y)
    )

# Função para enviar o comando de swipe na direção do bot
def swipe_to_target(bot_x, bot_y, screen_width, screen_height):
    # Determina o ponto central da tela
    center_x, center_y = screen_width // 2, screen_height // 2
    
    # Calcula o movimento necessário (pequenos ajustes)
    delta_x = bot_x - center_x
    delta_y = bot_y - center_y
    
    # Ajusta os valores para o swipe (redução para movimentos suaves)
    swipe_x = int(center_x + delta_x * 0.3)
    swipe_y = int(center_y + delta_y * 0.3)

    # Envia o comando via ADB
    subprocess.run(["adb", "shell", f"input swipe {center_x} {center_y} {swipe_x} {swipe_y} {SWIPE_SPEED}"])
    log_message(f"Movimento ajustado: Swipe de ({center_x}, {center_y}) para ({swipe_x}, {swipe_y})")

# Loop principal de detecção em tempo real
try:
    log_message("Iniciando o sistema de detecção em tempo real...")
    while True:
        # Captura um frame da tela
        frame = capture_screen_frame()
        if frame is None:
            log_message("Erro ao capturar o frame. Tentando novamente...")
            continue
        
        # Redimensiona para a resolução do modelo (640x640)
        resized_frame = cv2.resize(frame, MODEL_RESOLUTION)
        
        # Realiza a inferência
        results = model.predict(resized_frame, conf=MODEL_CONFIDENCE)
        detections = results[0].boxes.data.cpu().numpy()  # Extrai as caixas
        
        # Desenha as caixas e realiza swipes, se necessário
        for detection in detections:
            x_min, y_min, x_max, y_max, confidence, class_id = detection
            if confidence < MODEL_CONFIDENCE:
                continue
            
            # Escala as coordenadas para a resolução da tela
            x_min, y_min, x_max, y_max = scale_coordinates(x_min, y_min, x_max, y_max)
            
            # Calcula o ponto central do bot
            bot_x = int((x_min + x_max) / 2)
            bot_y = int((y_min + y_max) / 2)
            
            # Desenha a caixa no frame (opcional, para debugging local)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, f"Bot ({confidence:.2f})", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Realiza o swipe
            swipe_to_target(bot_x, bot_y, SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1])
            time.sleep(0.5)  # Pequeno atraso entre swipes

        # Logs periódicos
        log_message(f"Frame processado: {len(detections)} bots detectados.")

except KeyboardInterrupt:
    log_message("Sistema encerrado pelo usuário.")

