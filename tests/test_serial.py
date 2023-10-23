# Libraries 
import serial 
import time 
import random

# Arduino Serial Object
arduino = serial.Serial(port = 'COM4', baudrate = 115200, timeout = 0.1) 

arduino.flush()

FULL_ACTIVE = 0x00
CONTROL_ONLY = 0x01
CONTROLLED_SHUTDOWN = 0x02

SENSOR_DATA_END = bytearray(0xFF)

# FLAGS (first byte):
# - [0x01] PWM SEND
# - [0x02] Sensor Query
# - [0x04] State Change
# - [0x08] PWM Enable

# SENSOR_QUERY
# - [0x01] VITALS (check on hardware, send for debug)
# - [0x02] POSITION (gyro & acceleromiter [as fast as possible])
# - [0x04] HYDROPHONE (only at the end and much slower)
# - [0x08] CAMERA (30fps)

# R_STATE
# - [0x00] FULL ACTIVE
# - [0x01] CONTROL ONLY
# - [0x02] CONTROLLED SHUTDOWN

# SEND ORDER (IF APPLICABLE)
# - FLAGS
# - SENSOR_QUERY
# - R_STATE
# - PWM_ENABLE
# - PWM VALUES

# QUERY_RETURN (WIP)
# - [0x00] EMPTY (for when no sensor query is made)
# - [0x01-0x04] INT (not sure if we need multiple sizes or if/how python converts unsigned ints)
# - [0x08-0x0F] FLOAT/DOUBLE (same question as before)
# - [0x10] BOOL (for sending control flags)
# - [0x11] CHAR (for labling data, e.g. 't' = temp, 'd' = distance, etc.)
# - [0x12] CSTR (a string of chars ending with a null [0x00] byte)
# - [0xF8] ERR_CODE (an error code)
# - [0xFF] END (replace the 4 byte return code, these are all of a fixed length)

# BASIC SERIAL DATA TRANSFER:
# - Create bytearray() object
# - Populate with values:
#  > Convert numerical values to bytearray(num.to_bytes(size, "little")) and use .append(arr)
#  > Directly use .append(num) when integer value is less than 256
# - Send using .write(populated_byte_arr)

# Resolution of PWM for Arduino is only 256, cap to 250 for easy conversion (0 = 1000, 250 = 2000), reduces data transfer by ~40%
def get_pwm():
    return bytearray(random.randint(0,250).to_bytes(1,"little"))

def send_pwm():
    byte_data = bytearray()
    
    byte_data.append(0x0C) # Standard transfer - 4 byte control flag - 8 byte PWM data
    byte_data.append(0x00) # Normal robot state
    byte_data.append(0x00) # No sensor query
    byte_data.append(0xFF) # All motor enable
    
    for _ in range(8):
        for i in get_pwm():
            byte_data.append(i)

    arduino.write(byte_data) # Send over serial

    print(list(byte_data)) # Debug

    time.sleep(0.1)

    sensor_data = arduino.read_all() # TODO: End codes & start codes
    
    print(list(sensor_data)) # Debug

    return

while True: 
    send_pwm()
    time.sleep(5)