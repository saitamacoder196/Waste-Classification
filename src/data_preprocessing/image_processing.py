import os
import cv2
import numpy as np

def resize_image(image, target_size):
    """
    Resize một hình ảnh đến kích thước mong muốn.

    :param image: Hình ảnh cần resize.
    :param target_size: Kích thước đích.
    :return: Hình ảnh sau khi resize.
    """
    return cv2.resize(image, target_size)

def augment_image(image):
    """
    Tăng cường hình ảnh (ví dụ: xoay, phản chiếu).

    :param image: Hình ảnh cần tăng cường.
    :return: Hình ảnh sau khi tăng cường.
    """
    # Xoay hình ảnh
    image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    
    # Phản chiếu hình ảnh
    image_flipped = cv2.flip(image, 1)
    
    return image_rotated, image_flipped

def process_image(file_path, target_size=(224, 224)):
    """
    Tiền xử lý hình ảnh bao gồm resize và tăng cường.

    :param file_path: Đường dẫn đến file hình ảnh.
    :param target_size: Kích thước đích cho việc resize.
    :return: Hình ảnh sau khi tiền xử lý.
    """
    image = cv2.imread(file_path)
    if image is None:
        print(f"Cannot read image: {file_path}")
        return None, None
    image_resized = resize_image(image, target_size)
    image_augmented = augment_image(image_resized)
    return image_resized, image_augmented

def process_images_recursively(image_directory, processed_directory):
    for root, dirs, files in os.walk(image_directory):
        for filename in files:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                file_path = os.path.join(root, filename)
                process_and_save_image(file_path, image_directory, processed_directory)
        

def process_and_save_image(file_path, image_directory, processed_directory):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    image_resized, image_augmented = process_image(file_path)
    
    # Tạo đường dẫn mới trong thư mục xử lý
    processed_subdirectory = os.path.join(processed_directory, os.path.relpath(os.path.dirname(file_path), image_directory))
    os.makedirs(processed_subdirectory, exist_ok=True)

    # Lưu hình ảnh đã tiền xử lý
    filename = os.path.basename(file_path)
    cv2.imwrite(os.path.join(processed_subdirectory, 'resized_' + filename), image_resized)
    cv2.imwrite(os.path.join(processed_subdirectory, 'augmented_' + filename), image_augmented[0])
    cv2.imwrite(os.path.join(processed_subdirectory, 'augmented_flipped_' + filename), image_augmented[1])

def main():
    image_directory = 'data/images/raw'  # Thay thế bằng đường dẫn thực tế
    processed_directory = 'data/images/processed'  # Thay thế bằng đường dẫn lưu hình ảnh sau khi xử lý

    process_images_recursively(image_directory, processed_directory)



if __name__ == '__main__':
    main()
