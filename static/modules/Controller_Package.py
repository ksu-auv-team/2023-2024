import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, request, jsonify

class Controller:
    def __init__(self, controller_logger : logging.Logger, db : SQLAlchemy, InputControlDB : db.Model):
        self.controller_logger = controller_logger
        self.db = db
        self.InputControlDB = InputControlDB
        self.controller_logger.info('Controller Package initialized')
        
    def get_data(self):
        """
        Extracts data from the HTTP POST request.
        """
        self.controller_logger.info('Getting data from HTTP POST request')
        return request.json

    def parse_data(self, data):
        """
        Parses the data from the request. Adjust this as per your data structure.
        """
        # Example: Expecting data to be a dictionary with specific keys
        self.controller_logger.info('Parsing data from HTTP POST request')
        return {
            'X': data.get('X'),
            'Y': data.get('Y'),
            'Z': data.get('Z'),
            'Pitch': data.get('Pitch'),
            'Roll': data.get('Roll'),
            'Yaw': data.get('Yaw'),
            'Claw': data.get('Claw')
        }

    def save_data(self, data):
        """
        Saves the data to the database.
        """
        control_data = self.InputControlDB(
            Date=datetime.utcnow(),
            X=data['X'], 
            Y=data['Y'], 
            Z=data['Z'], 
            Pitch=data['Pitch'], 
            Roll=data['Roll'], 
            Yaw=data['Yaw'], 
            Claw=data['Claw']
        )
        self.controller_logger.info(f'Saving data: {control_data}')
        self.db.session.add(control_data)
        self.db.session.commit()

    def delete_data(self):
        """
        Deletes all data from the database (be cautious with this).
        """
        self.controller_logger.info('Deleting all data from database')
        self.InputControlDB.query.delete()
        self.db.session.commit()
