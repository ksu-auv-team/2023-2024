import smbus2
import time

bus=smbus2.SMBus(7)

def write_ESCs(data = [126, 126, 126, 126, 126, 126, 126, 126]):
    device_address = 0x09
    try:
        data = [120, 121, 122, 123, 124, 125, 126, 127]

        bus.write_i2c_block_data(device_address, 0, data)
        print("Message sent:", data)
    except Exception as e:
        print("Error writing I2C data:", str(e))

def write_BatteryMonitor(data = [126, 126, 126]):
    device_address = 0x08
    try:
        data = [120, 121, 122, 123, 124, 125, 126, 127]

        bus.write_i2c_block_data(device_address, 0, data)
        print("Message sent:", data)
    except Exception as e:
        print("Error writing I2C data:", str(e))

while True:
    write_ESCs()
    time.sleep(1)
