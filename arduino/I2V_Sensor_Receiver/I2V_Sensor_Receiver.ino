#include <Wire.h>

// 9600 - 115200

#define BAUD 9600

#define PWM_CNT         6
#define SUBSYSTEM_CNT   4
//#define CONTROLER_1_CNT 4
//#define CONTROLER_2_CNT 2

#define MASTER_ADDRESS  4
#define PWM_ADDRESS     8
#define SENSOR_ADDRESS  16

#define KILL_SWITCH     0b10000000
#define PWM_ENABLE      0b00000001
#define SENSOR_ENABLE   0b00000010
#define SENSOR_FETCH    0b00100000

// Range from 0-255 (can add more if needed)
byte[] SENSOR_DATA = {0, 16, 32, 64, 128, 255};

void setup() {
  Wire.begin(SENSOR_ADDRESS);    // Join line
  Wire.onRequest(onRequest);  // Link handlers
  Wire.onReceive(onReceive);
  Serial.begin(BAUD);         // Set serial BAUD
}

void loop() {}

void onReceive(int bytes) {
  Serial.write("RECIEVER {" + bytes + "} BYTES: ");

  byte flag = Wire.read(); // Enable / Disable flag
}

void onRequest() {
  Wire.beginTransmission(MASTER_ADDRESS);
  Wire.write(random(0, 254));
  Wire.endTransmission();
}