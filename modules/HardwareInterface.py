import requests
import smbus2
import time
import json

bus=smbus2.SMBus(7)

def write_ESCs(data = [127, 127, 127, 127, 127, 127, 127, 127]):
    device_address = 0x21
    try:
        bus.write_i2c_block_data(device_address, 0, data)
        print("Message sent:", data)
    except Exception as e:
        print("Error writing I2C data:", str(e))

def write_BatteryMonitor(data = [127, 0, 0]):
    device_address = 0x22
    try:
        bus.write_i2c_block_data(device_address, 0, data)
        print("Message sent:", data)
    except Exception as e:
        print("Error writing I2C data:", str(e))

def read_ESCs():
    device_address = 0x21
    try:
        data = bus.read_i2c_block_data(device_address, 0, 8)
        print("Message received:", data)
    except Exception as e:
        print("Error reading I2C data:", str(e))

def read_BatteryMonitor():
    device_address = 0x22
    try:
        data = bus.read_i2c_block_data(device_address, 0, 7)
        data[6] = bin(data[6])
        print("Message received:", data)
    except Exception as e:
        print("Error reading I2C data:", str(e))

def read_IMU():
    device_address = 0x68
    try:
        data = bus.read_i2c_block_data(device_address, 0x3B, 14)
        print("Message received:", data)
    except Exception as e:
        print("Error reading I2C data:", str(e))

def read_Temp_Humi():
    device_address = 0x07
    try:
        bus.write_byte(device_address, 0x01)
        time.sleep(0.1)
        data = bus.read_i2c_block_data(device_address, 0x00, 4)
        print("Message received:", data)
    except Exception as e:
        print("Error reading I2C data:", str(e))

def read_Hydrophones():
    device_address = 0x06
    try:
        data = bus.read_i2c_block_data(device_address, 0, 8)
        print("Message received:", data)
    except Exception as e:
        print("Error reading I2C data:", str(e))

def read_Depth():
    device_address = 0x05
    try:
        data = bus.read_i2c_block_data(device_address, 0, 2)
        print("Message received:", data)
    except Exception as e:
        print("Error reading I2C data:", str(e))

if __name__ == '__main__':
    # write_ESCs([127, 127, 127, 127, 127, 127, 127, 127])
    # for i in range(0, 256):
    #     write_BatteryMonitor([i, 0, 0])
    read_BatteryMonitor()