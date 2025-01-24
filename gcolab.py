from flask import Flask, request, jsonify
import cv2
import numpy as np
from FINALSYSTEM import detect_objects  # Importe sua função YOLO treinada

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    # Receber imagem
    file = request.files['image']
    img_array = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # YOLO para detectar bots
    detections = detect_objects(image)
    print(f"Detecções: {detections}")

    # Gerar comandos baseados nas detecções
    commands = generate_commands(detections)
    return jsonify(commands)

def generate_commands(detections):
    commands = []
    for det in detections:
        x, y, w, h = det['box']
        commands.append(f"adb shell input tap {x+w//2} {y+h//2}")
    return commands

app.run()
