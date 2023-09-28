import pygame  # Import the pygame library for joystick handling
import numpy as np  # Import the numpy library for numerical operations

# Define a class to handle joystick inputs
class JoystickHandler:
    def __init__(self, axis_count=6):  # Initialize the joystick handler with a default axis count of 6
        self.axis_count = axis_count  # Store the axis count
        pygame.init()  # Initialize the pygame library
        self.joysticks = {}  # Create an empty dictionary to store joystick instances
        pygame.joystick.init()  # Initialize the joystick module in pygame

        # Initialize all available joysticks and store them in the dictionary
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks[joystick.get_instance_id()] = joystick

    # Method to get joystick input
    def get_joystick_input(self):
        # Handle 6-axis joystick
        if self.axis_count == 6:
            joystick_input = np.zeros((6, 1))  # Initialize a numpy array to store joystick input
            # Loop through each joystick and get its input
            for joystick in self.joysticks.values():
                toggle_switch = joystick.get_button(0)  # Get the state of the toggle switch (button 0)
                # Get the axis values and round them to 2 decimal places
                for i in range(4):
                    joystick_input[i, 0] = round(joystick.get_axis(i), 2)
                # Special case handling based on axis 1 value
                if -0.665 >= joystick.get_axis(1) >= -0.667:
                    for i in range(6):
                        joystick_input[i, 0] = 0.00
                # Handle toggle switch being pressed
                if toggle_switch:
                    joystick_input[2, 0] = 0.00
                    joystick_input[3, 0] = 0.00
                    joystick_input[4, 0] = round(joystick.get_axis(2), 2)
                    joystick_input[5, 0] = round(joystick.get_axis(3), 2)
            # Return the joystick input as a list
            return [joystick_input[3, 0], joystick_input[4, 0], joystick_input[1, 0], joystick_input[2, 0], joystick_input[5, 0], joystick_input[0, 0]]
        # Handle 5-axis joystick
        elif self.axis_count == 5:
            joystick_input = np.zeros((5, 1))  # Initialize a numpy array to store joystick input for 5-axis
            # Loop through each joystick and get its input (similar to 6-axis)
            for joystick in self.joysticks.values():
                toggle_switch = joystick.get_button(0)
                for i in range(4):
                    joystick_input[i, 0] = round(joystick.get_axis(i), 2)
                if -0.665 >= joystick.get_axis(1) >= -0.667:
                    for i in range(5):
                        joystick_input[i, 0] = 0.00
                if toggle_switch:
                    joystick_input[2, 0] = 0.00
                    joystick_input[3, 0] = 0.00
                    joystick_input[4, 0] = round(joystick.get_axis(2), 2)
            return [joystick_input[3, 0], joystick_input[4, 0], joystick_input[1, 0], joystick_input[2, 0], joystick_input[0, 0]]
        # Default case: return zeros
        else:
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Define a class for PID control
class PID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, setpoint=0.0):  # Initialize the PID controller with default parameters
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Desired setpoint value
        self.prev_error = 0.0  # Previous error value for derivative calculation
        self.integral = 0.0  # Integral term

    def reset(self):  # Reset the PID controller
        self.prev_error = 0.0  # Reset previous error
        self.integral = 0.0  # Reset integral term

    def compute(self, current_value):  # Compute the PID output
        error = self.setpoint - current_value  # Calculate the error
        self.integral += error  # Update the integral term
        derivative = error - self.prev_error  # Calculate the derivative term
        output = self.kp * error + self.ki * self.integral + self.kd * derivative  # Calculate the PID output
        self.prev_error = error  # Update the previous error
        return output  # Return the PID output

