#include <Wire.h>

#define BAUD 115200

#define PWM_CNT         8
#define ESC_BYTE_IN     PWM_CNT / 2

#define MASTER_ADDRESS  4
#define ESC_1_ADDRESS   8
#define ESC_2_ADDRESS   16

#define CONTROL_BUFF    4
#define SERIAL_BUFF     PWM_CNT * 32 * 2

#define CTRL_BYTE_SIZE  0
#define CTRL_ROBO_STATE 1
#define CTRL_SENSORS    2
#define CTRL_PWM_ENABLE 3

// Serial input buffers
byte CONTROL_FLAGS[CONTROL_BUFF];
byte PWM_DATA[SERIAL_BUFF];
// Indexing variables (stored for reuse)
int CONTROL_BUFF_PTR = 0;
int PWM_BUFF_PTR = 0;
// Send flag once all serial input is stored
bool SEND = false;

void setup() {
  // Settup serial and I2C
  Wire.begin(MASTER_ADDRESS);
  Wire.onReceive(onReceive);
  Serial.begin(BAUD);
}

void loop() {
  
  // TODO: Error handling, send info through serial (i.e. unable to connect, invalid format, failed request, timeout)

  // TODO: Ugly
  while(!SEND && Serial.available()) {
    // Parse serial input as control flags until control buffer is full
    if(CONTROL_BUFF_PTR < CONTROL_BUFF)
    {
      CONTROL_FLAGS[CONTROL_BUFF_PTR] = Serial.read();
      //Serial.write(CONTROL_FLAGS[CONTROL_BUFF_PTR]); // TEST
      CONTROL_BUFF_PTR++;
    }
    // First control flag parsed is the byte count of the following transmission
    // Until max size is achieved, all bytes are accumilated in the PWM buffer
    else if(PWM_BUFF_PTR < CONTROL_FLAGS[0] - CONTROL_BUFF && PWM_BUFF_PTR < ESC_BYTE_IN * 2)
    {
      PWM_DATA[PWM_BUFF_PTR] = Serial.read();
      //Serial.write(PWM_DATA[PWM_BUFF_PTR]); // TEST
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
    // Temporary test code
    Wire.beginTransmission(ESC_1_ADDRESS);    // Open PWM channel
    Wire.write(CONTROL_FLAGS[3] & 0x0F);    // Send first half of the PWM control flag
    for(; PWM_BUFF_PTR < ESC_BYTE_IN; PWM_BUFF_PTR++) {
      Wire.write(PWM_DATA[PWM_BUFF_PTR]);   // Send PWM data
    }
    Wire.endTransmission();

    PWM_BUFF_PTR = 0;
    
    if(CONTROL_FLAGS[2]) {
      // TODO: Get I2C charts for the sensors
    }

    SEND = false;
  }
}

void onReceive(int bytes) {
  // TODO: Revceive I2C sensor data here
}