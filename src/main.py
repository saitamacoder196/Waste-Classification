import os
from src.data_preprocessing.image_processing import preprocess_images
from src.data_preprocessing.video_processing import preprocess_videos
from src.models.classification_model import train_classification_model, classify_waste
from src.models.detection_model import train_detection_model, detect_littering_behavior

def main():
    # Tiền xử lý dữ liệu
    print("Tiền xử lý hình ảnh...")
    preprocess_images('data/images/raw/', 'data/images/processed/')

    print("Tiền xử lý video...")
    preprocess_videos('data/videos/raw/', 'data/videos/processed/')

    # Huấn luyện mô hình phân loại rác thải
    print("Huấn luyện mô hình phân loại rác thải...")
    train_classification_model('data/images/processed/', 'models/yolov6/')

    # Huấn luyện mô hình phát hiện hành vi vứt rác
    print("Huấn luyện mô hình phát hiện hành vi vứt rác...")
    train_detection_model('data/videos/processed/', 'models/yolov6/')

    # Phân loại rác thải sử dụng mô hình đã huấn luyện
    print("Phân loại rác thải...")
    classify_waste('data/images/test/', 'models/yolov6/')

    # Phát hiện hành vi vứt rác sử dụng mô hình đã huấn luyện
    print("Phát hiện hành vi vứt rác...")
    detect_littering_behavior('data/videos/test/', 'models/yolov6/')

if __name__ == "__main__":
    main()
