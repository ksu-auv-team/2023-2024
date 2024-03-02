import socket
import numpy
import pygame


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
            "Pitch": [20, 4],
            "Roll": [20, 3],
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

    def print_in(self):
        """
        @brief Print the current state of the `data` array.
        """
        s = '\r'
        for i in range(len(self.joy_data)):
            s += f' {i}: {self.joy_data[i]} |'
        print(s, end='')

    def print_out(self):
        """
        @brief Print the current state of the `data` array.
        """
        # print(self.out_data)
        s = '\r'
        for key in self.out_data:
            s += f' {key}: {self.out_data[key]} |'
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
    def __init__(self, host : str = '127.0.0.1', port : int = 5005):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

        self.controller = CM()
        self.mapper = MovementPackage()
    
    def get_data(self) -> dict:
        """
        @brief Get the data from the controller and map it to the correct output.
        """
        self.controller.get_data()
        return self.controller.map_data()
    
    def send_data_6_values(self, data : dict):
        """
        @brief Send the data to the Unity simulation only works for 6 values. 
        """
        s = f'{data["X"]},{data["Y"]},{data["Z"]},{data["Pitch"]},{data["Roll"]},{data["Yaw"]}R'
        self.sock.sendall(s.encode('utf-8'))

    def send_data_8_values(self, data : list):
        """
        @brief Send the data to the Unity simulation only works for 8 values. 
        """
        s = f'{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]},{data[7]}R'
        self.sock.sendall(s.encode('utf-8'))
    
    def run(self):
        """
        @brief Run the main loop for the controller and the Unity simulation.
        """
        while True:
            try:
                data = self.get_data()
                # self.controller.print_in()
                # self.controller.print_out()
                data = self.mapper.compute_movement(data)
                self.send_data_8_values(data)
                print(f'\r{data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}, {data[7]}', end='')
                pygame.time.wait(10)
            except KeyboardInterrupt:
                pygame.quit()
                break

if __name__ == '__main__':
    unity = Unity()
    unity.run()