import os
import cv2
from ultralytics import YOLO

# Define the path to your test set
TEST_DIR = os.path.join('..', 'data', 'images', 'test', 'images')

# Define the path to your model
model_path = os.path.join('..', 'runs', 'detect', 'train3', 'weights', 'last.pt')

# Load the model
model = YOLO(model_path)

# Define the threshold
threshold = 0.5

# Loop over all images in the test set
for filename in os.listdir(TEST_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Define the path to the image
        img_path = os.path.join(TEST_DIR, filename)

        # Load the image
        img = cv2.imread(img_path)

        # Check if the image was loaded correctly
        if img is None:
            print(f"Failed to load image at {img_path}")
            continue

        print(f"Processing image at {img_path}")

        # Predict
        results = model(img)[0]

        # Loop over the results and check
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            print(f"Prediction: x1={x1}, y1={y1}, x2={x2}, y2={y2}, score={score}, class_id={class_id}")

            if score > threshold:
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(img, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        # Show the image
        cv2.imshow('Image', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()