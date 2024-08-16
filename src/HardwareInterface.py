from modules.HardwareInterfaceSupport.MPU6050 import MPU6050
from modules.SupportAll.DebugHandler import DebugHandler

import smbus2
import json
import logging
import requests
import argparse
import time

class HardwareInterface:
    @staticmethod
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
        
    @staticmethod
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
        # print(f"Raw Temp Value: {value}, Converted Temp: {temp}")  # Debugging statement
        return temp
    
    @staticmethod
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
        # print(f"Raw Humi Value: {value}, Converted Humi: {humi}")  # Debugging statement
        return humi
    
    @staticmethod
    def log_data(self, type_of_data, data):
        """
        Logs data to the specified log file.

        Args:
            type (str): The type of data being logged.
            data (dict): The data to be logged.
        """
        if type == 'Debug':
            logging.debug(f"{type_of_data}: {json.dumps(data)}")
        elif type == 'Info':
            logging.info(f"{type_of_data}: {json.dumps(data)}")
        elif type == 'Warning':
            logging.warning(f"{type_of_data}: {json.dumps(data)}")
        elif type == 'Error':
            logging.error(f"{type_of_data}: {json.dumps(data)}")
        elif type == 'Critical':
            logging.critical(f"{type_of_data}: {json.dumps(data)}")

    def __init__(self, ip='localhost', port=5000, debug=False):
        logging.basicConfig(
            filename='logs/main.log',      # Name of the log file
            filemode='a',            # Append mode (use 'w' for overwrite each time)
            format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
            datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
            level=logging.INFO       # Minimum log level to record
        )

        self.bus = smbus2.SMBus(1)
        
        self.addresses = {
            'MPU6050': 0x68,
            'ESCs': 6,
            'Battery_Monitor': 7,
            'Arm': 9,
            'Temp': 0x27,
            'Hydrophones': None,
            'Depth': None
        }
        
        self.url = f"http://{ip}:{port}"
        self.debug = debug
        
        self.mpu = MPU6050(self.bus, self.addresses['MPU6050'])
        
        self.debugger = DebugHandler('HardwareInterface', ip, port)
    
    def print_data(self, data, data_type):
        message = f'{data_type}: {data}'
        self.debugger.set_data(MessageType="LOG", Message=message)
    
    def handle_error(self, error):
        self.debugger.set_data(MessageType="ERROR", Message=error)
    
    def get_data(self):
        """Retrieves data from the specified data type endpoint.

        Args:
            data_type (str): 'sensors', 'output', or 'input' indicating the type of data to retrieve.

        Returns:
            dict: The retrieved data as a dictionary.
        """
        try:
            response = requests.get(f"{self.ip}:{self.port}/Sensors")
            if response.status_code == 200:
                self.print_data(MessageType='Returned Data', Message=response.json())
                return response.json()
            else:
                print(f"Failed to get data, status code: {response.status_code}")
                return {}
        except requests.exceptions.RequestException as e:
            self.debugger.set_data(MessageType="ERROR", Message=str(e))
            return {}
    
    def send_data(self, data):
        """Posts data to the specified data type endpoint.

        Args:
            data_type (str): 'sensors', 'output', or 'input' indicating the type of data to post.
            data (dict): The data to be posted.

        Returns:
            str: Server response as a string.
        """
        response = requests.post(f"{self.baseurl}/Sensors", json=data)
        if response.status_code == 201:
            return "Data added successfully"
        else:
            return f"Failed to add data, status code: {response.status_code}"
    
    def write_ESCs(self, data):
        """Writes data to the ESCs.

        Args:
            data (dict): The data to be written to the ESCs.
        """
        try:
            self.bus.write_i2c_block_data(self.addresses['ESCs'], 0, data)
            # print("Message sent:", data)
        except Exception as e:
            if self.debug:
                self.log_data('Error', {'Error': str(e), 'Data': data})
            else:
                pass

    def write_Arm(self, data):
        """Writes data to the Arm.

        Args:
            data (dict): The data to be written to the Arm.
        """
        try:
            self.bus.write_i2c_block_data(self.addresses['Arm'], 0, data)
        except Exception as e:
            if self.debug:
                self.log_data('Error', {'Error': str(e), 'Data': data})
            else:
                pass
    
    def read_Temp(self):
        """Reads data from the temperature sensor.

        Returns:
            float: The temperature in degrees Celsius.
        """
        try:
            data = self.bus.read_i2c_block_data(self.addresses['Temp'], 0, 2)
            temp = self.convert_temp(data)
            return temp
        except Exception as e:
            if self.debug:
                self.log_data('Error', {'Error': str(e)})
            else:
                pass
    
    def read_BatteryMonitor(self):
        """Reads data from the battery monitor.

        Returns:
            float: The battery voltage.
        """
        try:
            data = self.bus.read_i2c_block_data(self.addresses['Battery_Monitor'], 0, 2)
            voltage = (data[0] << 8) | data[1]
            return voltage
        except Exception as e:
            if self.debug:
                self.log_data('Error', {'Error': str(e)})
            else:
                pass
    
    def read_Depth(self):
        """Reads data from the depth sensor.

        Returns:
            float: The depth in meters.
        """
        pass
    
    def read_Hydrophones(self):
        """Reads data from the hydrophones.

        Returns:
            dict: The hydrophone data.
        """
        pass
    
    def read_MPU6050(self):
        """Reads data from the MPU6050.

        Returns:
            dict: The MPU6050 data.
        """
        try:
            data = self.mpu.get_all_data()
            return data
        except Exception as e:
            if self.debug:
                self.log_data('Error', {'Error': str(e)})
            else:
                pass
    
    def test_ESCs(self):
        """Tests the ESCs.

        No Return Value
        Logged Output
        """
        data = [127, 127, 127, 127, 127, 127, 127, 127]
        for i in range(0, 8):
            data[i] = 150
            self.write_ESCs(data)
            time.sleep(4)
        for i in range(0, 8):
            data[i] = 100
            self.write_ESCs(data)
            time.sleep(4)
        for i in range(0, 8):
            data[i] = 127
            self.write_ESCs(data)
            time.sleep(4)
        self.write_ESCs([150, 150, 150, 150, 150, 150, 150, 150])
        time.sleep(4)
        self.write_ESCs([127, 127, 127, 127, 127, 127, 127, 127])
    
    def test_BatteryMonitor(self):
        """Tests the Battery Monitor.

        No Return Value
        Logged Output
        """
        pass
    
    def test_Arm(self):
        """Tests the Arm.

        No Return Value
        Logged Output
        """
        pass
    
    def test_Temp(self):
        """Tests the Temperature Sensor.

        No Return Value
        Logged Output
        """
        pass
    
    def test_Depth(self):
        """Tests the Depth Sensor.

        No Return Value
        Logged Output
        """
        pass
    
    def test_Hydrophones(self):
        """Tests the Hydrophones.

        No Return Value
        Logged Output
        """
        pass
    
    def test_MPU6050(self):
        """Tests the MPU6050.

        No Return Value
        Logged Output
        """
        pass
       
    def test_suite(self):
        """Runs a suite of tests on the Hardware Interface.

        No Return Value
        Logged Output
        
        User can select the test to run by adding the test number to the test_suite method call.
        
        Tests:
            - Test 1: Test the ESCs
            - Test 2: Test the Battery Monitor
            - Test 3: Test the Arm and Torpedoes
            - Test 4: Test the Temperature Sensor
            - Test 5: Test the Depth Sensor
            - Test 6: Test the Hydrophones
            - Test 7: Test the MPU6050
        """
        print("Running Hardware Interface Test Suite")
        while True:
            print("Select a test to run: \
                  \n1: Test the ESCs \
                  \n2: Test the Battery Monitor \
                  \n3: Test the Arm and Torpedoes \
                  \n4: Test the Temperature Sensor \
                  \n5: Test the Depth Sensor \
                  \n6: Test the Hydrophones \
                  \n7: Test the MPU6050 \
                  \n8: Exit")
            test = int(input("Enter the test number: "))
            if test == 1:
                self.test_ESCs()
            elif test == 2:
                self.test_BatteryMonitor()
            elif test == 3:
                self.test_Arm()
            elif test == 4:
                self.test_Temp()
            elif test == 5:
                self.test_Depth()
            elif test == 6:
                self.test_Hydrophones()
            elif test == 7:
                self.test_MPU6050()
            elif test == 8:
                break
            else:
                print("Invalid test number")
        