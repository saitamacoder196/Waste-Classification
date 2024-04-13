import os
from ultralytics import YOLO
import time
import streamlit as st
import cv2
import yaml
# from communication.arduino_serial_interface import control_servo, display_on_lcd
from communication.arduino_serial_interface import control_servo, display_on_lcd, send_command
import settings
import threading
from database_connection import conn
from PIL import Image, ImageDraw

last_open_time = [0, 0, 0]

def sleep_and_clear_success():
    time.sleep(3)
    if 'recyclable_placeholder' in st.session_state:
        st.session_state['recyclable_placeholder'].empty()
    if 'inorganic_placeholder' in st.session_state:
        st.session_state['inorganic_placeholder'].empty()
    if 'organic_placeholder' in st.session_state:
        st.session_state['organic_placeholder'].empty()
    

def load_model(model_path):
    model = YOLO(model_path)
    return model

def classify_waste_type(detected_items):
    recyclable_items = set(detected_items) & set(settings.RECYCLABLE_WASTE)
    inorganic_items = set(detected_items) & set(settings.INORGANIC_WASTE)
    organic_items = set(detected_items) & set(settings.ORGANIC_WASTE)
    return recyclable_items, inorganic_items, organic_items

def remove_dash_from_class_name(class_name):
    return class_name.replace("_", " ")

