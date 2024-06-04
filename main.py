"""
    Main file for the project.
    For now this script handles the backend subprocesses of the project.
    Four sub-processes are handles:
        - Hardware Interface
        - Movement Package
        - Neural Network Package
        - Web Interface

    These four sub-processes will be run in parallel to each other and communicate via the custom database system.

    The main script will be responsible for handling the communication between the sub-processes and the handling of the state machine.
    The state machine will be responsible for the overall control of the project.
"""

# Importing the necessary libraries
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import subprocess
import argparse
import time
import sys
import os

# Creating the custom logger
import logging
logging.basicConfig(
    filename='logs/main.log',      # Name of the log file
    filemode='a',            # Append mode (use 'w' for overwrite each time)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
    level=logging.INFO       # Minimum log level to record
)

# Creating the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///KSUAUV.db'  # Adjust for your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set the upload folder relative to the current script's directory
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voltage1 = db.Column(db.Float, nullable=True)
    voltage2 = db.Column(db.Float, nullable=True)
    voltage3 = db.Column(db.Float, nullable=True)
    current1 = db.Column(db.Float, nullable=True)
    current2 = db.Column(db.Float, nullable=True)
    current3 = db.Column(db.Float, nullable=True)
    error = db.Column(db.Integer, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    X = db.Column(db.Float, nullable=True)
    Y = db.Column(db.Float, nullable=True)
    Z = db.Column(db.Float, nullable=True)
    pitch = db.Column(db.Float, nullable=True)
    roll = db.Column(db.Float, nullable=True)
    yaw = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    orin_temp = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    heading = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f'<{self.id}, {self.voltage1}, {self.voltage2}, \
                  {self.volage3}, {self.current1}, {self.current2}, \
                  {self.current3}, {self.depth}, {self.X}, \
                  {self.Y}, {self.Z}, {self.pitch}, \
                  {self.roll}, {self.yaw}, {self.temperature}, \
                  {self.orin_temp}, {self.humidity}, {self.heading}>'

class Output(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    M1 = db.Column(db.Integer, nullable=False)
    M2 = db.Column(db.Integer, nullable=False)
    M3 = db.Column(db.Integer, nullable=False)
    M4 = db.Column(db.Integer, nullable=False)
    M5 = db.Column(db.Integer, nullable=False)
    M6 = db.Column(db.Integer, nullable=False)
    M7 = db.Column(db.Integer, nullable=False)
    M8 = db.Column(db.Integer, nullable=False)
    Claw = db.Column(db.Integer, nullable=False)
    Torp1 = db.Column(db.Boolean, nullable=False)
    Torp2 = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<{self.id}, {self.M1}, {self.M2}, \
                  {self.M3}, {self.M4}, {self.M5}, \
                  {self.M6}, {self.M7}, {self.M8}, \
                  {self.Claw}, {self.Torp1}, {self.Torp2}>'

class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    pitch = db.Column(db.Float, nullable=False)
    roll = db.Column(db.Float, nullable=False)
    yaw = db.Column(db.Float, nullable=False)
    claw = db.Column(db.Integer, nullable=False)
    torp1 = db.Column(db.Boolean, nullable=False)
    torp2 = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<{self.id}, {self.X}, {self.Y}, \
                  {self.Z}, {self.pitch}, {self.roll}, \
                  {self.yaw}, {self.claw}, {self.torp1}, \
                  {self.torp2}>'
                  
class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    angle = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<{self.id}, {self.object}, {self.distance}, {self.angle}>'

# Creating the flask routes to handle the data
@app.route('/sensors', methods=['POST'])
def add_sensor_data():
    data = request.get_json()

    new_sensor_data = Sensors(voltage1=data['voltage1'], voltage2=data['voltage2'], voltage3=data['voltage3'],
                              current1=data['current1'], current2=data['current2'], current3=data['current3'],
                              depth=data['depth'], X=data['X'], Y=data['Y'], Z=data['Z'],
                              pitch=data['pitch'], roll=data['roll'], yaw=data['yaw'],
                              temperature=data['temperature'], orin_temp=data['orin_temp'], humidity=data['humidity'],
                              heading=data['heading'])

    db.session.add(new_sensor_data)
    db.session.commit()

    return 'Data added', 201

@app.route('/sensors', methods=['GET'])
def get_sensor_data():
    sensor_data = Sensors.query.order_by(Sensors.id.desc()).first()
    if sensor_data:
        data_dict = {
            'voltage1': sensor_data.voltage1, 'voltage2': sensor_data.voltage2, 'voltage3': sensor_data.voltage3,
            'current1': sensor_data.current1, 'current2': sensor_data.current2, 'current3': sensor_data.current3,
            'depth': sensor_data.depth, 'X': sensor_data.X, 'Y': sensor_data.Y, 'Z': sensor_data.Z,
            'pitch': sensor_data.pitch, 'roll': sensor_data.roll, 'yaw': sensor_data.yaw,
            'temperature': sensor_data.temperature, 'orin_temp': sensor_data.orin_temp, 'humidity': sensor_data.humidity,
            'heading': sensor_data.heading
        }
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/output', methods=['POST'])
def add_output_data():
    data = request.get_json()

    new_output_data = Output(M1=data['M1'], M2=data['M2'], M3=data['M3'], M4=data['M4'],
                             M5=data['M5'], M6=data['M6'], M7=data['M7'], M8=data['M8'],
                             Claw=data['Claw'], Torp1=data['Torp1'], Torp2=data['Torp2'])

    db.session.add(new_output_data)
    db.session.commit()

    return 'Data added', 201

@app.route('/output', methods=['GET'])
def get_output_data():
    output_data = Output.query.order_by(Output.id.desc()).first()
    if output_data:
        data_dict = {
            'M1': output_data.M1, 'M2': output_data.M2, 'M3': output_data.M3, 'M4': output_data.M4,
            'M5': output_data.M5, 'M6': output_data.M6, 'M7': output_data.M7, 'M8': output_data.M8,
            'Claw': output_data.Claw, 'Torp1': output_data.Torp1, 'Torp2': output_data.Torp2
        }
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/input', methods=['POST'])
def add_input_data():
    data = request.get_json()

    new_input_data = Input(X=data['X'], Y=data['Y'], Z=data['Z'],
                           pitch=data['Pitch'], roll=data['Roll'], yaw=data['Yaw'],
                           claw=data['Claw'], torp1=data['Torpedo_1'], torp2=data['Torpedo_2'])

    db.session.add(new_input_data)
    db.session.commit()
    # print(new_input_data)

    return 'Data added', 201

@app.route('/input', methods=['GET'])
def get_input_data():
    input_data = Input.query.order_by(Input.id.desc()).first()
    if input_data:
        data_dict = {
            'X': input_data.X, 'Y': input_data.Y, 'Z': input_data.Z,
            'pitch': input_data.pitch, 'roll': input_data.roll, 'yaw': input_data.yaw,
            'claw': input_data.claw, 'torp1': input_data.torp1, 'torp2': input_data.torp2
        }
        # print(data_dict)
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/objects', methods=['POST'])
def add_object_data():
    data = request.get_json()

    new_object_data = Objects(object=data['object'], distance=data['distance'], angle=data['angle'])

    db.session.add(new_object_data)
    db.session.commit()

    return 'Data added', 201

@app.route('/objects', methods=['GET'])
def get_object_data():
    object_data = Objects.query.order_by(Objects.id.desc()).first()
    if object_data:
        data_dict = {
            'object': object_data.object, 
            'distance': object_data.distance, 
            'angle': object_data.angle
        }
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/upload', methods=['POST'])
def upload():
    for filename in request.files:
        file = request.files[filename]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
    return 'Images uploaded', 200

@app.route('/images/<filename>')
def images(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

def create_tables():
    db.create_all()

# Main function
def main(args: list = sys.argv):
    if args.run:
        if args.P:
            hardware_interface = subprocess.Popen(["python3", "modules/HardwareInterface.py", '--P'])
            movement_package = subprocess.Popen(["python3", "modules/MovementPackage.py", '--P'])
            neural_network = subprocess.Popen(["python3", "modules/NeuralNetwork.py", '--P'])
            state_machine = subprocess.Popen(["python3", "modules/StateMachine.py", '-PL'])
            camera_package = subprocess.Popen(["python3", "modules/CameraPackage.py", '--P'])

        hardware_interface = subprocess.Popen(["python3", "modules/HardwareInterface.py", '--L'])
        movement_package = subprocess.Popen(["python3", "modules/MovementPackage.py", '--L'])
        neural_network = subprocess.Popen(["python3", "modules/NeuralNetwork.py", '--L'])
        state_machine = subprocess.Popen(["python3", "modules/StateMachine.py", '--L'])
        camera_package = subprocess.Popen(["python3", "modules/CameraPackage.py", '--L'])
    if args.HI and not args.run:
        if args.P:
            hardware_interface = subprocess.Popen(["python3", "modules/HardwareInterface.py", '--P'])
        hardware_interface = subprocess.Popen(["python3", "modules/HardwareInterface.py", '--L'])
    if args.MP and not args.run:
        if args.P:
            movement_package = subprocess.Popen(["python3", "modules/MovementPackage.py", '--P'])
        movement_package = subprocess.Popen(["python3", "modules/MovementPackage.py", '--L'])
    if args.NN and not args.run:
        if args.P: 
            neural_network = subprocess.Popen(["python3", "modules/NeuralNetwork.py", '--P'])
        neural_network = subprocess.Popen(["python3", "modules/NeuralNetwork.py", '--L'])
    if args.SM and not args.run:
        if args.P:
            state_machine = subprocess.Popen(["python3", "modules/StateMachine.py", '--P'])
        state_machine = subprocess.Popen(["python3", "modules/StateMachine.py", '--L'])
    if args.CP and not args.run:
        if args.P:
            camera_package = subprocess.Popen(["python3", "modules/CameraPackage.py", '--P'])
        camera_package = subprocess.Popen(["python3", "modules/CameraPackage.py", '--L'])
    if not args.run and not args.HI and not args.MP and not args.NN and not args.SM and not (args.P or args.L):
        print("No arguments provided. Please provide an argument to run the main script.")
        print("Use the -h flag for more information.")
        print("Exiting...")
        exit(1)

    with app.app_context():
        create_tables()
    app.run(debug=True, host="0.0.0.0", port=5000)

    if args.run:
        hardware_interface.wait()
        movement_package.wait()
        neural_network.wait()
        state_machine.wait()
        camera_package.wait()
    if args.HI and not args.run:
        hardware_interface.wait()
    if args.MP and not args.run:
        movement_package.wait()
    if args.NN and not args.run:
        neural_network.wait()
    if args.SM and not args.run:
        state_machine.wait()
    if args.CP and not args.run:
        camera_package.wait()

# Running the main function
if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--run", help="Run all the main script", action="store_true")
    args.add_argument("--HI", help="Run the Hardware Interface", action="store_true")
    args.add_argument("--MP", help="Run the Movement Package", action="store_true")
    args.add_argument("--NN", help="Run the Neural Network Package", action="store_true")
    args.add_argument("--SM", help="Run the State Machine", action="store_true")
    args.add_argument("--CP", help="Run the Camera Package", action="store_true")
    args.add_argument("--P", help = "Use the pool IP address", action = "store_true")
    args.add_argument("--L", help = "Use the lab IP address", action = "store_true")

    args = args.parse_args()

    main(args)
