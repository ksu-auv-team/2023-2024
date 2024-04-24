#include <Wire.h>
#include <Servo.h>

#define masterAddress 0x20
#define ownAddress 0x08

uint8_t motorValues[3] = {127, 127, 127};
uint8_t sensorValues[6] = {0, 0, 0, 0, 0, 0};
int motorPins[3] = {2, 3, 4};
int maxPWM = 2000;
int minPWM = 1000;
int inMax = 256;
int inMin = 0;

Servo servos[3];

bool newData = 0;

int numOfServos = 3;
int numOfSensors = 6;

void setup() {
  Wire.begin(ownAddress);
  for (int i = 0; i < numOfServos; i++) {
    servos[i].attach(motorPins[i]);
  }
  Wire.beginTransmission(masterAddress);
  Wire.write(0x01);
  Wire.endTransmission();

  Wire.onReceive(receiveEvent);
}

void loop() {
  if (newData) {
    for (int i = 0; i < numOfServos; i++) {
      servos[i].writeMicroseconds(map(motorValues[i], inMin, inMax, minPWM, maxPWM));
    }
    if (Wire.available()) {
      Wire.beginTransmission(masterAddress);
      for (int i = 0; i < numOfSensors; i++) {
        Wire.write(sensorValues[i]);
      }
      Wire.endTransmission();
    }
    newData = 0;
  }
}

void receiveEvent() {
  int i = 0;
  while (Wire.available()) {
    if (i < 8) {
      motorValues[i] = Wire.read();
    } else {
      break;
    }
    i++;
  }
  newData = 1;
}

