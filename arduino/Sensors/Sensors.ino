#include <Wire.h>

#define masterAddress 0x20
#define ownAddress 0x24

bool dataRequest = 0;

uint8_t sensorData[8] = {0, 0, 0, 0, 0, 0, 0, 0};

void setup() {
  Wire.begin(ownAddress);
  Wire.beginTransmission(masterAddress);
  Wire.write(0x01);
  Wire.endTransmission();
  Wire.onReceive(receiveEvent);
}

void loop() {
  if (dataRequest) {
    Wire.beginTransmission(masterAddress);
    for (int i = 0; i < 8; i++) {
      Wire.write(sensorData[i]);
    }
    Wire.endTransmission();
  }
}

void receiveEvent() {
  if (Wire.available()) {
    dataRequest = 1;
  }
}