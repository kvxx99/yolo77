from ultralytics import YOLO

# Carregar o modelo base do YOLOv8
model = YOLO("yolov8n.pt")  # Use "yolov8s.pt" ou outros conforme necessário


# Treinar o modelo
model.train(
    data="dataset/data.yaml",
    epochs=50,
    batch=16,
    imgsz=640,
    name="bot-detection",
    save=True
)
