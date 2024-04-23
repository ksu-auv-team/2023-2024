#include <Wire.h>

#define masterAddress 0x20
#define ownAddress 0x23

bool dataRequest = 0;

// The first element represents angle 0-90
// The second element represents heading:
// - N = 0, 
// - NW = 1, 
// - W = 2, 
// - SW = 3,
// - S = 4,
// - SE = 5,
// - E = 6,
// - NE = 7 
uint8_t sensorData[2] = {0, 0};

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
    for (int i = 0; i < 2; i++) {
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