# Class for M6 Controller
class M6Controller:
    def __init__(self):
        # Initialize parameters
        self.d = 0.2  # Distance parameter
        self.theta = np.pi / 4  # Angle parameter in radians

        # Initialize PID controllers for each axis and rotation
        self.X = PID(1.0, 0.0, 0.0)
        self.Y = PID(1.0, 0.0, 0.0)
        self.Z = PID(1.0, 0.0, 0.0)
        self.R_x = PID(1.0, 0.0, 0.0)
        self.R_y = PID(1.0, 0.0, 0.0)
        self.R_z = PID(1.0, 0.0, 0.0)

        # List of PID controllers
        self.PIDs = [self.X, self.Y, self.Z, self.R_x, self.R_z]

        # Initialize joystick input and desired and actual states
        self.input = JoystickHandler(axis_count=5)
        self.desired = self.input.get_joystick_input()
        self.actual = [0.0, 0.0, 0.0, 0.0, 0.0]

        # Initialize PID outputs
        self.PIDs_out = [0.00, 0.00, 0.00, 0.00, 0.00]

        # Create thruster matrix
        self.thruster_matrix = self.create_Thruster_Matrix()

    # Function to create thruster matrix
    def create_Thruster_Matrix(self):
        # Define thruster configurations
        thruster_configurations = [
            {'position': [-1 * self.d, self.d, 0], 'orientation': [np.cos(np.radians(30)), np.sin(np.radians(30)), 0]},
            {'position': [self.d, self.d, 0], 'orientation': [-np.cos(np.radians(30)), np.sin(np.radians(30)), 0]},
            {'position': [-1 * self.d, 0, 0.1], 'orientation': [0, 0, -1]},
            {'position': [self.d, 0, 0.1], 'orientation': [0, 0, -1]},
            {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': [np.cos(np.radians(30)), -np.sin(np.radians(30)), 0]},
            {'position': [self.d, -1 * self.d, 0], 'orientation': [-np.cos(np.radians(30)), -np.sin(np.radians(30)), 0]}
        ]

        # Initialize mixing matrix
        mixing_matrix = np.zeros((6, 5))

        # Populate mixing matrix based on thruster configurations
        for i, config in enumerate(thruster_configurations):
            r = np.array(config['position'])
            d = np.array(config['orientation'])
            mixing_matrix[i, :3] = d
            mixing_matrix[i, 3:] = np.cross(r, d)

        return mixing_matrix

    # Function to update desired state from joystick input
    def update_desired(self):
        self.desired = self.input.get_joystick_input()

    # Function to update actual state
    def update_actual(self, actual):
        self.actual = actual

    # Main update function
    def update(self):
        self.update_desired()
        self.update_actual(self.actual)

        # Update PID controllers
        for i in range(6):
            self.PIDs[i].setpoint = self.desired[i]
            self.PIDs[i].compute(self.actual[i])

# Class for M8 Controller
class M8Controller:
    def __init__(self):
        # Initialize parameters
        self.d = 0.2  # Distance parameter
        self.theta = np.pi / 4  # Angle parameter in radians

        # Initialize PID controllers for each axis and rotation
        self.X = PID(1.0, 0.0, 0.0)
        self.Y = PID(1.0, 0.0, 0.0)
        self.Z = PID(1.0, 0.0, 0.0)
        self.R_x = PID(1.0, 0.0, 0.0)
        self.R_y = PID(1.0, 0.0, 0.0)
        self.R_z = PID(1.0, 0.0, 0.0)

        # List of PID controllers
        self.PIDs = [self.X, self.Y, self.Z, self.R_x, self.R_y, self.R_z]

        # Initialize joystick input and desired and actual states
        self.input = JoystickHandler(axis_count=6)
        self.desired = self.input.get_joystick_input()
        self.actual = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Initialize PID outputs
        self.PIDs_out = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

        # Create thruster matrix
        self.thruster_matrix = self.create_Thruster_Matrix()

    # Function to create thruster matrix
    def create_Thruster_Matrix(self):
        # Define thruster configurations
        thruster_configurations = [
            {'position': [-1 * self.d, self.d, 0], 'orientation': [-1 * np.cos(self.theta), 1 * np.sin(self.theta), 0]},
            {'position': [self.d, self.d, 0], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [self.d, -1 * self.d, 0], 'orientation': [np.cos(self.theta), -1 * np.sin(self.theta), 0]},
            {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': [-1 * np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [-1 * self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, self.d, self.d], 'orientation': [0, 0, 1]},
            {'position': [self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, -1 * self.d, self.d], 'orientation': [0, 0, 1]}
        ]

        # Initialize mixing matrix
        mixing_matrix = np.zeros((8, 6))

        # Populate mixing matrix based on thruster configurations
        for i, config in enumerate(thruster_configurations):
            r = np.array(config['position'])
            d = np.array(config['orientation'])
            mixing_matrix[i, :3] = d
            mixing_matrix[i, 3:] = np.cross(r, d)

        return mixing_matrix

    # Function to update desired state from joystick input
    def update_desired(self):
        self.desired = self.input.get_joystick_input()

    # Function to update actual state
    def update_actual(self, actual):
        self.actual = actual

    # Main update function
    def update(self):
        self.update_desired()
        self.update_actual(self.actual)

        # Update PID controllers
        for i in range(6):
            self.PIDs[i].setpoint = self.desired[i]
            self.PIDs[i].compute(self.actual[i])

if __name__ == '__main__':
    m8 = M8Controller()

    print(m8.thruster_matrix)