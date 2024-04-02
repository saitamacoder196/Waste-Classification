from ultralytics import YOLO
import time
import streamlit as st
import cv2
import yaml
import settings
import threading

def sleep_and_clear_success():
    time.sleep(3)
    if 'recyclable_placeholder' in st.session_state:
        st.session_state['recyclable_placeholder'].empty()
    if 'non_recyclable_placeholder' in st.session_state:
        st.session_state['non_recyclable_placeholder'].empty()
    if 'hazardous_placeholder' in st.session_state:
        st.session_state['hazardous_placeholder'].empty()

def load_model(model_path):
    model = YOLO(model_path)
    return model

def classify_waste_type(detected_items):
    recyclable_items = set(detected_items) & set(settings.RECYCLABLE)
    non_recyclable_items = set(detected_items) & set(settings.NON_RECYCLABLE)
    hazardous_items = set(detected_items) & set(settings.HAZARDOUS)
    
    return recyclable_items, non_recyclable_items, hazardous_items

def remove_dash_from_class_name(class_name):
    return class_name.replace("_", " ")

def _translate_vietnamese_class_name(class_name):
    with open('vi.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    vi_class_name = data.get(class_name, class_name, "vi")
    vi_class_name_no_accent = data.get(class_name, class_name, "vi_no_accent")
    return vi_class_name, vi_class_name_no_accent


def _display_detected_frames(model, st_frame, image):
    image = cv2.resize(image, (640, int(640*(9/16))))
    
    if 'unique_classes' not in st.session_state:
        st.session_state['unique_classes'] = set()

    if 'recyclable_placeholder' not in st.session_state:
        st.session_state['recyclable_placeholder'] = st.sidebar.empty()
    if 'non_recyclable_placeholder' not in st.session_state:
        st.session_state['non_recyclable_placeholder'] = st.sidebar.empty()
    if 'hazardous_placeholder' not in st.session_state:
        st.session_state['hazardous_placeholder'] = st.sidebar.empty()

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
            st.session_state['non_recyclable_placeholder'].markdown('')
            st.session_state['hazardous_placeholder'].markdown('')
            detected_items.update(st.session_state['unique_classes'])

            recyclable_items, non_recyclable_items, hazardous_items = classify_waste_type(detected_items)

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
            if non_recyclable_items:
                # detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in non_recyclable_items)
                vietnamese_non_recyclable_items = [_translate_vietnamese_class_name(item) for item in non_recyclable_items]
                vietnamese_accents = [item[0] for item in vietnamese_non_recyclable_items]
                vietnamese_no_accents = [item[1] for item in vietnamese_non_recyclable_items]
                detected_items_str = "\n- ".join(vietnamese_accents)
                detected_items_str_no_accent = "\n- ".join(vietnamese_no_accents)

                # st.session_state['non_recyclable_placeholder'].warning(f"Non-Recyclable items:\n\n- {detected_items_str}")
                st.session_state['non_recyclable_placeholder'].markdown(
                    f"<div class='stNonRecyclable'>Non-Recyclable items:\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )
            if hazardous_items:
                # detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in hazardous_items)
                vietnamese_hazardous_items = [_translate_vietnamese_class_name(item) for item in hazardous_items]
                vietnamese_accents = [item[0] for item in vietnamese_hazardous_items]
                vietnamese_no_accents = [item[1] for item in vietnamese_hazardous_items]
                detected_items_str = "\n- ".join(vietnamese_accents)
                detected_items_str_no_accent = "\n- ".join(vietnamese_no_accents)
                
                # st.session_state['hazardous_placeholder'].error(f"Hazardous items:\n\n- {detected_items_str}")
                st.session_state['hazardous_placeholder'].markdown(
                    f"<div class='stHazardous'>Hazardous items:\n\n- {detected_items_str}</div>",
                    unsafe_allow_html=True
                )

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
    selected_camera = st.selectbox('Select a camera device:', camera_devices)
    if st.button('Detect Objects'):
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
            st.sidebar.error("Error loading video: " + str(e))
