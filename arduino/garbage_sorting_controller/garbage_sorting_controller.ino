#include <Wire.h>
#include "Waveshare_LCD1602.h"
#include <Servo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

Servo myservo;

#define GOC_DONG 0 // Góc đóng của servo
#define GOC_MO 110 // Góc mở của servo

int distance;
unsigned long previousMillis = 0;
unsigned long autoMillis = 0;

bool isAutoMode = true;
// Khai báo các đối tượng servo
Servo servo1;
Servo servo2;
Servo servo3;


void setup() {
    // Khởi tạo giao tiếp serial với tốc độ baud 9600
    Serial.begin(9600);
    Serial.setTimeout(1000); // Set the timeout for serial communication
    // servo attached to pin 10
    servo1.attach(10); // Giả sử servo1 gắn vào chân số 6
    servo2.attach(12); // Giả sử servo2 gắn vào chân số 7
    servo3.attach(13); // Giả sử servo3 gắn vào chân số 8
    // Khởi tạo
    lcd.begin(16, 2);  // LCD 16x2
    // Khởi tạo LCD
    // lcd.setCursor(0,0);
    // lcd.send_string("Waveshare");
    // lcd.setCursor(0,1);
    // lcd.send_string("Waiting...");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    if (input.startsWith("servo,")) {
      controlServo(input);
    } else if (input.startsWith("lcd,")) {
      displayLCD(input.substring(4)); // Loại bỏ phần "lcd," và hiển thị phần còn lại
    }
  }
}

void controlServo(String command) {
  int servoNumber = command.charAt(6) - '0'; // Lấy số thứ tự của servo từ chuỗi
  String state = command.substring(8); // Lấy trạng thái từ chuỗi

  int angle = state == "open" ? 110 : 0; // Đặt góc tùy thuộc vào trạng thái
  
  switch (servoNumber) {
    case 1:
      servo1.write(angle);
      break;
    case 2:
      servo2.write(angle);
      break;
    case 3:
      servo3.write(angle);
      break;
  }
}

void displayLCD(String message) {
  lcd.clear();
  lcd.print(message);
}
