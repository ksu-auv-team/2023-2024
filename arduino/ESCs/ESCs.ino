#include <Servo.h>
#include <Wire.h>

#define masterAddress 0x20
#define ownAddress 9

uint8_t motorValues[8];  // Holds the actual motor values
int motorPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
int maxPWM = 1800;
int minPWM = 1200;
int inMax = 256;
int inMin = 0;

Servo ESCs[8];

bool newData = false;

int numOfMotors = 9;

void setup() {
  Serial.begin(115200);
  Wire.begin(ownAddress);
  Wire.onReceive(receiveEvent);
  Serial.println("Setup complete, waiting for data...");
}

void loop() {
  if (newData) {
    Serial.print("Motor Values: ");
    for (int i = 0; i < numOfMotors; i++) {
      Serial.print(motorValues[i]);
      if (i < numOfMotors - 1) {
        Serial.print(", ");
      }
    }
    Serial.println();
    newData = false;
  }
}

void receiveEvent(int howMany) {
  Serial.print("Received bytes: ");
  Serial.println(howMany);

  if (howMany != numOfMotors) {
    // Log an error if the received data does not match the expected size
    Serial.println("Error: Received incorrect number of bytes.");
    while (Wire.available()) Wire.read(); // Clear the buffer to prepare for the next transmission
    return;
  }

  int i = 0;
  while (Wire.available() && i < howMany) {
    motorValues[i] = Wire.read();
    i++;
  }
  newData = true;
}

