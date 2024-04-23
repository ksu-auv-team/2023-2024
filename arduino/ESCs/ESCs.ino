#include <Servo.h>
#include <Wire.h>

#define masterAddress 0x20
#define ownAddress 0x21

uint8_t motorValues[8] = {127, 127, 127, 127, 127, 127, 127, 127};
int motorPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
int maxPWM = 1800;
int minPWM = 1200;
int inMax = 256;
int inMin = 0;

Servo ESCs[8];

bool newData = 0;

int numOfMotors = 8;

void setup() {
  Wire.begin(ownAddress);
  for (int i = 0; i < numOfMotors; i++) {
    ESCs[i].attach(motorPins[i]);
    ESCs[i].writeMicroseconds(1500);
    delay(5000);
  }
  Wire.beginTransmission(masterAddress);
  Wire.write(0x01);
  Wire.endTransmission();

  Wire.onReceive(receiveEvent);
}

void loop() {
  if (newData) {
    for (int i = 0; i < numOfMotors; i++) {
      ESCs[i].writeMicroseconds(map(motorValues[i], inMin, inMax, minPWM, maxPWM));
    }
    newData = 0;
  }
}

void receiveEvent(int howMany){
  if(Wire.available() && (howMany == numOfMotors)){
    for(int i = 0; i<numOfMotors; i++){
      motorValues[i]=Wire.read();
    }
    newData = 1;
  }
}