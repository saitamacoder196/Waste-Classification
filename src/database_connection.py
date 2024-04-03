import os
from dotenv import load_dotenv
import psycopg2

# Load giá trị từ file .env
load_dotenv()

# Lấy thông tin kết nối từ các biến môi trường
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Thiết lập kết nối
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


# Tạo một cursor object để thực hiện các truy vấn SQL
# cur = conn.cursor()

# Đóng kết nối
# cur.close()
# conn.close()

