import torch

def detect_objects(image):
    # Carregar o modelo YOLO
    model = torch.hub.load('content/yolo77/dataset/runs/detect/bot-detection/', 'custom', path='best.pt')
    results = model(image)

    # Extrair caixas delimitadoras e rótulos
    detections = []
    for *box, conf, cls in results.xyxy[0]:  # Coordenadas x1, y1, x2, y2, confiança e classe
        detections.append({
            'box': [int(box[0]), int(box[1]), int(box[2]), int(box[3])],
            'confidence': float(conf),
            'class': int(cls),
        })
    return detections
