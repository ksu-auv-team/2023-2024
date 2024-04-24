#include <Servo.h>
#include <Wire.h>

// this device's i2c address
#define I2CADDRESS 0x22

// Output values to Orin
int currentActual1 = 1, voltageActual1 = 2;
int currentActual2 = 3, voltageActual2 = 4;
int currentActual3 = 5, voltageActual3 = 6;

// Input values from Orin
int armPWM = 127;
bool torpedo1 = false;
bool torpedo2 = false;

bool newData = false;
Servo Arm;

void setup() {
  Serial.begin(115200);
  Wire.begin(I2CADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  Arm.attach(2);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
  if (newData) {
    Arm.writeMicroseconds(map(armPWM, 0, 256, 1000, 2000));
    digitalWrite(5, torpedo1);
    digitalWrite(3, torpedo2);
    newData = false;  // Reset newData after handling
  }
  delay(100);
}

void requestEvent() {
  Wire.write((byte)voltageActual1);
  Wire.write((byte)currentActual1);
  Wire.write((byte)voltageActual2);
  Wire.write((byte)currentActual2);
  Wire.write((byte)voltageActual3);
  Wire.write((byte)currentActual3);
  Wire.write((byte)15);
}

void receiveEvent(int howMany) {
  if (Wire.available() == 4) {
    Wire.read();
    armPWM = Wire.read();           // Read second byte as armPWM
    torpedo1 = Wire.read();    // Read third byte as torpedo1
    torpedo2 = Wire.read();    // Read fourth byte as torpedo2
    Serial.print(armPWM);
    Serial.print(", ");
    Serial.print(torpedo1);
    Serial.print(", ");
    Serial.println(torpedo2);
    newData = true;
  }
}