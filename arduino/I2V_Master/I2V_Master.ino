#include <Wire.h>

// BAUD RANGE: 9600 - 115200

#define BAUD 115200

#define PWM_CNT         6
#define SUBSYSTEM_CNT   4

#define MASTER_ADDRESS  4
#define PWM_ADDRESS     8
#define SENSOR_ADDRESS  16

#define KILL_SWITCH     0b10000000
#define PWM_ENABLE      0b00000001
#define SENSOR_ENABLE   0b00000010
#define SENSOR_FETCH    0b00100000

// Range from 0-255 (can add more if needed)
byte PWM_DATA[6] = {0, 16, 32, 64, 128, 255};
const byte CONTROL_FLAGS = PWM_ENABLE | SENSOR_ENABLE;

void setup() {
  Wire.begin(MASTER_ADDRESS); // Join line
  Wire.onRequest(onRequest);  // Link handlers
  Wire.onReceive(onReceive);
  Serial.begin(BAUD);         // Set serial BAUD
}

void loop() {
  
  // TODO: Serial interface
  // TODO: Handle sensor fetch request
  // TODO: Error handling, send info through serial (i.e. unable to connect, invalid format, failed request, timeout)

  // int in_cnt = Serial.available(); 
	// x = Serial.readString().toInt(); 
	// Serial.print(x + 1);

  Serial.write("MASTER: BEGIN PWM TRANSMISSION\n");
  Wire.beginTransmission(PWM_ADDRESS);    // Open PWM channel
  Wire.write(PWM_DATA, PWM_CNT);          // Send PWM data
  Wire.write(CONTROL_FLAGS & PWM_ENABLE); // Send control flag
  Wire.endTransmission();
  Serial.write("MASTER: END PWM TRANSMISSION\n");

  delay(5000);
}

void onReceive(int bytes) {
  
}

void onRequest() {

}