from pathlib import Path
import streamlit as st
import helper
import settings
import threading

st.set_page_config(
    page_title="Phân loại rác thông minh",
)

st.sidebar.title("Detect Console")

model_path = Path(settings.DETECTION_MODEL)

st.title("Hệ thống phân loại rác thông minh")
st.write("Bắt đầu phát hiện các vật thể trong luồng webcam bằng cách nhấn nút bên dưới. Để dừng việc phát hiện, hãy nhấn nút dừng ở góc trên bên phải của luồng webcam.")
st.markdown(
"""
<style>
    .stRecyclable {
        background-color: rgba(233,192,78,255);
        padding: 1rem 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        margin-top: 0 !important;
        font-size:18px !important;
    }
    .stNonRecyclable {
        background-color: rgba(94,128,173,255);
        padding: 1rem 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        margin-top: 0 !important;
        font-size:18px !important;
    }
    .stHazardous {
        background-color: rgba(194,84,85,255);
        padding: 1rem 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        margin-top: 0 !important;
        font-size:18px !important;
    }

</style>
""",
unsafe_allow_html=True
)

try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Không thể tải model. Kiểm tra đường dẫn đã chỉ định: {model_path}")
    st.error(ex)

helper.play_webcam(model)
t = threading.Thread(target=helper.check_servo_status)
t.start()
st.sidebar.markdown("Đây là một demo của mô hình phân loại rác.", unsafe_allow_html=True)

