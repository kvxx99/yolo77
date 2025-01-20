from ultralytics import YOLO

# Carregar o modelo base do YOLOv8
model = YOLO("yolov8n.pt")  # Use "yolov8s.pt" ou outros conforme necessário


# Treinar o modelo
model.train(
    data="/dataset/data.yaml",
    epochs=80,
    batch=32,
    imgsz=2400,
    name="bot-detection",
    save=True
)
