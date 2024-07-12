## Overview
The `HardwareInterface` class provides methods to interact with various hardware components of an Autonomous Underwater Vehicle (AUV) such as ESCs (Electronic Speed Controllers), Battery Monitors, IMUs (Inertial Measurement Units), Temperature and Humidity sensors, Hydrophones, and Depth sensors. It also includes methods for posting and retrieving data from a server.

| Electrical Component          | I2C Address |
| ----------------------------- | ----------- |
| Nvidia AGX Orin               | 0x20        |
| ESC Motor Controller          | 0x08        |
| Humidity / Temperature Sensor | 0x27        |
| IMU Sensor                    | 0x69        |
| Battery Monitor               | 0x22        |
| Depth Sensor                  |             |
| Hydrophones                   | 0x23        |
## Installation
Before using this class, ensure you have the required libraries installed:
`pip install requests smbus2`
## Overview
This software consists of two main components:
1. **MPU6050**: A class that interfaces with the MPU-6050 sensor to read acceleration, gyroscope, and temperature data.
2. **HardwareInterface**: A class that interfaces with various hardware components such as ESCs, Battery Monitor, and environmental sensors. It also handles communication with a server to post and retrieve sensor data.
## Dependencies
The following libraries are required to run this software:
- `requests`: For making HTTP requests to fetch and send data.
- `smbus2`: For I2C communication.
- `time`: For handling time-related functions.
- `json`: For handling JSON data.
- `sys`: For accessing system-specific parameters and functions.
- `argparse`: For handling command-line arguments.
## MPU6050 Class
The `MPU6050` class interfaces with the MPU-6050 sensor to read acceleration, gyroscope, and temperature data. It uses I2C communication to interact with the sensor.
### MPU6050 Class Variables
```python
class MPU6050:
    # Constants
    GRAVITIY_MS2 = 9.80665

    # I2C Bus
    bus = smbus2.SMBus(7)

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    SELF_TEST_X = 0x0D
    SELF_TEST_Y = 0x0E
    SELF_TEST_Z = 0x0F
    SELF_TEST_A = 0x10

    ACCEL_XOUT0 = 0x3B
    ACCEL_XOUT1 = 0x3C
    ACCEL_YOUT0 = 0x3D
    ACCEL_YOUT1 = 0x3E
    ACCEL_ZOUT0 = 0x3F
    ACCEL_ZOUT1 = 0x40

    TEMP_OUT0 = 0x41
    TEMP_OUT1 = 0x42

    GYRO_XOUT0 = 0x43
    GYRO_XOUT1 = 0x44
    GYRO_YOUT0 = 0x45
    GYRO_YOUT1 = 0x46
    GYRO_ZOUT0 = 0x47
    GYRO_ZOUT1 = 0x48

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B
```
### MPU6050 Class Methods
#### Initialization
```python
def __init__(self, address):
    self.address = address
    # Wake up the MPU-6050 since it starts in sleep mode
    self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)
```
#### `read_i2c_word` Method
```python
def read_i2c_word(self, register):
    """
    Read two i2c registers and combine them.

    Args:
        register (int): The first register to read from.

    Returns:
        int: The combined read results.
    """
    high = self.bus.read_byte_data(self.address, register)
    low = self.bus.read_byte_data(self.address, register + 1)
    value = (high << 8) + low

    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value
```
#### `get_temp` Method
```python
def get_temp(self):
    """
    Reads the temperature from the onboard temperature sensor of the MPU-6050.

    Returns:
        float: The temperature in degrees Celsius.
    """
    raw_temp = self.read_i2c_word(self.TEMP_OUT0)
    actual_temp = (raw_temp / 340) + 36.53
    return actual_temp
```
#### `set_accel_range` Method
```python
def set_accel_range(self, accel_range):
    """
    Sets the range of the accelerometer.

    Args:
        accel_range (int): The range to set the accelerometer to. Using a pre-defined range is advised.
    """
    self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)
    self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)
```
#### `read_accel_range` Method
```python
def read_accel_range(self, raw=False):
    """
    Reads the range the accelerometer is set to.

    Args:
        raw (bool): If True, returns the raw value from the ACCEL_CONFIG register.

    Returns:
        int: The accelerometer range or -1 if an error occurred.
    """
    raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

    if raw:
        return raw_data
    else:
        if raw_data == self.ACCEL_RANGE_2G:
            return 2
        elif raw_data == self.ACCEL_RANGE_4G:
            return 4
        elif raw_data == self.ACCEL_RANGE_8G:
            return 8
        elif raw_data == self.ACCEL_RANGE_16G:
            return 16
        else:
            return -1
```
#### `get_accel_data` Method
```python
def get_accel_data(self, g=False):
    """
    Gets and returns the X, Y, and Z values from the accelerometer.

    Args:
        g (bool): If True, returns the data in g. If False, returns the data in m/s^2.

    Returns:
        dict: A dictionary with the measurement results.
    """
    x = self.read_i2c_word(self.ACCEL_XOUT0)
    y = self.read_i2c_word(self.ACCEL_YOUT0)
    z = self.read_i2c_word(self.ACCEL_ZOUT0)

    accel_scale_modifier = None
    accel_range = self.read_accel_range(True)

    if accel_range == self.ACCEL_RANGE_2G:
        accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
    elif accel_range == self.ACCEL_RANGE_4G:
        accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
    elif accel_range == self.ACCEL_RANGE_8G:
        accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
    elif accel_range == self.ACCEL_RANGE_16G:
        accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
    else:
        print("Unknown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
        accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

    x = x / accel_scale_modifier
    y = y / accel_scale_modifier
    z = z / accel_scale_modifier

    if g:
        return {'x': x, 'y': y, 'z': z}
    else:
        x = x * self.GRAVITIY_MS2
        y = y * self.GRAVITIY_MS2
        z = z * self.GRAVITIY_MS2
        return {'x': x, 'y': y, 'z': z}
```
#### `set_gyro_range` Method
```python
def set_gyro_range(self, gyro_range):
    """
    Sets the range of the gyroscope.

    Args:
        gyro_range (int): The range to set the gyroscope to. Using a pre-defined range is advised.
    """
    self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)
    self.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)
```
#### `read_gyro_range` Method
```python
def read_gyro_range(self, raw=False):
    """
    Reads the range the gyroscope is set to.

    Args:
        raw (bool): If True, returns the raw value from the GYRO_CONFIG register.

    Returns:
        int: The gyroscope range or -1 if an error occurred.
    """
    raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

    if raw:
        return raw_data
    else:
        if raw_data == self.GYRO_RANGE_250DEG:
            return 250
        elif raw_data == self.GYRO_RANGE_500DEG:
            return 500


        elif raw_data == self.GYRO_RANGE_1000DEG:
            return 1000
        elif raw_data == self.GYRO_RANGE_2000DEG:
            return 2000
        else:
            return -1
```
#### `get_gyro_data` Method
```python
def get_gyro_data(self):
    """
    Gets and returns the X, Y, and Z values from the gyroscope.

    Returns:
        dict: A dictionary with the measurement results.
    """
    x = self.read_i2c_word(self.GYRO_XOUT0)
    y = self.read_i2c_word(self.GYRO_YOUT0)
    z = self.read_i2c_word(self.GYRO_ZOUT0)

    gyro_scale_modifier = None
    gyro_range = self.read_gyro_range(True)

    if gyro_range == self.GYRO_RANGE_250DEG:
        gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
    elif gyro_range == self.GYRO_RANGE_500DEG:
        gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
    elif gyro_range == self.GYRO_RANGE_1000DEG:
        gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
    elif gyro_range == self.GYRO_RANGE_2000DEG:
        gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
    else:
        print("Unknown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
        gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

    x = x / gyro_scale_modifier
    y = y / gyro_scale_modifier
    z = z / gyro_scale_modifier

    return {'x': x, 'y': y, 'z': z}
```
## HardwareInterface Class
The `HardwareInterface` class interfaces with various hardware components such as ESCs, Battery Monitor, and environmental sensors. It also handles communication with a server to post and retrieve sensor data.
### Initialization
```python
class HardwareInterface:
    def __init__(self, args: list = sys.argv):
        self.bus = smbus2.SMBus(7)

        with open('./configs/hardware_interface.json') as f:
            self.config = json.load(f)
                    
        # if args.P:
        #     self.baseurl = self.config['poolUrl']
        # else:
        #     self.baseurl = self.config['labUrl']
        
        self.baseurl = "http://192.168.1.246:5000"
        
        try:
            self.IMU = MPU6050(0x69)
        except OSError as e:
            print("Error initializing the MPU6050:", str(e))
            self.IMU = None    
        self.TEMP_CALIBRATION_OFFSET = -5.75
```
### Methods
#### `write_ESCs` Method
```python
def write_ESCs(self, data=[127, 127, 127, 127, 127, 127, 127, 127]):
    """
    Writes data to the ESCs.

    Args:
        data (list): A list of 8 values to send to the ESCs.
    """
    device_address = 8
    try:
        self.bus.write_i2c_block_data(device_address, 0, data)
        # print("Message sent:", data)
    except Exception as e:
        print("Error writing I2C data:", str(e))
```
#### `write_BatteryMonitor` Method
```python
def write_BatteryMonitor(self, data=[127, 0, 0]):
    """
    Writes data to the Battery Monitor.

    Args:
        data (list): A list of 3 values to send to the Battery Monitor.
    """
    device_address = 0x22
    try:
        self.bus.write_i2c_block_data(device_address, 0, data)
        # print("Message sent:", data)
    except Exception as e:
        print("Error writing I2C data:", str(e))
```
#### `read_BatteryMonitor` Method
```python
def read_BatteryMonitor(self):
    """
    Reads data from the Battery Monitor.

    Returns:
        list: A list of 7 values read from the Battery Monitor.
    """
    device_address = 0x22
    try:
        data = self.bus.read_i2c_block_data(device_address, 0, 7)
        data[6] = bin(data[6])
        # print("Message received:", data)
        return data
    except Exception as e:
        print("Error reading I2C data:", str(e))
        return [0, 0, 0, 0, 0, 0, 0]
```
#### `read_i2c_word` Method
```python
def read_i2c_word(self, register):
    """
    Read two i2c registers and combine them.

    Args:
        register (int): The first register to read from.

    Returns:
        int: The combined read results.
    """
    high = self.bus.read_byte_data(self.address, register)
    low = self.bus.read_byte_data(self.address, register + 1)
    value = (high << 8) + low

    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value
```
#### `read_IMU` Method
```python
def read_IMU(self):
    """
    Reads data from the IMU (MPU-6050).

    Returns:
        dict: A dictionary with the accelerometer and gyroscope data.
    """
    accel_data = self.IMU.get_accel_data()
    gyro_data = self.IMU.get_gyro_data()

    data = {
        "accel_x": round(accel_data['x'], 2),
        "accel_y": round(accel_data['y'], 2),
        "accel_z": round(accel_data['z'], 2),
        "gyro_x": round(gyro_data['x'], 2),
        "gyro_y": round(gyro_data['y'], 2),
        "gyro_z": round(gyro_data['z'], 2)
    }
    return data
```
#### `convert_temp` Method
```python
def convert_temp(self, data):
    """
    Converts raw temperature data to degrees Celsius.

    Args:
        data (list): A list of two bytes containing the raw temperature data.

    Returns:
        float: The temperature in degrees Celsius.
    """
    value = ((data[0] << 8) | data[1]) & 0x3FFF
    temp = ((value * 165.0) / 16383.0) - 40.0 + self.TEMP_CALIBRATION_OFFSET
    # print(f"Raw Temp Value: {value}, Converted Temp: {temp}")  # Debugging statement
    return temp
```
#### `convert_humi` Method
```python
def convert_humi(self, data):
    """
    Converts raw humidity data to percentage.

    Args:
        data (list): A list of two bytes containing the raw humidity data.

    Returns:
        float: The humidity in percentage.
    """
    value = ((data[0] << 8) | data[1]) & 0x3FFF
    humi = (value / 16383.0) * 100
    # print(f"Raw Humi Value: {value}, Converted Humi: {humi}")  # Debugging statement
    return humi
```
#### `read_Temp_Humi` Method
```python
def read_Temp_Humi(self):
    """
    Reads temperature and humidity data from the sensor.

    Returns:
        dict: A dictionary with the temperature and humidity data.
    """
    device_address = 0x27

    self.bus.write_byte(device_address, 0x00)
    time.sleep(0.1)
    temp = self.bus.read_i2c_block_data(device_address, 0, 2)

    self.bus.write_byte(device_address, 0x01)
    time.sleep(0.1)
    humi = self.bus.read_i2c_block_data(device_address, 0, 2)

    temp = self.convert_temp(temp)
    humi = self.convert_humi(humi)

    data = {
        "temperature": temp,
        "humidity": humi
    }

    return data
```
#### `post_data` Method
```python
def post_data(self, data_type, data):
    """
    Posts data to the specified data type endpoint.

    Args:
        data_type (str): 'sensors', 'output', or 'input' indicating the type of data to post.
        data (dict): The data to be posted.

    Returns:
        str: Server response as a string.
    """
    response = requests.post(f"{self.baseurl}/{data_type}", json=data)
    if response.status_code == 201:
        return "Data added successfully"
    else:
        return f"Failed to add data, status code: {response.status_code}"
```
#### `get_data` Method
```python
def get_data(self, data_type):
    """
    Retrieves data from the specified data type endpoint.

    Args:
        data_type (str): 'sensors', 'output', or 'input' indicating the type of data to retrieve.

    Returns:
        dict: The retrieved data as a dictionary.
    """
    response = requests.get(f"{self.baseurl}/{data_type}")
    if response.status_code == 200:
        return response.json()


    else:
        print(f"Failed to get data, status code: {response.status_code}")
        return {}
```
#### `print_data` Method
```python
def print_data(self, data):
    """
    Prints the data in a human-readable format.

    Args:
        data (dict): The data to be printed.
    """
    s = ""
    for key, value in data.items():
        s += f"{key}: {value:.2f}     "
    s += "\r"
    print(s)
```
#### `run` Method
```python
def run(self):
    """
    Main loop to read sensor data, post it to the server, and retrieve output data to control hardware components.
    """
    delay = 0.01
    default_esc_value = 127  # Default value for ESCs when data is missing or there's an error

    time.sleep(10)  # Wait for the server to start

    while True:
        # battery_monitor_data = self.read_BatteryMonitor()
        IMU_data = self.read_IMU()
        # temp_humi_data = self.read_Temp_Humi()
        sensor_data = {
            "voltage1": 0,
            "voltage2": 0,
            "voltage3": 0,
            "current1": 0,
            "current2": 0,
            "current3": 0,
            "error": 0,
            "depth": 0,
            "X": IMU_data["accel_x"],
            "Y": IMU_data["accel_y"],
            "Z": IMU_data["accel_z"],
            "pitch": IMU_data["gyro_x"],
            "roll": IMU_data["gyro_y"],
            "yaw": IMU_data["gyro_z"],
            "temperature": 0,
            "orin_temp": 0,
            "humidity": 0,
            "heading": 0
        }

        # Post sensor data to the server
        self.post_data("sensors", sensor_data)

        # Get output data from the server
        output_data = self.get_data("output")

        # Debug 
        # print(output_data)
        # print(sensor_data)

        # Check if all required keys are present in the output data
        required_keys = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "Claw", "Torp1", "Torp2"]
        if all(key in output_data for key in required_keys):
            esc_values = [output_data[key] for key in required_keys[:8]]
            claw_torp_values = [output_data["Claw"], output_data["Torp1"], output_data["Torp2"]]
        else:
            # Log an error and use default values if some data is missing
            print("Error: Not all required output data keys received, using default values")
            print(output_data.keys())
            esc_values = [default_esc_value] * 8
            claw_torp_values = [0, 0, 0]

        # Send data to ESCs and battery monitor
        self.write_ESCs(esc_values)
        # self.write_BatteryMonitor(claw_torp_values)

        time.sleep(delay)
```
#### `test_run` Method
```python
def test_run(self, data):
    """
    Test method for manual input and IMU testing.

    Args:
        data (list): A list of initial values for testing.
    """
    delay = 0.01

    while True:
        try:
            if self.IMU is None:
                print("IMU not initialized")
                time.sleep(delay)
                print("Retrying...")
                self.IMU = MPU6050(0x69)
                time.sleep(delay)
                continue
            IMU_data = self.read_IMU()
            sensor_data = {
                "X": IMU_data["accel_x"],
                "Y": IMU_data["accel_y"],
                "Z": IMU_data["accel_z"],
                "pitch": IMU_data["gyro_x"],
                "roll": IMU_data["gyro_y"],
                "yaw": IMU_data["gyro_z"]
            }
            self.print_data(sensor_data)
            time.sleep(delay)
        except OSError as e:
            time.sleep(delay)
            continue
```
## Main Execution
The script can be run from the command line with optional arguments to use different configurations for the pool or lab environment.
```python
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--P", help="Use the pool IP address", action="store_true")
    args.add_argument("--L", help="Use the lab IP address", action="store_true")
    args = args.parse_args()
    HI = HardwareInterface(args=args)
    # HI.run()
    HI.test_run([127, 127, 127, 127, 127, 127, 127, 127])
```
