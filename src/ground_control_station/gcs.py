
# Import the necessary python libraries
import os
import sys
import datetime
import logging
import platform
import subprocess
from dataclasses import dataclass

# Import the necessary custom libraries
import PySimpleGUI as sg
import numpy as np
from numpysocket import NumpySocket
import serial
import yaml


# Define the dataclass for the ground control station joystick data
@dataclass
class Joystick:
    x_axis: float = 0.0
    y_axis: float = 0.0
    z_axis: float = 0.0
    
# Define the dataclass for the ground control station controller data
@dataclass
class Controller:
    left: Joystick
    right: Joystick
    buttons: dict
    

# Main class
class GCS:
    def __init__(self):
        # Create the log folder
        date = datetime.datetime.now(format='%Y-%m-%d_%H-%M-%S')
        os.mkdir(f'logs/{date}')
        
        # Create the logger which outputs a log file to the log folder that was just created
        logging.basicConfig(filename=f'logs/{date}/gcs.log', level=logging.DEBUG)
        
        # Create the logger which outputs to the console
        self.console = logging.StreamHandler()
        
        # Set the logging level for the console logger
        self.console.setLevel(logging.INFO)
        
        # Create the formatter for the console logger
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.console.setFormatter(console_format)
        
        # Add the console logger to the logger
        logging.getLogger('').addHandler(self.console)
        
        # Log the start of the program
        self.console.info('Starting the ground control station')
        
        # Load the configuration file
        with open('configs/gcs.yml', 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            
        # Log the configuration file
        self.console.info(f'Configuration file: {self.config}')
        
        # if self.config['serial'] == True:
        if self.config['serial']['enabled']:
            # Log that the serial port is being opened
            self.console.info('Opening the serial port')
            
            # Open the serial port
            self.serial = serial.Serial(
                port=self.config['serial']['serial_port'],
                baudrate=self.config['serial']['serial_baudrate'],
                timeout=self.config['serial']['serial_timeout'],
            )
            
            # Log that the serial port was opened
            self.console.info('Serial port opened at ' + str(self.serial.name))
            
        # Make sure the serial port is open and send the start bit
        if self.serial.is_open:
            self.serial.write(b'1\n')
            
        # Create the GUI
        title_size = (25, 1)
        label_size = (20, 1)
        data_label_size = (17, 1)
        data_size = (10, 1)
        font_size = 12
        
        # Define the layout of the GUI
        layout = [
                    [sg.Text('Surface Station', size=title_size,  font=("Helvetica", 25))],
                    [sg.Column([
                        [sg.Text('AUV Configuration', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Mode', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='mode', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Serial', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='serial', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Motors', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='motors', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Camera', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='camera', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Servos', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='servos', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Sensors', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='sensors', size=data_size,  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Motor Configuration', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Motor Speed Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['motor_speed_max'], size=data_size, key='motor_speed_max',  font=("Helvetica", font_size))],
                        [sg.Text('Motor Speed Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['motor_speed_min'], size=data_size, key='motor_speed_min',  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Camera Configuration', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Camera 1 Res: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_1_resolution'], size=data_size, key='camera_1_resolution',  font=("Helvetica", font_size))],
                        [sg.Text('Camera 2 Res: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_2_resolution'], size=data_size, key='camera_2_resolution',  font=("Helvetica", font_size))],
                        [sg.Text('Camera 1 FPS: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_1_fps'], size=data_size, key='camera_1_fps',  font=("Helvetica", font_size))],
                        [sg.Text('Camera 2 FPS: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_2_fps'], size=data_size, key='camera_2_fps',  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Servo Configuration', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Servo 1 Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_1_min'], size=data_size, key='servo_1_min',  font=("Helvetica", font_size))],
                        [sg.Text('Servo 1 Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_1_max'], size=data_size, key='servo_1_max',  font=("Helvetica", font_size))],
                        [sg.Text('Servo 2 Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_2_min'], size=data_size, key='servo_2_min',  font=("Helvetica", font_size))],
                        [sg.Text('Servo 2 Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_2_max'], size=data_size, key='servo_2_max',  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Sensor Configuration', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Temperature Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['Celsius', 'Fahrenheit'], default_value=self.config['temperature_unit'], size=data_size, key='temperature_unit',  font=("Helvetica", font_size))],
                        [sg.Text('Humidity Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['%', 'g/m3'], default_value=self.config['humidity_unit'], size=data_size, key='humidity_unit',  font=("Helvetica", font_size))],
                        [sg.Text('Voltage Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['V', 'mV'], default_value=self.config['voltage_unit'], size=data_size, key='voltage_unit',  font=("Helvetica", font_size))],
                        [sg.Text('Current Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['A', 'mA'], default_value=self.config['current_unit'], size=data_size, key='current_unit',  font=("Helvetica", font_size))],
                        [sg.Text('IMU Axis Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['imu_axis_min'], size=data_size, key='imu_axis_min',  font=("Helvetica", font_size))],
                        [sg.Text('IMU Axis Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['imu_axis_max'], size=data_size, key='imu_axis_max',  font=("Helvetica", font_size))],
                        [sg.Text('Pressure Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['Pa', 'hPa', 'kPa', 'MPa'], default_value=self.config['pressure_unit'], size=data_size, key='pressure_unit',  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                    ], size=(320, 1080)),
                    sg.Column([
                        [sg.Image('imgs/placeholder.png', key='camera_feed', size=(1280, 720))],
                        [
                            sg.Column([
                                [sg.Text('Orin Status', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='orin_status', size=data_size,  font=("Helvetica", font_size))],
                                [sg.Text('Orin IP Address: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['orin_ip_address'], size=label_size, key='orin_ip_address',  font=("Helvetica", font_size))],
                                [sg.Button('Ping Orin', size=data_size, key='ping_orin', font=("Helvetica", font_size)) , sg.Button('Connect', size=data_size, key='connect_orin', font=("Helvetica", font_size))],
                            ], size=(640, 150)),
                            sg.Column([
                                [sg.Text('Arduino Configuration', size=label_size,  font=("Helvetica", font_size))],
                                [sg.Text('Arduino Serial Port: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['arduino_serial_port'], size=label_size, key='arduino_serial_port',  font=("Helvetica", font_size))],
                                [sg.Text('Arduino Baudrate: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['arduino_baudrate'], size=label_size, key='arduino_baudrate',  font=("Helvetica", font_size))],
                                [sg.Text('Arduino Timeout: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['arduino_timeout'], size=label_size, key='arduino_timeout',  font=("Helvetica", font_size))],
                                [sg.Button('Connect', size=data_size, key='connect_arduino', font=("Helvetica", font_size))],
                            ], size=(640, 150)),
                        ],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Battery 1', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery1', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size)), sg.Text('Battery 3', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery3', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Battery 2', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery2', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size)), sg.Text('Battery 4', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery4', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size))],
                    ], size=(1280, 1080)),
                    sg.Column([
                        [sg.Text('IMU Data', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Roll: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='imu_roll', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Pitch: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='imu_pitch', size=data_size,  font=("Helvetica", font_size))],
                        [sg.Text('Yaw: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='imu_yaw', size=data_size,  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Depth Data', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Depth: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='depth', size=data_size,  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Temperature Data', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Temperature: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='temperature', size=data_size,  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Humidity Data', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Humidity: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='humidity', size=data_size,  font=("Helvetica", font_size))],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Motor Data', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Motor 1: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor1_progress')],
                        [sg.Text('Motor 2: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor2_progress')],
                        [sg.Text('Motor 3: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor3_progress')],
                        [sg.Text('Motor 4: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor4_progress')],
                        [sg.Text('Motor 5: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor5_progress')],
                        [sg.Text('Motor 6: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor6_progress')],
                        [sg.Text('Motor 7: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor7_progress')],
                        [sg.Text('Motor 8: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor8_progress')],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Servo Data', size=label_size,  font=("Helvetica", font_size))],
                        [sg.Text('Servo 1: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='servo1_progress')],
                        [sg.Text('Servo 2: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='servo2_progress')],
                        [sg.Text('Servo 3: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='servo3_progress')],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Acoustics Data', size=label_size,  font=("Helvetica", font_size))]
                    ], size=(320, 1080)),
                    ],  
                ]
        
        self.window = sg.Window('KSU Control Panel', layout, size=(1920, 1080), finalize=True)
        self.window.Maximize()
    def generate_text(self, text, key, mode="display"):
        font = ("Helvetica", self.font_size)
        if mode == "display":
            return [sg.Text(text, size=self.data_label_size, font=font), sg.Text('0', key=key, size=self.data_size, font=font)]
        elif mode == "input":
            return [sg.Text(text, size=self.data_label_size, font=font), sg.InputText(self.config[key], size=self.data_size, key=key, font=font)]
        elif mode == "combo":
            return [sg.Text(text, size=self.data_label_size, font=font), sg.Combo(['Celsius', 'Fahrenheit'], default_value=self.config[key], size=self.data_size, key=key, font=font)]

    def generate_section(self, section_title, keys, mode="display"):
        section = [[sg.Text(section_title, size=self.label_size,  font=("Helvetica", self.font_size))]]
        for key in keys:
            section.append(self.generate_text(key + ": ", key, mode))
        section.append([sg.HorizontalSeparator()])
        return section

    def generate_progress(self, section_title, keys):
        section = [[sg.Text(section_title, size=self.label_size, font=("Helvetica", self.font_size))]]
        for key in keys:
            section.append([sg.Text(key + ": ", size=self.data_label_size, font=("Helvetica", self.font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key=key + '_progress')])
        section.append([sg.HorizontalSeparator()])
        return section
    
    def ping_orin(self):
        pass
    
    def ssh_orin(self):
        pass
    
    def run(self):
        pass