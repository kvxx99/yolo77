from ultralytics import YOLO

# Carregar o modelo base do YOLOv8
model = YOLO("yolov8n.pt")  # Use "yolov8s.pt" ou outros conforme necessário


# Treinar o modelo
model.train(
    data="/content/yolo77/dataset/data.yaml",
    epochs=50,
    batch=8,
    imgsz=2400,
    name="bot-detection",
    amp=True,
    save=True
)
