import cv2
import os

def extract_frames(video_path, target_folder, frame_rate=5):
    """
    Trích xuất các frame từ video.

    :param video_path: Đường dẫn đến file video.
    :param target_folder: Thư mục để lưu các frame.
    :param frame_rate: Số frame cần trích xuất mỗi giây.
    """
    video = cv2.VideoCapture(video_path)
    count = 0
    success = True
    fps = int(video.get(cv2.CAP_PROP_FPS))

    while success:
        success, image = video.read()
        
        if count % (fps // frame_rate) == 0 and success:
            frame_name = f"frame_{count}.jpg"
            cv2.imwrite(os.path.join(target_folder, frame_name), image)

        count += 1

    video.release()

def process_videos(video_directory, target_directory, frame_rate=5):
    """
    Xử lý tất cả video trong một thư mục.

    :param video_directory: Thư mục chứa video.
    :param target_directory: Thư mục lưu các frame.
    :param frame_rate: Số frame cần trích xuất mỗi giây.
    """
    for filename in os.listdir(video_directory):
        if filename.endswith('.mp4'):
            video_path = os.path.join(video_directory, filename)
            target_folder = os.path.join(target_directory, filename.split('.')[0])
            
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            
            extract_frames(video_path, target_folder, frame_rate)

def main():
    video_directory = 'path/to/your/video/directory'  # Thay thế bằng đường dẫn thực tế
    target_directory = 'path/to/extracted/frames'    # Thay thế bằng đường dẫn lưu các frame

    process_videos(video_directory, target_directory)

if __name__ == '__main__':
    main()
