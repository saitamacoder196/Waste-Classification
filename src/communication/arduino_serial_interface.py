import serial
import time

# Thay thế 'COMx' bằng cổng COM mà Arduino của bạn được kết nối
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2) # Đợi cho Arduino reset sau khi mở cổng

def send_to_lcd(text):
    ser.write(text.encode()) # Gửi chuỗi văn bản tới Arduino qua cổng serial


# Gửi chuỗi văn bản
send_to_lcd("VO CHUOI")

def open_servo():
    ser.write("servo10_mo".encode()) # Gửi lệnh mở servo (1)
    time.sleep(2) # Đợi servo thực hiện hành động trước khi gửi lệnh tiếp theo

def close_servo():
    ser.write("servo10_dong".encode()) # Gửi lệnh đóng servo (0)
    time.sleep(2) # Đợi servo thực hiện hành động trước khi gửi lệnh tiếp theo

# servo10_mo
    
# open_servo() # Mở servo
close_servo() # Đóng servo


ser.close() # Đóng cổng serial khi hoàn tất
