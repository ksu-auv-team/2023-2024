import serial
import threading
import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import logging

class HardwarePackage:
    """Class to handle hardware interface and serial communication."""

    def __init__(self, port: str, baudrate: int = 115200, hardware_logger: logging.Logger = None, db: SQLAlchemy = None, SensorsInputDB: db.Model = None, OutputDB: db.Model = None):
        """
        Initialize the HardwarePackage.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.hardware_logger = hardware_logger
        self.db = db
        self.SensorsInputDB = SensorsInputDB
        self.OutputDB = OutputDB
        hardware_logger.info('Hardware Package initialized')

    def run(self):
        """Main method to handle reading from and writing to the serial port."""
        while True:
            self.send_data()
            time.sleep(2)  # Delay between commands
            self.receive_data()

    def receive_data(self):
        """Receive data from the serial port and save it to the database."""
        if self.serial_port.isOpen():
            try:
                data = self.serial_port.readline().decode('utf-8').strip()
                if data:
                    self.hardware_logger.info(f'Received data: {data}')
                    parsed_data = self.parse_data(data)
                    self.save_data(parsed_data)
            except serial.SerialException as e:
                self.hardware_logger.error(f'Serial exception: {e}')

    def parse_data(self, data):
        """Parse the raw data from the serial port."""
        return data.split(',')

    def save_data(self, parsed_data):
        """Save parsed data into the database."""
        if parsed_data and len(parsed_data) >= 6:
            try:
                new_entry = self.SensorsInputDB(
                    Date=datetime.utcnow(),
                    OTemp=float(parsed_data[0]),
                    TTube=float(parsed_data[1]),
                    Depth=float(parsed_data[2]),
                    Humidity=float(parsed_data[3]),
                    Voltage=float(parsed_data[4]),
                    Current=float(parsed_data[5])
                )
                self.db.session.add(new_entry)
                self.db.session.commit()
                self.hardware_logger.info(f'Saving data: {new_entry}')
            except Exception as e:
                self.hardware_logger.error(f'Error saving data: {e}')

    def get_output_data(self):
        """Get the output data from the database."""
        data = self.OutputDB.query.order_by(self.OutputDB.Date.desc()).first()
        if data:
            return f"{data.M1},{data.M2},{data.M3},{data.M4},{data.M5},{data.M6},{data.M7},{data.M8},{data.Claw},{data.SB}\n"
        return ""

    def send_data(self):
        """Send data to the serial port based on database outputs."""
        data = self.get_output_data()
        if self.serial_port.isOpen() and data:
            try:
                self.serial_port.write(data.encode())
                self.hardware_logger.info(f'Sending data: {data}')
            except serial.SerialException as e:
                self.hardware_logger.error(f'Error sending data: {e}')

    def start(self):
        """Start the hardware interface thread."""
        if not self.thread.is_alive():
            self.thread.start()
            self.hardware_logger.info('Hardware interface started')

    def stop(self):
        """Stop the hardware interface."""
        if self.serial_port.isOpen():
            self.serial_port.close()
            self.hardware_logger.info('Hardware interface stopped')
