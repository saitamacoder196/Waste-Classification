import os
import pdb
import numpy as np
import cv2
from pathlib import Path
import shutil

def move_images(source_directory, destination_directory):
  """
  Di chuyển tất cả hình ảnh từ thư mục nguồn sang thư mục đích.

  :param source_directory: Thư mục chứa hình ảnh nguồn.
  :param destination_directory: Thư mục đích.
  """
  for item in os.listdir(source_directory):
        shutil.move(os.path.join(source_directory, item), destination_directory)


# def load_images(directory):
#   """
#   Tải tất cả hình ảnh trong thư mục và các thư mục con của nó.

#   :param directory: Thư mục chứa hình ảnh.
#   :return: Danh sách các mảng NumPy chứa dữ liệu hình ảnh.
#   """
#   images = []
#   for root, dirs, files in os.walk(directory):
#     for file in files:
#       if file.endswith('.jpg') or file.endswith('.png'):
#         image = cv2.imread(os.path.join(root, file))
#         images.append(image)
#     for dir in dirs:
#       sub_dir = os.path.join(root, dir)
#       images.extend(load_images(sub_dir))
#   return images

# # def load_labels(file_path):
# #   """
# #   Tải các nhãn từ file.

# #   :param file_path: Đường dẫn đến file chứa nhãn.
# #   :return: Danh sách các nhãn.
# #   """
# #   labels = []
# #   with open(file_path, 'r') as f:
# #     for line in f:
# #       labels.append(line.strip())
# #   return labels

# def load_labels(directory):
#     """
#     Tải các nhãn từ thư mục hình ảnh.

#     :param directory: Đường dẫn đến thư mục chứa hình ảnh.
#     :return: Danh sách các nhãn.
#     """
#     labels = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.jpg') or file.endswith('.png'):
#                 # Thêm tên hình ảnh và nhãn vào danh sách
#                 labels.append({'image_name': file, 'label': Path(root).name})
#     return labels

def load_images_and_labels(directory):
    """
    Tải tất cả hình ảnh và nhãn từ thư mục và các thư mục con của nó.

    :param directory: Thư mục chứa hình ảnh.
    :return: Tuple chứa danh sách các mảng NumPy chứa dữ liệu hình ảnh và danh sách các nhãn.
    """
    images = []
    labels = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                image = cv2.imread(os.path.join(root, file))
                images.append(image)
                labels.append({'image_name': file, 'label': Path(root).name})
    return images, labels

def split_dataset(images, labels, train_ratio=0.8, validation_ratio=0.1):
  """
  Chia tập dữ liệu thành tập huấn luyện, tập xác thực và tập kiểm tra.

  :param images: Danh sách các mảng NumPy chứa dữ liệu hình ảnh.
  :param labels: Danh sách các nhãn.
  :param train_ratio: Tỷ lệ tập huấn luyện.
  :param validation_ratio: Tỷ lệ tập xác thực.
  :return: Tuple chứa (images_train, labels_train, images_validation, labels_validation, images_test, labels_test).
  """
  num_samples = len(images)

  # Chia tập dữ liệu
  train_size = int(num_samples * train_ratio)
  validation_size = int(num_samples * validation_ratio)
  test_size = num_samples - train_size - validation_size

  images_train = images[:train_size]
  labels_train = labels[:train_size]

  images_validation = images[train_size:train_size + validation_size]
  labels_validation = labels[train_size:train_size + validation_size]

  images_test = images[train_size + validation_size:]
  labels_test = labels[train_size + validation_size:]

  return images_train, labels_train, images_validation, labels_validation, images_test, labels_test

def clear_directory(directory):
  for filename in os.listdir(directory):
      file_path = os.path.join(directory, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print(f'Failed to delete {file_path}. Reason: {e}')

def save_images(images, labels, directory):
    clear_directory(directory)  # Xóa dữ liệu cũ
    for i, image in enumerate(images):
        label = labels[i]['label']
        image_name = labels[i]['image_name']
        
        # Create a subdirectory for this label, if it doesn't already exist
        label_directory = os.path.join(directory, label)
        os.makedirs(label_directory, exist_ok=True)
        
        # Save the image in the label subdirectory
        cv2.imwrite(os.path.join(label_directory, f'image_{i}_{image_name}.png'), image)

def split_dataset(images, labels, train_ratio=0.8, validation_ratio=0.1):
  num_samples = len(images)
  indices = np.arange(num_samples)
  np.random.shuffle(indices)

  train_size = int(num_samples * train_ratio)
  validation_size = int(num_samples * validation_ratio)

  train_indices = indices[:train_size]
  validation_indices = indices[train_size:train_size + validation_size]
  test_indices = indices[train_size + validation_size:]

  return train_indices, validation_indices, test_indices


def main():
  # Tải dữ liệu
  images_directory = 'data/images/processed'
  images, labels = load_images_and_labels(images_directory)
  # Chia tập dữ liệu và lưu chúng
  train_indices, validation_indices, test_indices = split_dataset(images, labels)

  # Lưu dữ liệu
  save_images([images[i] for i in train_indices], [labels[i] for i in train_indices], 'data/images/training')
  save_images([images[i] for i in validation_indices], [labels[i] for i in validation_indices], 'data/images/validation')
  save_images([images[i] for i in test_indices], [labels[i] for i in test_indices], 'data/images/test')

  # In thông tin
  print(f"Số lượng ảnh huấn luyện: {len(train_indices)}")
  print(f"Số lượng ảnh xác thực: {len(validation_indices)}")
  print(f"Số lượng ảnh kiểm tra: {len(test_indices)}")

if __name__ == "__main__":
    main()
