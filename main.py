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
from datetime import datetime
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

# Create the database models for image uploads and movement outputs
class ImageUpload(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    img1 = db.Column(db.Bytea, nullable=False)
    img2 = db.Column(db.Bytea, nullable=False)
    img3 = db.Column(db.Bytea, nullable=False)

    def __init__(self, time, img1, img2, img3):
        self.time = time
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3

    def __repr__(self):
        return f"ImageUpload('{self.time}')"

class Output(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    direction = db.Column(db.String(2), nullable=False)
    speed = db.Column(db.Integer, nullable=False)

    def __init__(self, time, output):
        self.time = time
        self.direction = output[0]
        self.speed = output[1]

    def __repr__(self):
        return f"Output('{self.time}')"

# def the route for the image upload
@app.route('/upload', methods=['POST'])
def upload():
    logging.info("Received image upload request")
    # Get the images from the request
    img1 = request.files['img1']
    img2 = request.files['img2']
    img3 = request.files['img3']

    # Save the images to the upload folder
    img1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'img1.jpg'))
    img2.save(os.path.join(app.config['UPLOAD_FOLDER'], 'img2.jpg'))
    img3.save(os.path.join(app.config['UPLOAD_FOLDER'], 'img3.jpg'))

    # Save the images to the database
    new_upload = ImageUpload(time=datetime.now(), img1=img1.read(), img2=img2.read(), img3=img3.read())

    db.session.add(new_upload)
    db.session.commit()

    logging.info("Images saved to database")

    return jsonify({'message': 'Images uploaded successfully'})

# def the route for the movement input
@app.route('/output', methods=['POST'])
def output():
    pass

# def the route for the movement output
@app.route('/output', methods=['GET'])
def get_output():
    pass

@app.route('/')
def index():
    return render_template('index.html')

def create_tables():
    db.create_all()

# Main function
def main(args = sys.argv):
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

# Running the main function
if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--run", help="Run all the main script", action="store_true")
    args.add_argument("--HI", help="Run the Hardware Interface", action="store_true")
    args.add_argument("--MP", help="Run the Movement Package", action="store_true")
    args.add_argument("--NN", help="Run the Neural Network Package", action="store_true")
    args.add_argument("--CP", help="Run the Camera Package", action="store_true")
    args.add_argument("--P", help = "Use the pool IP address", action = "store_true")
    args.add_argument("--L", help = "Use the lab IP address", action = "store_true")

    args = args.parse_args()

    main(args)
