import matplotlib.pyplot as plt
import numpy as np

def plot_image(image):
    """
    Hiển thị hình ảnh.

    :param image: Mảng NumPy chứa dữ liệu hình ảnh.
    """
    plt.imshow(image)
    plt.show()

def plot_multiple_images(images, titles=None):
    """
    Hiển thị nhiều hình ảnh.

    :param images: Danh sách các mảng NumPy chứa dữ liệu hình ảnh.
    :param titles: Danh sách tiêu đề cho các hình ảnh (tùy chọn).
    """
    num_images = len(images)
    fig, axes = plt.subplots(1, num_images, figsize=(15, 5))

    for i in range(num_images):
        axes[i].imshow(images[i])
        if titles is not None:
            axes[i].set_title(titles[i])

    plt.show()

def visualize_predictions(image, predictions):
    """
    Hiển thị hình ảnh với các dự đoán.

    :param image: Mảng NumPy chứa dữ liệu hình ảnh.
    :param predictions: Danh sách các dự đoán.
    """
    plt.imshow(image)
    plt.axis('off')

    for pred in predictions:
        class_name = pred['class_name']
        confidence = pred['confidence']
        bbox = pred['bbox']

        plt.text(bbox[0], bbox[1], f'{class_name}: {confidence:.2f}', color='red', fontsize=10, backgroundcolor='white')
        plt.gca().add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2]-bbox[0], bbox[3]-bbox[1], fill=False, edgecolor='red', linewidth=2))

    plt.show()