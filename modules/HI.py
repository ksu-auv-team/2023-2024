import numpy as np
import serial
from datetime import datetime
import logging
import platform
import sys
import os
import json

# Create a logger object for the module
# Detect OS platform
system_os = platform.system()

# Dependent on OS, toggle os type flag
if system_os == "Windows":
    os_type = "windows"
elif system_os == "Linux":
    os_type = "linux"
elif system_os == "Darwin":
    os_type = "mac"
else:
    print("Unsupported OS")
    sys.exit()

# Configure log file path
def create_logger(filename="logfile"):
    """
    Creates and returns a logging object that writes log messages to a file.
    The filename includes a timestamp in the format "logfile_YYYY-MM-DD_HH-MM-SS.log".

    :return: Logger object configured with a timestamped file handler
    :rtype: logging.Logger
    """
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.INFO)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_handler = logging.FileHandler(f"logs/{filename}_{timestamp}.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger_.addHandler(file_handler)
    return logger_

# Create a logger object
logger = create_logger()
logger.info("Logger created")

# Log system information
logger.info(f'Date: {datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
logger.info(f"OS: {os_type}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")

# get config file
f = open(__file__.split("modules")[0]+'configs\\config.json')
config = json.load(f)
robot_config = config["ROBOT"]
f.close()

# Define a class for serial communication
class comm:
    def __init__(self, port="COM3", baud=115200, timeout=1, motor_count=robot_config["MOTORS"]["COUNT"], logger:logging.Logger=logger): #Actually use the config file
        self.port = port
        self.baud = baud
        self.timeout = timeout

        self.logger = logger

        self.serial = serial.Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)
        self.serial.flush()

        self.FULL_ACTIVE = 0xFF
        self.CONTROL_ONLY = 0x04
        self.CONTROLLED_SHUTDOWN = 0x0F
        self.EMERGENCY_SHUTDOWN = 0xFF

        self.KILL_SWITCH = 0b10000000
        self.PWM_ENABLE = 0b00000001
        self.SENSOR_ENABLE = 0b00000010
        self.SENSOR_FETCH = 0b00100000

        self.SENSOR_DATA_END = bytearray(0xFFFFFFFF)

        self.data = bytearray()
        self.byte_data.append(0x0C) # Standard transfer - 4 byte control flag - 8 byte PWM data
        self.byte_data.append(0x00) # Normal robot state
        self.byte_data.append(0x00) # No sensor query
        self.byte_data.append(0xFF) # All motor enable

        self.motor_count = motor_count
        self.in_data = [0, 0, 0, 0, 0, 0, 0, 0]

        #no need to check if the motor count is 8 as we can just make that the default
        if self.motor_count !=8 or self.motor_count != 6:
            print("Invalid motor count")
            sys.exit()
        elif self.motor_count==6:
            #just cut off the last 2 values since thats what was happening already
            self.in_data = self.in_data[:-2]
            
        for _ in range(len(self.in_data)):
                self.byte_data.append(0)

    def get_data(self, data):
        self.in_data = data
        
        for i in range(4, len(self.in_data)):
            self.byte_data[i] = i.to_bytes(1,"little")

    def send(self):
        self.serial.write(self.byte_data)
        self.logger.info(f"Sent: {self.byte_data}")
    
    def receive(self):
        self.data = self.serial.read_all()
        self.logger.info(f"Received: {self.data}")

        return self.data

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
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)  # Calculate the PID output
        self.prev_error = error  # Update the previous error
        return output  # Return the PID output

