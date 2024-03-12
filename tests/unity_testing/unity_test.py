import socket 
import numpy
import pygame
import numpy as np


class CM:
    """
    ## CM (Control Mapping) Class
    
    The `CM` class is used to read input data from an RC flight controller 
    and store it as a numpy array.
    
    ### Attributes
    - `joystick`: The pygame Joystick object.
    - `data`: A numpy array that stores joystick data.
    """
    
    def __init__(self):
        """
        Initialize the CM object and call the method to initialize the joystick.
        
        ### Parameters
        - `num_of_axis`: Number of axes to initialize in the data array. Default is 6.
        """
        self.joystick = None
        self.init_joystick()

        self.config = {
            "X": 4,
            "Y": 3,
            "Z": 1,
            "Pitch": [8, 4],
            "Roll": [8, 3],
            "Yaw": 0
        }

        self.joy_data = []
        self.out_data = {"X": 0.0, "Y": 0.0, "Z": 0.0, "Pitch": 0.0, "Roll": 0.0, "Yaw": 0.0}

    def init_joystick(self):
        """
        Initialize the pygame library and the joystick.
        
        This method will keep retrying until a joystick is found.
        """
        pygame.init()
        while True:
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                print(f"{joystick_count} joystick(s) found. Using the first one.")
                break
            else:
                print("No joystick found. Retrying in 3 seconds.")
                pygame.time.wait(3000)
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_data(self):
        """
        Update the `data` array with the latest joystick values.
        
        ### Returns
        - `data`: The updated data array.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.joystick.init()

        self.joy_data = [round(self.joystick.get_axis(i), 2) for i in range(self.joystick.get_numaxes())]
        for i in range(self.joystick.get_numbuttons()):
            self.joy_data.append(self.joystick.get_button(i))
        for i in range(self.joystick.get_numhats()):
            self.joy_data.append(self.joystick.get_hat(i))
        return self.joy_data
    
    def map_data(self):
        """
        Map the data to the correct output values.
        self.config = {
            "X": 4,
            "Y": 3,
            "Z": 1,
            "Pitch": [20, 4],
            "Roll": [20, 3],
            "Yaw": 0
        }
        or On personal controller
        self.config = {
            "X": 4,
            "Y": 3,
            "Z": 1,
            "Pitch": [8, 4],
            "Roll": [8, 3],
            "Yaw": 0
        }
        """
        if self.joy_data[self.config["Pitch"][0]] == 1:
            self.out_data["Pitch"] = self.joy_data[self.config["Pitch"][1]] if abs(self.joy_data[self.config["Pitch"][1]]) > 0.1 else 0.0
            self.out_data["Roll"] = self.joy_data[self.config["Roll"][1]] if abs(self.joy_data[self.config["Roll"][1]]) > 0.1 else 0.0
            self.out_data["X"] = 0.0
            self.out_data["Y"] = 0.0
        else:
            self.out_data["X"] = self.joy_data[self.config["X"]] if abs(self.joy_data[self.config["X"]]) > 0.1 else 0.0
            self.out_data["Y"] = self.joy_data[self.config["Y"]] if abs(self.joy_data[self.config["Y"]]) > 0.1 else 0.0
            self.out_data["Pitch"] = 0.0
            self.out_data["Roll"] = 0.0
        self.out_data["Z"] = self.joy_data[self.config["Z"]] if abs(self.joy_data[self.config["Z"]]) > 0.1 else 0.0
        self.out_data["Yaw"] = self.joy_data[self.config["Yaw"]] if abs(self.joy_data[self.config["Yaw"]]) > 0.1 else 0.0

        return self.out_data

    def print_data(self):
        """
        Print the data array.
        """
        s = "\r"
        for i in range(len(self.joy_data)):
            s += f"{self.joy_data[i]}, "
        s = "\r"
        for i in range(len(self.out_data)):
            s += f"{self.out_data[i]}, "
        print(s, end='')

    def map(self, x : float, in_min : float = -1.0, in_max : float = 1.0, out_min : int = 1000, out_max : int = 2000):
        """
        @brief Map a value from one range to another.
        """
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


class MovementPackage:
    def __init__(self):
        d1 = (numpy.sqrt((0.5 ** 2) + (0.3 ** 2))) * numpy.sin(45)
        d2 = (numpy.sqrt((0.25 ** 2) + (0.3 ** 2)))
        self.motors1_4 = [[d1,  d1, -d1, -d1],   # X 
                        [d1, -d1, -d1,  d1],   # Y
                        [d1,  d1,  d1,  d1]]   # Yaw
        self.motors5_8 = [[d2,  d2,  d2, d2],   # Z 
                          [-d2, -d2,  d2, d2],   # Pitch 
                          [d2, -d2, -d2, d2]]   # Roll 
        
    def map(self, x : float, in_min : float, in_max : float, out_min : int, out_max : int) -> int:
        """
        @brief Map a value from one range to another.
        """
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min, 2)
    
    def compute_movement(self, data : dict) -> list:
        """
        @brief Compute the movement of the drone based on the input data.
        """
        values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if data['X'] != 0.0 or data['Y'] != 0.0 or data['Yaw'] != 0.0:
            if data['X'] >= 0.1 or data['X'] <= -0.1:
                for i in range(4):
                    values[i] = round(data['X'] * self.motors1_4[0][i], 2)
            elif data['Y'] >= 0.1 or data['Y'] <= -0.1:
                for i in range(4):
                    values[i] = round(data['Y'] * self.motors1_4[1][i], 2)
            elif data['Yaw'] >= 0.1 or data['Yaw'] <= -0.1:
                for i in range(4):
                    values[i] = round(data['Yaw'] * self.motors1_4[2][i], 2)
        if data['Z'] != 0.0 or data['Pitch'] != 0.0 or data['Roll'] != 0.0:
            if data['Z'] >= 0.1 or data['Z'] <= -0.1:
                for i in range(4):
                    values[i + 4] = round(data['Z'] * self.motors5_8[0][i], 2)
            elif data['Pitch'] >= 0.1 or data['Pitch'] <= -0.1:
                for i in range(4):
                    values[i + 4] = round(data['Pitch'] * self.motors5_8[1][i], 2)
            elif data['Roll'] >= 0.1 or data['Roll'] <= -0.1:
                for i in range(4):
                    values[i + 4] = round(data['Roll'] * self.motors5_8[2][i], 2)
        # Map the values to the correct range
        for i in range(len(values)):
            values[i] = self.map(values[i], -0.5, 0.5, -1, 1)
        return values

class Unity:
    def __init__(self, ip='localhost', port=1234):
        """
        Initialize the Unity object.
        
        Parameters:
        - `ip`: IP address of the remote computer. Default is '10.0.0.52'.
        - `port`: Port number for the TCP connection. Default is 1234.
        """
        self.ip = ip
        self.port = port
        self.controller = CM()
        self.mapper = MovementPackage()

        # Create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the remote server
        try:
            self.s.connect((self.ip, self.port))
            print("Connected to the server successfully.")
        except socket.error as err:
            print(f"Failed to connect to the server: {err}")
            # It's a good practice to handle connection errors such as this.

    def get_data(self) -> dict:
        """
        Get the data from the controller and map it to the correct output.
        """
        self.controller.get_data()
        return self.controller.map_data()

    def get_mapped_data(self) -> list:
        """
        Get the data from the controller and map it to the correct output.
        """
        data = self.get_data()
        return self.mapper.compute_movement(data)

    def send_motor_data(self):
        """
        Send motor data to the remote computer over a TCP connection.
        """
        data = self.get_mapped_data()
        motor_data_str = ','.join([str(i) for i in data]) + ',R'  # Assuming you want to append ',R' for some reason.

        print(f"Sending motor data: {motor_data_str}")

        try:
            # Send the motor data
            self.s.sendall(motor_data_str.encode('utf-8'))
            print('Motor data sent to the server successfully.')
        except socket.error as err:
            print(f"Failed to send data: {err}")
            # Handle potential errors, such as disconnection or server unavailability.

    def close_connection(self):
        """
        Close the TCP connection when done.
        """
        self.s.close()
        print("Connection closed.")

    def fetch_image_data(self, image_id):
        """
        This method will not be functional in the TCP version as it was designed for HTTP communication.
        """
        pass

if __name__ == '__main__':
    unity = Unity()
    try:
        while True:
            unity.send_motor_data()
            # Additional operations...
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    finally:
        unity.close_connection()