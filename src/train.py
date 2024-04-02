from ultralytics import YOLO

# Load a model
# Use the model
model = YOLO('yolov8n.yaml')
model = YOLO('yolov8n.pt')
path = 'config.yaml'
results = model.train(data=path, epochs=50)
results = model.val()
success = model.export(format='onnx')