class MP:
    def __init__(self, logger, motor_count=robot_config["MOTORS"]["COUNT"], theta=45, d=0.2, PID_vals:list=[[1.0, 0, 0]]*6, out_min=1100, out_max=1900):
        # set our paramaters as recorded values
        self.motor_count = motor_count
        self.theta = np.radians(theta)
        self.d = d
        self.logger = logger # Initialize the logging setup
        self.out_min = out_min
        self.out_max = out_max
        
        # set this as the PID default and just remove / add values as needed
        self.PIDs = [
                PID(PID_vals[0][0], PID_vals[0][1], PID_vals[0][2]),
                PID(PID_vals[1][0], PID_vals[1][1], PID_vals[1][2]),
                PID(PID_vals[2][0], PID_vals[2][1], PID_vals[2][2]),
                PID(PID_vals[3][0], PID_vals[3][1], PID_vals[3][2]),
                PID(PID_vals[4][0], PID_vals[4][1], PID_vals[4][2]),
                PID(PID_vals[5][0], PID_vals[5][1], PID_vals[5][2]),
            ]
        
        # move outside the if statement since its already decided in the function
        self.mixing_matrix = self.create_thruster_matrix()
        if motor_count == 8:
            self.actual = np.zeros((6, 1))
            self.desired = np.zeros((6, 1))

        elif motor_count == 6:
            self.actual = np.zeros((5, 1))
            self.desired = np.zeros((5, 1))
            self.PIDs = self.PIDS[:-1] # remove the last value so it is correct
        
        # Finish initializing logger
        self.logger.info(f"MP initialized with {motor_count} motors")
        self.logger.info(f"MP initialized with PID values: {PID_vals}")

        # Initialize the serial module
        self.serial = comm(motor_count=self.motor_count, logger=self.logger)

        #declaring up here so we can have just one function instead of 2
        self.eight_thruster_config = [
            {'position': [-1 * self.d, self.d, 0], 'orientation': [-np.cos(self.theta), np.sin(self.theta), 0]}, #! idk why it was multiplied by 1 ???
            {'position': [self.d, self.d, 0], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [self.d, -1 * self.d, 0], 'orientation': [np.cos(self.theta), -np.sin(self.theta), 0]},
            {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': [-np.cos(self.theta), np.sin(self.theta), 0]},
            {'position': [-1 * self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, self.d, self.d], 'orientation': [0, 0, 1]},
            {'position': [self.d, 0, self.d], 'orientation': [0, 0, 1]},
            {'position': [0, -1 * self.d, self.d], 'orientation': [0, 0, 1]}
        ]
        self.six_thruster_config = [
            {'position': [-1 * self.d, self.d, 0], 'orientation': [np.cos(self.theta), np.sin(self.theta), 0]}, #! why is this hard codded to 30 degrees???
            {'position': [self.d, self.d, 0], 'orientation': [-np.cos(self.theta), np.sin(self.theta), 0]},     #! why not just use self.theta instead of np.radians(30)?
            {'position': [-1 * self.d, 0, 0.1], 'orientation': [0, 0, -1]},
            {'position': [self.d, 0, 0.1], 'orientation': [0, 0, -1]},
            {'position': [-1 * self.d, -1 * self.d, 0], 'orientation': [np.cos(self.theta), -np.sin(self.theta), 0]},
            {'position': [self.d, -1 * self.d, 0], 'orientation': [-np.cos(self.theta), -np.sin(self.theta), 0]}
        ]

    def create_thruster_matrix(self): #fix function naming into correct casing
        if self.motor_count == 8:
            thruster_configurations = self.eight_thruster_config
            # Initialize mixing matrix
            mixing_matrix = np.zeros((8, 6))
            
        elif self.motor_count == 6:
            thruster_configurations = self.six_thruster_config
            mixing_matrix = np.zeros((6, 5))

        # Populate mixing matrix based on thruster configurations
        for i, config in enumerate(thruster_configurations):
            r = np.array(config['position'])
            d = np.array(config['orientation'])
            mixing_matrix[i, :3] = d
            mixing_matrix[i, 3:] = np.cross(r, d)

        # Log mixing matrix
        self.logger.info(f"Mixing matrix: {mixing_matrix}")

        return mixing_matrix

    # TODO: Receive actual data from serial module
    # Function to update actual state
    def update_actual(self):
        """
        if motor_count == 8:
            actual = [x, y, z, yaw, roll, pitch]
        else:
            actual = [x, y, z, yaw, roll]
        received from serial module
        """
        self.actual = None

    # TODO: Receive desired data from state machine module
    # Function to update desired state from joystick input
    def update_desired(self):
        """
        if motor_count == 8:
            desired = [x, y, z, yaw, roll, pitch]
        else:
            desired = [x, y, z, yaw, roll]
        received from state machine module
        """
        self.desired = None

    # TODO: Test this function
    # TODO: Ensure data is in correct format
    # TODO: Ensure data is in correct range
    # Main update function
    def update(self):
        """
        1. Calculate error (desired - actual)
        2. Calculate thrusts (error * PIDs)
        3. Calculate PWMs (thrusts * mixing matrix)
        4. Don't know if we need to map PWM output to 1100-1900 yet, will find out later
        5. PWMs to serial module
        """
        for i in range(len(self.PIDs)):
            self.update_actual()
            self.update_desired()
            self.PIDs[i].setpoint = self.desired[i]
            self.PIDs[i].compute(self.actual[i])
        self.data = np.dot(self.mixing_matrix, self.PIDs)
        self.serial.get_data(self.data)
        self.serial.send()

    # Function to map PID Output to PWM
    def map(self, x):
        in_min = -1.0
        in_max = 1.0
        out_min = self.out_min
        out_max = self.out_max

        return ( ( (x - in_min) * (out_max - out_min) ) / (in_max - in_min) ) + out_min

    # Function to run the MP
    def run(self):
        pass
