import serial
import threading
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from logging.handlers import RotatingFileHandler
import logging

db = SQLAlchemy()

class HardwarePackage:
    """Class to handle hardware interface and serial communication."""

    def __init__(self, port : str, baudrate : int = 9600, hardware_logger : logging.Logger = None, db : SQLAlchemy = None, SensorsInputDB : db.Model = None, OutputDB : db.Model = None):
        """
        Initialize the HardwarePackage.

        Args:
            port (str): Serial port to use.
            baudrate (int): Baud rate for serial communication.
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.thread = threading.Thread(target=self.read_from_serial)
        self.thread.daemon = True

        self.hardware_logger = hardware_logger
        self.db = db
        self.SensorsInputDB = SensorsInputDB
        self.OutputOutputDB = OutputDB

        hardware_logger.info('Hardware Package initialized')

    def read_from_serial(self):
        """Continuously read data from the serial port and process it."""
        while True:
            data = self.get_data()
            if data:
                parsed_data = self.parse_data(data)
                self.save_data(parsed_data)
                self.hardware_logger.info(f"Received data: {parsed_data}")

    def get_data(self):
        """
        Read data from the serial port.

        Returns:
            str: The read data, or None if there's an error or if the port is closed.
        """
        if self.ser.isOpen():
            try:
                self.hardware_logger.info('Reading data from serial port')
                return self.ser.readline().decode('utf-8').strip()
            except serial.SerialException:
                return None
        return None

    def parse_data(self, data):
        """
        Parse the raw data from the serial port.

        Args:
            data (str): Raw data string from the serial port.

        Returns:
            list: Parsed data as a list of values.
        """
        return data.split(',')

    def save_data(self, parsed_data):
        """
        Save parsed data into the database.

        Args:
            parsed_data (list): Parsed data to be saved.
        """
        new_entry = self.SensorsInputDB(
            Date=datetime.utcnow(),
            OTemp=float(parsed_data[15]),
            TTube=float(parsed_data[16]),
            Depth=float(parsed_data[17]),
            Humidity=float(parsed_data[18]),
            Voltage=float(parsed_data[19]),
            Current=float(parsed_data[20])
        )
        self.hardware_logger.info(f"Saving data: {new_entry}")
        self.db.session.add(new_entry)
        self.db.session.commit()

    def get_output_data(self):
        """
        Get the output data from the database.

        Returns:
            str: The output data as a string.
        """
        data = self.OutputDB.query.order_by(self.OutputDB.Date.desc()).first()
        return [data.M1, data.M2, data.M3, data.M4, data.M5, data.M6, data.M7, data.M8, data.Claw, data.SB]
    
    def send_data(self):
        """
        Send data to the serial port.

        Args:
            data (str): Data to be sent to the serial device.
        """
        if self.ser.isOpen():
            try:
                data = self.get_output_data()
                self.hardware_logger.info(f"Sending data: {data}")
                self.ser.write(data.encode())
            except serial.SerialException:
                pass

    def start(self):
        """Start the hardware interface."""
        if not self.thread.is_alive():
            self.hardware_logger.info('Starting hardware interface')
            self.thread.start()


    def stop(self):
        """Stop the hardware interface."""
        if self.ser.isOpen():
            self.hardware_logger.info('Stopping hardware interface')
            self.ser.close()