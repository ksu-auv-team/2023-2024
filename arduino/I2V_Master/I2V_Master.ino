#include <Wire.h>

// BAUD RANGE: 9600 - 115200

#define BAUD 115200

#define PWM_CNT         8
#define ESC_BYTE_IN     PWM_CNT / 2 * 2

#define MASTER_ADDRESS  4
#define ESC_1_ADDRESS   8
#define ESC_2_ADDRESS   16

#define CONTROL_BUFF    4
#define SERIAL_BUFF     PWM_CNT * 32 * 2

#define CTRL_BYTE_SIZE  0
#define CTRL_ROBO_STATE 1
#define CTRL_SENSORS    2
#define CTRL_PWM_ENABLE 3

// Range from 0-255 (can add more if needed)
byte CONTROL_FLAGS[CONTROL_BUFF];
int CONTROL_BUFF_PTR = 0; // TODO: Use an actual pointer?
byte PWM_DATA[SERIAL_BUFF];
int PWM_BUFF_PTR = 0; // TODO: Use an actual pointer?
bool SEND = false;

void setup() {
  Wire.begin(MASTER_ADDRESS); // Join line
  Wire.onReceive(onReceive);
  Serial.begin(BAUD);         // Set serial BAUD
}

void loop() {
  
  // TODO: Error handling, send info through serial (i.e. unable to connect, invalid format, failed request, timeout)

  // TODO: Ugly
  while(!SEND && Serial.available()) {
    // Parse serial input as control flags until control buffer is full
    if(CONTROL_BUFF_PTR < CONTROL_BUFF)
    {
      CONTROL_FLAGS[CONTROL_BUFF_PTR] = Serial.read();
      Serial.write(CONTROL_FLAGS[CONTROL_BUFF_PTR]); // TEST
      CONTROL_BUFF_PTR++;
    }
    // First control flag parsed is the byte count of the following transmission
    // Until max size is achieved, all bytes are accumilated in the PWM buffer
    else if(PWM_BUFF_PTR < CONTROL_FLAGS[0] - CONTROL_BUFF && PWM_BUFF_PTR < ESC_BYTE_IN * 2)
    {
      PWM_DATA[PWM_BUFF_PTR] = Serial.read();
      Serial.write(PWM_DATA[PWM_BUFF_PTR]); // TEST
      PWM_BUFF_PTR++;

      // Once the transmission is considered over, reset pointers and raise send flag
      if(PWM_BUFF_PTR >= CONTROL_FLAGS[0] - CONTROL_BUFF) {
        PWM_BUFF_PTR = 0;
        CONTROL_BUFF_PTR = 0;
        SEND = true;
      }
    }
  }

  // Send data we read
  if(SEND) {

    Wire.beginTransmission(ESC_1_ADDRESS);    // Open PWM channel
    Wire.write(CONTROL_FLAGS[3] & 0x0F);    // Send first half of the PWM control flag
    for(; PWM_BUFF_PTR < ESC_BYTE_IN; CONTROL_BUFF_PTR++) {
      Wire.write(PWM_DATA[PWM_BUFF_PTR]);   // Send PWM data
    }
    Wire.endTransmission();

    if(CONTROL_FLAGS[2]) {
      // TODO: Get I2C charts for the sensors
    }

    SEND = false;
  }
}

void onReceive(int bytes) {
  // TODO: Revceive I2C sensor data here
}