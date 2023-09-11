import pygame
import numpy as np

class JoystickHandler:
    def __init__(self, axis_count=6):
        self.axis_count = axis_count
        pygame.init()
        self.joysticks = {}
        pygame.joystick.init()
        
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks[joystick.get_instance_id()] = joystick

    def get_joystick_input(self):
        if self.axis_count == 6:
            joystick_input = np.zeros((6, 1))
            
            for joystick in self.joysticks.values():
                toggle_switch = joystick.get_button(0)
                
                for i in range(4):
                    joystick_input[i, 0] = round(joystick.get_axis(i), 2)
                
                if -0.665 >= joystick.get_axis(1) >= -0.667:
                    for i in range(6):
                        joystick_input[i, 0] = 0.00

                if toggle_switch:
                    joystick_input[2, 0] = 0.00
                    joystick_input[3, 0] = 0.00
                    joystick_input[4, 0] = round(joystick.get_axis(2), 2)
                    joystick_input[5, 0] = round(joystick.get_axis(3), 2)

            return [joystick_input[3, 0], joystick_input[4, 0], joystick_input[1, 0], joystick_input[2, 0], joystick_input[5, 0], joystick_input[0, 0]]
        elif self.axis_count == 5:
            joystick_input = np.zeros((5, 1))
            
            for joystick in self.joysticks.values():
                toggle_switch = joystick.get_button(0)
                
                for i in range(4):
                    joystick_input[i, 0] = round(joystick.get_axis(i), 2)
                
                if -0.665 >= joystick.get_axis(1) >= -0.667:
                    for i in range(6):
                        joystick_input[i, 0] = 0.00

                if toggle_switch:
                    joystick_input[2, 0] = 0.00
                    joystick_input[3, 0] = 0.00
                    joystick_input[4, 0] = round(joystick.get_axis(2), 2)
                    joystick_input[5, 0] = round(joystick.get_axis(3), 2)

            return [joystick_input[3, 0], joystick_input[4, 0], joystick_input[1, 0], joystick_input[2, 0], joystick_input[5, 0], joystick_input[0, 0]]
        else:
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

class PID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, setpoint=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0.0
        self.integral = 0.0

    def reset(self):
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, current_value):
        error = self.setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output

class M6Controller:
    def __init__(self):
        self.d = 0.2
        self.theta = np.pi / 4

        self.X = PID(1.0, 0.0, 0.0)
        self.Y = PID(1.0, 0.0, 0.0)
        self.Z = PID(1.0, 0.0, 0.0)
        self.R_x = PID(1.0, 0.0, 0.0)
        self.R_y = PID(1.0, 0.0, 0.0)
        self.R_z = PID(1.0, 0.0, 0.0)

        self.PIDs = [self.X, self.Y, self.Z, self.R_x, self.R_y, self.R_z]

        self.input = JoystickHandler(axis_count=5)
        self.desired = self.input.get_joystick_input()
        self.actual = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.PIDs_out = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

        # Thruster Matrix for 8 thrusters
        self.thruster_matrix = self.create_Thruster_Matrix()

    def create_Thruster_Matrix(self):
        # thruster_configurations = [
        #     {'position': [-1 * self.d, self.d, 0], 'orientation': [-1 * np.cos(self.theta), 1 * np.sin(self.theta), 0]},
        #     {'position': [self.d, self.d, 0], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]},
        #     {'position': [self.d, -1 * self.d, 0], 'orientation': [np.cos(self.theta), -1 * np.sin(self.theta), 0]},
        #     {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': -1 * [np.cos(self.theta), -1 * np.sin(self.theta), 0]},
        #     {'position': [-1 * self.d, 0, self.d], 'orientation': [0, 0, 1]},
        #     {'position': [0, self.d, self.d], 'orientation': [0, 0, 1]},
        #     {'position': [self.d, 0, self.d], 'orientation': [0, 0, 1]},
        #     {'position': [0, -1 * self.d, self.d], 'orientation': [0, 0, 1]}
        # ]

        thruster_configurations = [
            {},
            {},
            {},
            {},
            {},
            {}
        ]

        mixing_matrix = np.zeros((6, 5))

        for i, config in enumerate(thruster_configurations):
            r = np.array(config['position'])
            d = np.array(config['orientation'])

            mixing_matrix[i, :3] = d
            mixing_matrix[i, 3:] = np.cross(r, d)

        return mixing_matrix

class M8Controller:
    def __init__(self):
        self.d = 0.2
        self.theta = np.pi / 4

        self.X = PID(1.0, 0.0, 0.0)
        self.Y = PID(1.0, 0.0, 0.0)
        self.Z = PID(1.0, 0.0, 0.0)
        self.R_x = PID(1.0, 0.0, 0.0)
        self.R_y = PID(1.0, 0.0, 0.0)
        self.R_z = PID(1.0, 0.0, 0.0)

        self.PIDs = [self.X, self.Y, self.Z, self.R_x, self.R_y, self.R_z]

        self.input = JoystickHandler(axis_count=6)
        self.desired = self.input.get_joystick_input()
        self.actual = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.PIDs_out = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

        self.thruster_matrix = self.create_Thruster_Matrix()

    def create_Thruster_Matrix(self):
        thruster_configurations = [
            {'position': [-1 * self.d, self.d, 0], 'orientation': [-1 * np.cos(self.theta), 1 * np.sin(self.theta), 0]},
            {'position': [self.d, self.d, 0], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [self.d, -1 * self.d, 0], 'orientation': [np.cos(self.theta), -1 * np.sin(self.theta), 0]},
            {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': -1 * [np.cos(self.theta), -1 * np.sin(self.theta), 0]},
            {'position': [-1 * self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, self.d, self.d], 'orientation': [0, 0, 1]},
            {'position': [self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, -1 * self.d, self.d], 'orientation': [0, 0, 1]}
        ]

        mixing_matrix = np.zeros((8, 6))

        for i, config in enumerate(thruster_configurations):
            r = np.array(config['position'])
            d = np.array(config['orientation'])

            mixing_matrix[i, :3] = d
            mixing_matrix[i, 3:] = np.cross(r, d)

        return mixing_matrix

    def update_desired(self):
        self.desired = self.input.get_joystick_input()

    def update_actual(self, actual):
        self.actual = actual

    def update(self):
        self.update_desired()
        self.update_actual(self.actual)

        for i in range(6):
            self.PIDs[i].setpoint = self.desired[i]
            self.PIDs[i].compute(self.actual[i])
