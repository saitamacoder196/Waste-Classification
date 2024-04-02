import torch
import torchvision.transforms as transforms
from PIL import Image

# Đường dẫn đến mô hình YOLOv6 đã được huấn luyện
MODEL_PATH = 'src/models/yolov6/yolov6_model.pth'

# Tải mô hình YOLOv6
model = torch.load(MODEL_PATH)
model.eval()

# Hàm phát hiện đối tượng
def detect_objects(image_path, model):
    # Tải và xử lý ảnh
    image = Image.open(image_path)
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    image = transform(image).unsqueeze(0)

    # Phát hiện đối tượng
    with torch.no_grad():
        predictions = model(image)

    # Xử lý và trả về kết quả
    return predictions

if __name__ == '__main__':
    image_path = 'data/images/test/your_test_image.jpg'
    predictions = detect_objects(image_path, model)
    # Xử lý kết quả dự đoán ở đây
