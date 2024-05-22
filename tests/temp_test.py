import smbus2
import time

# I2C address of the HIH61xx sensor
temp_address = 0x27
# Initialize the I2C bus
bus = smbus2.SMBus(1)

# Calibration offset for temperature (sensor reading - actual temperature)
TEMP_CALIBRATION_OFFSET = -5.75

def read_temp():
    """
    Reads the temperature data from the sensor.

    Writes a command to the sensor to read the temperature, waits for a short
    period, and then reads two bytes of data from the sensor.

    Returns:
        list: A list of two bytes read from the sensor.
    """
    bus.write_byte(temp_address, 0x00)
    time.sleep(0.1)
    data = bus.read_i2c_block_data(temp_address, 0, 2)
    return data

def convert_temp(data):
    """
    Converts raw temperature data to degrees Celsius.

    Args:
        data (list): A list of two bytes containing the raw temperature data.

    Returns:
        float: The temperature in degrees Celsius.
    """
    # Combine the two bytes and ignore the status bits
    value = ((data[0] << 8) | data[1]) & 0x3FFF
    # Convert to Celsius
    temp = ((value * 165.0) / 16383.0) - 40.0 + TEMP_CALIBRATION_OFFSET
    print(f"Raw Temp Value: {value}, Converted Temp: {temp}")  # Debugging statement
    return temp

def read_humi():
    """
    Reads the humidity data from the sensor.

    Writes a command to the sensor to read the humidity, waits for a short
    period, and then reads two bytes of data from the sensor.

    Returns:
        list: A list of two bytes read from the sensor.
    """
    bus.write_byte(temp_address, 0x01)
    time.sleep(0.1)
    data = bus.read_i2c_block_data(temp_address, 0, 2)
    return data

def convert_humi(data):
    """
    Converts raw humidity data to percentage.

    Args:
        data (list): A list of two bytes containing the raw humidity data.

    Returns:
        float: The humidity in percentage.
    """
    # Combine the two bytes and ignore the status bits
    value = ((data[0] << 8) | data[1]) & 0x3FFF
    # Convert to percentage
    humi = (value / 16383.0) * 100
    print(f"Raw Humi Value: {value}, Converted Humi: {humi}")  # Debugging statement
    return humi

def main():
    """
    Main function to continuously read and print temperature and humidity data.

    Reads the temperature and humidity data from the sensor, converts the data
    to human-readable format, and prints it to the console every second.
    """
    while True:
        temp_data = read_temp()
        humi_data = read_humi()
        temp = convert_temp(temp_data)
        humi = convert_humi(humi_data)
        print(f"Raw Temp Data: {temp_data} | Raw Humi Data: {humi_data} | Temperature: {round(temp, 2)}°C | Humidity: {round(humi, 2)}%")
        time.sleep(1)

if __name__ == "__main__":
    main()
