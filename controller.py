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

import requests
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

    def print_data(self):
        """
        Print the data array.
        """
        s = "\r"
        # for i in range(len(self.joy_data)):
        #     s += f"{self.joy_data[i]}, "
        for key in self.out_data:
            s += f"{self.out_data[key]}, "
        print(s, end='')

    def map(self, x : float, in_min : float = -1.0, in_max : float = 1.0, out_min : int = 1000, out_max : int = 2000):
        """
        @brief Map a value from one range to another.
        """
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
    def run(self):
        """
        Run the main loop to get and print the data.
        """
        while True:
            self.get_data()
            self.map_data()
            self.print_data()
            pygame.time.wait(100)

if __name__ == "__main__":
    cm = CM()
    cm.run()