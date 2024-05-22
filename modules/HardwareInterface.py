import requests
import smbus2
import time
import json

class MPU6050:

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    bus = smbus2.SMBus(1)

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

    def __init__(self, address):
        self.address = address

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)

    # I2C communication methods

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.

        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # MPU-6050 Methods

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.

        Returns the temperature in degrees Celcius.
        """
        # Get the raw data
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340) + 36.53

        # Return the temperature
        return actual_temp

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer to range.

        accel_range -- the range to set the accelerometer to. Using a
        pre-defined range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw = False):
        """Reads the range the accelerometer is set to.

        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        # Get the raw value
        raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
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

    def get_accel_data(self, g = False):
        """Gets and returns the X, Y and Z values from the accelerometer.

        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        # Read the data from the MPU-6050
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
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * self.GRAVITIY_MS2
            y = y * self.GRAVITIY_MS2
            z = z * self.GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}

    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope to range.

        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw = False):
        """Reads the range the gyroscope is set to.

        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        # Get the raw value
        raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
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

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.

        Returns the read values in a dictionary.
        """
        # Read the raw data from the MPU-6050
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
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

class HardwareInterface:
    def __init__(self):
        self.bus = smbus2.SMBus(7)

        with open('./configs/hardware_interface.json') as f:
            self.config = json.load(f)

        self.base_url = self.config["baseUrl"]
        
        self.IMU = MPU6050(0x69)      
        
        self.TEMP_CALIBRATION_OFFSET = -5.75

    def write_ESCs(self, data = [127, 127, 127, 127, 127, 127, 127, 127]):
        device_address = 8
        try:
            self.bus.write_i2c_block_data(device_address, 0, data)
            # print("Message sent:", data)
        except Exception as e:
            print("Error writing I2C data:", str(e))

    def write_BatteryMonitor(self, data = [127, 0, 0]):
        device_address = 0x22
        try:
            self.bus.write_i2c_block_data(device_address, 0, data)
            # print("Message sent:", data)
        except Exception as e:
            print("Error writing I2C data:", str(e))

    def read_BatteryMonitor(self):
        device_address = 0x22
        try:
            data =self.bus.read_i2c_block_data(device_address, 0, 7)
            data[6] = bin(data[6])
            # print("Message received:", data)
            return data
        except Exception as e:
            print("Error reading I2C data:", str(e))
            return [0, 0, 0, 0, 0, 0, 0]

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.

        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    def read_IMU(self):
        accel_data = self.IMU.get_accel_data()
        gyro_data = self.IMU.get_gyro_data()
        
        # convert the data to single dictionary
        data = {
            "accel_x": accel_data['x'],
            "accel_y": accel_data['y'],
            "accel_z": accel_data['z'],
            "gyro_x": gyro_data['x'],
            "gyro_y": gyro_data['y'],
            "gyro_z": gyro_data['z']
        }
        return data

    def convert_temp(self, data):
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
        temp = ((value * 165.0) / 16383.0) - 40.0 + self.TEMP_CALIBRATION_OFFSET
        print(f"Raw Temp Value: {value}, Converted Temp: {temp}")  # Debugging statement
        return temp

    def convert_humi(self, data):
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

    def read_Temp_Humi(self):
        device_address = 0x27
        
        self.bus.write_byte(device_address, 0x00)
        time.sleep(0.1)
        temp = self.bus.read_i2c_block_data(device_address, 0, 2)
        
        self.bus.write_bytes(device_address, 0x01)
        time.sleep(0.1)
        humi = self.bus.read_i2c_block_data(device_address, 0, 2)
        
        temp = self.convert_temp(temp)
        humi = self.convert_humi(humi)
        
        data = {
            "temperature": temp,
            "humidity": humi
        }
        
        return data

    def read_Hydrophones(self):
        pass

    def read_Depth(self):
        pass

    def post_data(self, data_type, data):
        """Posts data to the specified data type endpoint.

        Args:
            data_type (str): 'sensors', 'output', or 'input' indicating the type of data to post.
            data (dict): The data to be posted.

        Returns:
            str: Server response as a string.
        """
        response = requests.post(f"{self.base_url}/{data_type}", json=data)
        if response.status_code == 201:
            return "Data added successfully"
        else:
            return f"Failed to add data, status code: {response.status_code}"

    def get_data(self, data_type):
        """Retrieves data from the specified data type endpoint.

        Args:
            data_type (str): 'sensors', 'output', or 'input' indicating the type of data to retrieve.

        Returns:
            dict: The retrieved data as a dictionary.
        """
        response = requests.get(f"{self.base_url}/{data_type}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get data, status code: {response.status_code}")
            return {}

    def run(self):
        delay = 0.01
        default_esc_value = 127  # Default value for ESCs when data is missing or there's an error

        time.sleep(10)  # Wait for the server to start

        while True:
            battery_monitor_data = self.read_BatteryMonitor()
            IMU_data = self.read_IMU()
            temp_humi_data = self.read_Temp_Humi()
            sensor_data = {
                "voltage1": battery_monitor_data[0],
                "voltage2": battery_monitor_data[2],
                "voltage3": battery_monitor_data[4],
                "current1": battery_monitor_data[1],
                "current2": battery_monitor_data[3],
                "current3": battery_monitor_data[5],
                "error": battery_monitor_data[6],
                "depth": 0,
                "X": IMU_data["accel_x"],
                "Y": IMU_data["accel_y"],
                "Z": IMU_data["accel_z"],
                "pitch": IMU_data["gyro_x"],
                "roll": IMU_data["gyro_y"],
                "yaw": IMU_data["gyro_z"],
                "temperature": temp_humi_data["temperature"],
                "orin_temp": 0,
                "humidity": temp_humi_data["humidity"],
                "heading": 0
            }

            # # Post sensor data to the server
            # self.post_data("sensors", sensor_data)

            # Get output data from the server
            output_data = self.get_data("output")

            # Debug 
            # print(output_data)
            print(sensor_data)

            # Check if all required keys are present in the output data
            required_keys = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "Claw", "Torp1", "Torp2"]
            if all(key in output_data for key in required_keys):
                # esc_values = [output_data["M1"], output_data["M2"], output_data["M3"], output_data["M4"], 
                #               output_data["M5"], output_data["M6"], output_data["M7"], output_data["M8"]]
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

    def test_run(self, data):
        delay = 0.01
        # esc_data = [127, 127, 127, 127, 127, 127, 127, 127]
        # while True:
            # self.write_ESCs()
            # # print(1)
            # time.sleep(delay)
            # motor_choice = input("Enter motor number (1 - 8): ")
            # motor_value = input("Enter motor value (64 - 191): ")
            # esc_data[int(motor_choice) - 1] = int(motor_value)
        esc_data = data
        self.write_ESCs(esc_data)
        time.sleep(delay)

if __name__ == '__main__':
    HI = HardwareInterface()
    HI.run()
    # HI.test_run([127, 127, 127, 127, 127, 127, 127, 127])
