import serial
import time

# Thay thế 'COMx' bằng cổng COM mà Arduino của bạn được kết nối
ser = serial.Serial('COM18', 9600, timeout=1)
time.sleep(2) # Đợi cho Arduino reset sau khi mở cổng
if ser.is_open == False:
        ser.open()

def send_command(command):
    time.sleep(2) # Đợi cho Arduino reset sau khi mở cổng
    ser.write(command.encode())

# Gửi lệnh điều khiển servo
def control_servo(servo_number, state):
    command = f"servo,{servo_number},{state}\n"
    send_command(command)

# Gửi chuỗi để hiển thị trên LCD
def display_on_lcd(message):
    command = f"lcd,{message}\n"
    send_command(command)

