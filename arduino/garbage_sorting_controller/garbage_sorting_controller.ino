#include <Wire.h>
#include "Waveshare_LCD1602.h"
#include <Servo.h>

#define GOC_DONG 0 // Góc đóng của servo
#define GOC_MO 110 // Góc mở của servo

Waveshare_LCD1602 lcd(16, 2); // 16 characters and 2 lines of show

Servo servo1;
Servo servo2;
Servo servo3;

void setup() {
    // initialize lcd
    lcd.init();
    lcd.setCursor(0, 0);
    lcd.send_string("Waveshare");
    lcd.setCursor(0, 1);
    lcd.send_string("Waiting...");

    // Khởi tạo giao tiếp serial với tốc độ baud 9600
    Serial.begin(9600);
    // Serial.setTimeout(1000);

    // Gắn servo vào các chân
    servo1.attach(9);
    servo2.attach(10);
    servo3.attach(11);

    // Đóng các giấy ban đầu
    servo1.write(GOC_DONG);
    servo2.write(GOC_DONG);
    servo3.write(GOC_DONG);
}

void loop() {
    unsigned long currentMillis = millis();

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
    int angle = state == "open" ? GOC_MO : GOC_DONG; // Đặt góc tùy thuộc vào trạng thái

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
    lcd.send_string(message.c_str());
}