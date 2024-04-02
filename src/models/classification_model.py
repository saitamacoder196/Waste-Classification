import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import BatchNormalization

def build_resnet_model(input_shape, num_classes):
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Đóng băng các lớp cơ sở

    x = Flatten()(base_model.output)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

def build_vgg_model(input_shape, num_classes):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False

    x = Flatten()(base_model.output)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

def build_custom_vgg_model(input_shape, num_classes):
    # Tải mô hình VGG16 đã được đào tạo trước, không bao gồm các lớp đầu ra
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Đóng băng các lớp cơ sở

    # Tùy chỉnh các lớp bổ sung
    x = Flatten()(base_model.output)
    x = Dense(1024, activation='relu')(x)
    x = BatchNormalization()(x)  # Thêm lớp Batch Normalization
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu')(x)  # Thêm một lớp Dense với 512 nơ-ron
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    # Lớp đầu ra
    predictions = Dense(num_classes, activation='softmax')(x)

    # Tạo mô hình mới
    model = Model(inputs=base_model.input, outputs=predictions)

    # Biên dịch mô hình
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model

def train_classification_model(model_type, train_data_dir, validation_data_dir, model_save_path, input_shape, num_classes):
    # Xác định mô hình dựa trên model_type
    if model_type == 'resnet':
        model = build_resnet_model(input_shape, num_classes)
    elif model_type == 'vgg':
        model = build_vgg_model(input_shape, num_classes)
    elif model_type == 'custom_vgg':
        model = build_custom_vgg_model(input_shape, num_classes)
    else:
        raise ValueError('Invalid model type. Choose from "resnet", "vgg", or "custom_vgg".')

    # Cấu hình tiền xử lý dữ liệu
    train_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical')

    validation_datagen = ImageDataGenerator(rescale=1./255)
    validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical')
    
    # Biên dịch mô hình
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    # Huấn luyện mô hình
    model.fit(
        train_generator,
        epochs=10,
        steps_per_epoch=100,
        validation_data=validation_generator,
        validation_steps=50)

    # Lưu mô hình
    model.save(model_save_path)

if __name__ == "__main__":
    input_shape = (150, 150, 3)
    num_classes = 2  # Ví dụ: 2 lớp
    model_type = 'vgg'  # Chọn từ 'resnet', 'vgg', 'custom_vgg'
    train_data_dir = 'data/images/training/'
    validation_data_dir = 'data/images/validation/'
    model_save_path = 'src/models/classification_model/saved_model.h5'

    train_classification_model(model_type, train_data_dir, validation_data_dir, model_save_path, input_shape, num_classes)
