from smbus2 import SMBus

# Define the Arduino addresses
addresses = {
    'arduino_1': 0x21,
    'arduino_2': 0x22,
    'arduino_3': 0x23,
    'arduino_4': 0x24
}

def send_data_to_arduino_1(bus):
    # Arduino at address 0x21 expects an uint8_t array of size 8
    data = [0, 1, 2, 3, 4, 5, 6, 7]  # Example data
    bus.write_i2c_block_data(addresses['arduino_1'], 0x00, data)

def send_and_receive_from_arduino_2(bus):
    # Arduino at address 0x22 expects an uint8_t array of size 2 and sends back size 8
    data = [0x10, 0x20]  # Example data
    bus.write_i2c_block_data(addresses['arduino_2'], 0x00, data)
    received_data = bus.read_i2c_block_data(addresses['arduino_2'], 0x00, 8)
    print("Data received from Arduino 2:", received_data)

def receive_from_arduino_3(bus):
    # Arduino at address 0x23 expects a get flag and sends back a uint8_t array of size 2
    # Assuming the get flag is just a write to trigger the response
    bus.write_byte(addresses['arduino_3'], 0x01)  # Sending a read trigger
    received_data = bus.read_i2c_block_data(addresses['arduino_3'], 0x00, 2)
    print("Data received from Arduino 3:", received_data)

def receive_from_arduino_4(bus):
    # Arduino at address 0x24 expects a get flag and sends back a uint8_t array of size 8
    bus.write_byte(addresses['arduino_4'], 0x01)  # Sending a read trigger
    received_data = bus.read_i2c_block_data(addresses['arduino_4'], 0x00, 8)
    print("Data received from Arduino 4:", received_data)

# Open I2C bus (e.g., bus 0)
with SMBus(0) as bus:
    send_data_to_arduino_1(bus)
    send_and_receive_from_arduino_2(bus)
    receive_from_arduino_3(bus)
    receive_from_arduino_4(bus)
