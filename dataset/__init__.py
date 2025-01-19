from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # carrega um modelo YOLO pré-treinado
model.train(data='/content/drive/MyDrive/YOLO/dataset/data.yaml', epochs=80)  # seu dataset no Drive
git remote add origin https://github.com/kvxx99/yolo77.git
