import requests
import smbus2
import time
import json


class HardwareInterface:
    def __init__(self):
        self.bus = smbus2.SMBus(7)

        with open('./configs/hardware_interface.json') as f:
            self.config = json.load(f)

        self.baseUrl = self.config["baseUrl"]

    def write_ESCs(self, data = [127, 127, 127, 127, 127, 127, 127, 127]):
        device_address = 0x21
        try:
            self.bus.write_i2c_block_data(device_address, 0, data)
            print("Message sent:", data)
        except Exception as e:
            print("Error writing I2C data:", str(e))

    def write_BatteryMonitor(self, data = [127, 0, 0]):
        device_address = 0x22
        try:
            self.bus.write_i2c_block_data(device_address, 0, data)
            print("Message sent:", data)
        except Exception as e:
            print("Error writing I2C data:", str(e))

    def read_BatteryMonitor(self):
        device_address = 0x22
        try:
            data =self.bus.read_i2c_block_data(device_address, 0, 7)
            data[6] = bin(data[6])
            print("Message received:", data)
            return data
        except Exception as e:
            print("Error reading I2C data:", str(e))
            return [0, 0, 0, 0, 0, 0, 0]

    def read_IMU(self):
        pass

    def read_Temp_Humi(self):
        pass

    def read_Hydrophones(self):
        pass

    def read_Depth(self):
        pass

    def get_data(self, data_type):
        """Fetches data from the specified data type endpoint.

        Args:
            data_type (str): 'sensors', 'output', or 'input' indicating the type of data to fetch.

        Returns:
            dict: The data fetched from the server.
        """
        response = requests.get(f"{self.base_url}/{data_type}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data", "status_code": response.status_code}

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

    def run(self):
        delay = 0.01

        sensor_data = {
            "voltage1": 0,
            "voltage2": 0,
            "voltage3": 0,
            "current1": 0,
            "current2": 0,
            "current3": 0,
            "error": 0,
            "depth": 0,
            "X": 0,
            "Y": 0,
            "Z": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": 0,
            "temperature": 0,
            "orin_temp": 0,
            "humidity": 0,
            "heading": 0
        }

        while True:
            battery_monitor_data = self.read_BatteryMonitor()
            sensor_data["voltage1"] = battery_monitor_data[0]
            sensor_data["voltage2"] = battery_monitor_data[2]
            sensor_data["voltage3"] = battery_monitor_data[4]
            sensor_data["current1"] = battery_monitor_data[1]
            sensor_data["current2"] = battery_monitor_data[3]
            sensor_data["current3"] = battery_monitor_data[5]
            sensor_data["error"] = battery_monitor_data[6]

            self.post_data("sensors", sensor_data)

            data = self.get_data("output")
            self.write_ESCs([data["M1"], data["M2"], data["M3"], data["M4"], data["M5"], data["M6"], data["M7"], data["M8"]])
            self.write_BatteryMonitor([data["Claw"], data["Torp1"], data["Torp2"]])
            time.sleep(delay)

if __name__ == '__main__':
    HI = HardwareInterface()
    HI.run()