import requests
import smbus2
import time
import json


class HardwareInterface:
    def __init__(self):
        self.bus = smbus2.SMBus(7)

        with open('./configs/hardware_interface.json') as f:
            self.config = json.load(f)

        self.base_url = self.config["baseUrl"]

    def write_ESCs(self, data = [127, 127, 127, 127, 127, 127, 127, 127]):
        device_address = 0x21
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
        default_esc_value = 127  # Default value for ESCs when data is missing or there's an error

        while True:
            battery_monitor_data = self.read_BatteryMonitor()
            sensor_data = {
                "voltage1": battery_monitor_data[0],
                "voltage2": battery_monitor_data[2],
                "voltage3": battery_monitor_data[4],
                "current1": battery_monitor_data[1],
                "current2": battery_monitor_data[3],
                "current3": battery_monitor_data[5],
                "error": battery_monitor_data[6],
                "depth": 0,  # Example: Add defaults or fetch from sensors
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

            # Post sensor data to the server
            self.post_data("sensors", sensor_data)

            # Get output data from the server
            output_data = self.get_data("output")

            # Check if all required keys are present in the output data
            required_keys = ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "claw", "torp1", "torp2"]
            print(output_data.keys())
            if all(key in output_data for key in required_keys):
                esc_values = [output_data[key] for key in required_keys[:8]]  # Get ESC values
                claw_torp_values = [output_data["claw"], output_data["torp1"], output_data["torp2"]]
            else:
                # Log an error and use default values if some data is missing
                print("Error: Not all required output data keys received, using default values")
                esc_values = [default_esc_value] * 8
                claw_torp_values = [0, 0, 0]

            # Send data to ESCs and battery monitor
            self.write_ESCs(esc_values)
            self.write_BatteryMonitor(claw_torp_values)

            time.sleep(delay)

if __name__ == '__main__':
    HI = HardwareInterface()
    HI.run()