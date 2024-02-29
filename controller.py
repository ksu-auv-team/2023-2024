# # CM Class with Pygame and NumPy
#
# This class, `CM`, demonstrates how to get data from an RC flight controller.
# It uses `pygame` for the joystick interface and `NumPy` for data storage.
# The class has methods for initializing the joystick and updating and printing the control data.
#
# ## Dependencies
# - pygame
# - numpy
#
# ## How to Run
# - Initialize a `CM` object and call its `get_data` and `print` methods in a loop.

import numpy as np
import requests
import pygame
import json


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

        with open('static/configs/controller.json') as f:
            self.config = json.load(f)

        self.joy_data = []
        self.out_data = {"ARM": 0, "X": 0.0, "Y": 0.0, "Z": 0.0, "Pitch": 0.0, "Roll": 0.0, "Yaw_Right": 0.0, "Yaw_Left": 0.0, "Claw_Close": 0.0, "Claw_Open": 0.0}

        orin_ip = '127.0.0.1'
        self.url = f"http://{orin_ip}:5000/post_input_data"

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
        """
        for keys in self.config:
            if keys == "Yaw_Right" and abs(self.joy_data[self.config[keys]]) > 0.1:
                self.out_data['Yaw'] = -1 * self.joy_data[self.config[keys]]
            elif keys == "Yaw_Left" and abs(self.joy_data[self.config[keys]]) > 0.1:
                self.out_data['Yaw'] = self.joy_data[self.config[keys]]
            elif keys == "Claw_Close" and abs(self.joy_data[self.config[keys]]) > 0.1:
                self.out_data['Claw'] = -1 * self.joy_data[self.config[keys]]
            elif keys == "Claw_Open" and abs(self.joy_data[self.config[keys]]) > 0.1:
                self.out_data['Claw'] = self.joy_data[self.config[keys]]
            else:
                if abs(self.joy_data[self.config[keys]]) > 0.1:
                    self.out_data[keys] = self.joy_data[self.config[keys]]
                else:
                    pass
        return self.out_data
    
    def send_data(self, data : dict):
        """
        Sends controller data to the server.
        """
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, headers=headers, data=json.dumps(data))
        return response

    def print_in(self):
        """
        @brief Print the current state of the `data` array.
        """
        s = ''
        for i in range(len(self.joy_data)):
            s += f'   {i}: {self.joy_data[i]}   |'
        print(s)

    def print_out(self):
        """
        @brief Print the current state of the `data` array.
        """
        print(self.out_data)

    def map(self, x : float, in_min : float = -1.0, in_max : float = 1.0, out_min : int = 1000, out_max : int = 2000):
        """
        @brief Map a value from one range to another.
        """
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def run(self, debug : int = 0):
        """
        @brief Run the controller.
        """
        while True:
            self.get_data()
            self.map_data()
            # response = self.send_data(self.out_data)
            if debug == 1:
                self.print_in()
                # print("Server response:", response.text)
            elif debug == 2:
                self.print_out()
                # print("Server response:", response.text)
            else:
                # print("Server response:", response.text)
                pass


if __name__ == "__main__":
    cm = CM()
    cm.run(debug=2)    