def _translate_vietnamese_class_name(class_name):
    with open('vi.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    vi_class_name = data.get(class_name,{}).get("vi", remove_dash_from_class_name(class_name))
    vi_class_name_no_accent = data.get(class_name,{}).get("vi_no_accent", remove_dash_from_class_name(class_name))

    return vi_class_name, vi_class_name_no_accent

def display_images_from_database():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, image_path, top_left_x, top_left_y, bottom_right_x, bottom_right_y, label, timestamp, is_correct FROM detected_images ORDER BY timestamp DESC")
        detected_images = cur.fetchall()
        st.markdown("""
            <style>
                .btn-green { background-color: #008000; color: white; }
                .btn-red { background-color: #FF0000; color: white; }
            </style>
        """, unsafe_allow_html=True)
        
        for (id, image_path, top_left_x, top_left_y, bottom_right_x, bottom_right_y, label, timestamp, is_correct) in detected_images:
            st.sidebar.markdown(f"### {label}")
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            draw.rectangle(((top_left_x, top_left_y), (bottom_right_x, bottom_right_y)), outline="green", width=3)
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            st.sidebar.image(image, caption=timestamp_str, use_column_width=True)

            if is_correct == True:
                st.sidebar.markdown(f'<button class="btn-green" id="yes-{id}" disabled>Đúng</button>', unsafe_allow_html=True)
            elif is_correct == False:
                st.sidebar.markdown(f'<button class="btn-red" id="no-{id}" disabled>Sai</button>', unsafe_allow_html=True)
            else:
                if st.sidebar.markdown(f'<button class="btn-green" id="yes-{id}" disabled>Đúng</button>', unsafe_allow_html=True):
                    cur.execute(f"UPDATE detected_images SET is_correct = True WHERE id = {id}")
                    conn.commit()
                if st.sidebar.markdown(f'<button class="btn-red" id="no-{id}" disabled>Sai</button>', unsafe_allow_html=True):
                    cur.execute(f"UPDATE detected_images SET is_correct = False WHERE id = {id}")
                    conn.commit()

    except Exception as e:
        st.write(f"An error occurred: {e}")
        conn.rollback()

def save_detected_image(cur, image_path, top_left_x, top_left_y, bottom_right_x, bottom_right_y, label):
    # Tạo truy vấn SQL
    query = """
    INSERT INTO detected_images (image_path, top_left_x, top_left_y, bottom_right_x, bottom_right_y, label, is_correct, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, NULL, CURRENT_TIMESTAMP)
    """
    # Thực hiện truy vấn
    cur.execute(query, (image_path, top_left_x, top_left_y, bottom_right_x, bottom_right_y, label))
    
    
def load_sidebar():
    pass
    # st.sidebar.empty()
    # st.sidebar.title("Detected Images")
    # if 'organic_placeholder' in st.session_state:
    #     st.sidebar.markdown(st.session_state['organic_placeholder'])
    # if 'inorganic_placeholder' in st.session_state:
    #     st.sidebar.markdown(st.session_state['inorganic_placeholder'])
    # if 'recyclable_placeholder' in st.session_state:
    #     st.sidebar.markdown(st.session_state['recyclable_placeholder'])
    # st.sidebar.title("Detected Images")
    # display_images_from_database()

# Hàm lưu trữ hình ảnh vào thư mục
def save_image(result, file_name):
    folder_path = 'detected/images'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    cv2.imwrite(file_path, result.orig_img)

    cur = conn.cursor()
    bounding_boxes = result.boxes.xyxy.tolist()
    name = result.names[int(result.boxes.cls[0])]
    vi_name, vi_name_no_accent = _translate_vietnamese_class_name(name)
    save_detected_image(cur, file_path, bounding_boxes[0][0], bounding_boxes[0][1], bounding_boxes[0][2], bounding_boxes[0][3], vi_name)
    conn.commit()
    load_sidebar()
    return file_path

def check_servo_status():
    global last_open_time
    while True:
        for i in range(3):
            if (last_open_time[i] > 0) and (time.time() - last_open_time[i] > 2):
                last_open_time[i] = 0
                control_servo(i + 1, 'close')
                send_command("")
        time.sleep(1)
        

def _display_detected_frames(model, st_frame, image):

    image = cv2.resize(image, (640, int(640*(9/16))))
    
    if 'unique_classes' not in st.session_state:
        st.session_state['unique_classes'] = set()

    if 'recyclable_placeholder' not in st.session_state:
        st.session_state['recyclable_placeholder'] = st.sidebar.empty()
    if 'inorganic_placeholder' not in st.session_state:
        st.session_state['inorganic_placeholder'] = st.sidebar.empty()
    if 'organic_placeholder' not in st.session_state:
        st.session_state['organic_placeholder'] = st.sidebar.empty()

    if 'last_detection_time' not in st.session_state:
        st.session_state['last_detection_time'] = 0

    # res = model.track(image, conf=0.6, persist=True, tracker='bytetrack.yaml')
    res = model.predict(image, conf=0.8)
    names = model.names
    detected_items = set()

    for result in res:
        new_classes = set([names[int(c)] for c in result.boxes.cls])
        if new_classes != st.session_state['unique_classes']:
            st.session_state['unique_classes'] = new_classes
            st.session_state['recyclable_placeholder'].markdown('')
            st.session_state['inorganic_placeholder'].markdown('')
            st.session_state['organic_placeholder'].markdown('')
            detected_items.update(st.session_state['unique_classes'])

            recyclable_items, inorganic_items, organic_items = classify_waste_type(detected_items)
            file_name = f"{time.time()}.jpg"  # Tên tệp có thể được tùy chỉnh theo nhu cầu
            if recyclable_items:
                # detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in recyclable_items)
                vietnamese_recyclable_items = [_translate_vietnamese_class_name(item) for item in recyclable_items]
                vietnamese_accents = [item[0] for item in vietnamese_recyclable_items]
                vietnamese_no_accents = [item[1] for item in vietnamese_recyclable_items]
                detected_items_str = "\n- ".join(vietnamese_accents)
                detected_items_str_no_accent = "\n- ".join(vietnamese_no_accents)
                # st.session_state['recyclable_placeholder'].info(f"Recyclable items:\n\n- {detected_items_str}")
                st.session_state['recyclable_placeholder'].markdown(
                    f"<div class='stRecyclable'>Recyclable items:\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
                save_image(result, file_name)
                control_servo(1, 'open')  # Mở servo số 1
                last_open_time[0] = time.time()
                display_on_lcd(detected_items_str_no_accent)
            elif inorganic_items:
                # detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in inorganic_items)
                vietnamese_inorganic_items = [_translate_vietnamese_class_name(item) for item in inorganic_items]
                vietnamese_accents = [item[0] for item in vietnamese_inorganic_items]
                vietnamese_no_accents = [item[1] for item in vietnamese_inorganic_items]
                detected_items_str = "\n- ".join(vietnamese_accents)
                detected_items_str_no_accent = "\n- ".join(vietnamese_no_accents)

                # st.session_state['inorganic_placeholder'].warning(f"Non-Recyclable items:\n\n- {detected_items_str}")
                st.session_state['inorganic_placeholder'].markdown(
                    f"<div class='stNonRecyclable'>Non-Recyclable items:\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
                save_image(result, file_name)
                control_servo(2, 'open')  # Mở servo số 1
                last_open_time[1] = time.time()
                display_on_lcd(detected_items_str_no_accent)
    # 
            elif organic_items:
                # detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in organic_items)
                vietnamese_organic_items = [_translate_vietnamese_class_name(item) for item in organic_items]
                vietnamese_accents = [item[0] for item in vietnamese_organic_items]
                vietnamese_no_accents = [item[1] for item in vietnamese_organic_items]
                detected_items_str = "\n- ".join(vietnamese_accents)
                detected_items_str_no_accent = "\n- ".join(vietnamese_no_accents)
                
                # st.session_state['organic_placeholder'].error(f"Hazardous items:\n\n- {detected_items_str}")
                st.session_state['organic_placeholder'].markdown(
                    f"<div class='stHazardous'>Hazardous items:\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
                
                save_image(result, file_name)
                control_servo(3, 'open')  # Mở servo số 1
                last_open_time[2] = time.time()
                display_on_lcd(detected_items_str_no_accent)
            threading.Thread(target=sleep_and_clear_success).start()
            st.session_state['last_detection_time'] = time.time()

    res_plotted = res[0].plot()
    st_frame.image(res_plotted, channels="BGR")

# Get the list of available camera devices.
def get_camera_devices():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(int(index))  # Ensure 'index' is an integer
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

# Now you can use `selected_camera` as the index for `cv2.VideoCapture`.
def play_webcam(model):
    camera_devices = get_camera_devices()
    selected_camera = st.selectbox('Chọn thiết bị camera:', camera_devices)
    # load_sidebar()
    if st.button('Bắt đầu phát hiện'):
        try:
            vid_cap = cv2.VideoCapture(selected_camera)
            st_frame = st.empty()
            frame_count = 0  # Biến đếm frames
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                frame_count += 1  # Tăng biến đếm frames
                if frame_count % 2 == 0:  # Chỉ xử lý mỗi 2 frames
                    if success:
                        _display_detected_frames(model, st_frame, image)
                    else:
                        vid_cap.release()
                        break
        except Exception as e:
            st.sidebar.error("Lôi tải video: " + str(e))
