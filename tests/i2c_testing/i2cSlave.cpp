/*Will setup each individual Arduino board programmed as a slave
in an I2C connection with raspberry pi*/

#include <Arduino.h>
#include <Wire.h>

void receiveEvent(int count);

void setup(){
    //Calls particular address for arduino, switch from 0x6 - 0x8 as needed for each board
    Wire.begin(0x08);
    //needed to proper event called each time data received through i2c
    Wire.onReceive(receiveEvent);

    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
}

void receiveEvent(int count){
    while(Wire.available()){
        char ard_Read = Wire.read();
        digitalWrite(LED_BUILTIN, ard_Read);
    }
}

void loop(){
    delay(1000);
}



