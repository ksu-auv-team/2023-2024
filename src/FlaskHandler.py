from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import argparse
import logging
import os

# Create the logs directory if it doesn't exist
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Set up the log file path and configure logging
log_file = os.path.join(log_folder, 'application.log')
logging.basicConfig(
    filename=log_file, 
    level=logging.DEBUG,  # Use DEBUG level to capture debug logs
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Set Flask's logger to use the same settings as the root logger
app.logger.setLevel(logging.DEBUG)

# Define the database models
class Inputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    X = db.Column(db.Integer, nullable=False)
    Y = db.Column(db.Integer, nullable=False)
    Z = db.Column(db.Integer, nullable=False)
    Roll = db.Column(db.Integer, nullable=False)
    Pitch = db.Column(db.Integer, nullable=False)
    Yaw = db.Column(db.Integer, nullable=False)
    Torp1 = db.Column(db.Integer, nullable=False)
    Torp2 = db.Column(db.Integer, nullable=False)
    Claw = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Inputs('{self.X}', '{self.Y}', '{self.Z}', '{self.Roll}', '{self.Pitch}', '{self.Yaw}', '{self.Torp1}', '{self.Torp2}', '{self.Claw}')"

class Outputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    M1 = db.Column(db.Integer, nullable=False)
    M2 = db.Column(db.Integer, nullable=False)
    M3 = db.Column(db.Integer, nullable=False)
    M4 = db.Column(db.Integer, nullable=False)
    M5 = db.Column(db.Integer, nullable=False)
    M6 = db.Column(db.Integer, nullable=False)
    M7 = db.Column(db.Integer, nullable=False)
    M8 = db.Column(db.Integer, nullable=False)
    Torp1 = db.Column(db.Integer, nullable=False)
    Torp2 = db.Column(db.Integer, nullable=False)
    Claw = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Outputs('{self.M1}', '{self.M2}', '{self.M3}', '{self.M4}', '{self.M5}', '{self.M6}', '{self.M7}', '{self.M8}', '{self.Torp1}', '{self.Torp2}', '{self.Claw}')"

class Sonar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Distance = db.Column(db.Integer, nullable=False)
    Angle = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Sonar('{self.Distance}', '{self.Angle}')"

class Batteries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Voltage1 = db.Column(db.Integer, nullable=False)
    Voltage2 = db.Column(db.Integer, nullable=False)
    Voltage3 = db.Column(db.Integer, nullable=False)
    Current1 = db.Column(db.Integer, nullable=False)
    Current2 = db.Column(db.Integer, nullable=False)
    Current3 = db.Column(db.Integer, nullable=False)
    Error = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Batteries('{self.Voltage1}', '{self.Voltage2}', '{self.Voltage3}', '{self.Current1}', '{self.Current2}', '{self.Current3}', '{self.Error}')"
    
class IMU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AccelX = db.Column(db.Integer, nullable=False)
    AccelY = db.Column(db.Integer, nullable=False)
    AccelZ = db.Column(db.Integer, nullable=False)
    GyroX = db.Column(db.Integer, nullable=False)
    GyroY = db.Column(db.Integer, nullable=False)
    GyroZ = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"IMU('{self.AccelX}', '{self.AccelY}', '{self.AccelZ}', '{self.GyroX}', '{self.GyroY}', '{self.GyroZ}')"

class Sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Temp = db.Column(db.Integer, nullable=False)
    Humidity = db.Column(db.Integer, nullable=False)
    Pressure = db.Column(db.Integer, nullable=False)
    Depth = db.Column(db.Integer, nullable=False)
    Heading = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Sensors('{self.Temp}', '{self.Humidity}', '{self.Pressure}', '{self.Depth}', '{self.Heading}')"

class Debug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Package = db.Column(db.String(100), nullable=False)
    ErrorType = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.String(300), nullable=False)
    
    def __repr__(self):
        return f"Debug('{self.Package}', '{self.ErrorType}', '{self.Message}')"

# API Endpoints for Inputs
@app.route('/inputs', methods=['GET', 'POST'])
def handle_inputs():
    if request.method == 'POST':
        data = request.get_json()
        new_input = Inputs(X=data['X'], Y=data['Y'], Z=data['Z'], Roll=data['Roll'], 
                           Pitch=data['Pitch'], Yaw=data['Yaw'], Torp1=data['Torp1'], 
                           Torp2=data['Torp2'], Claw=data['Claw'])
        db.session.add(new_input)
        db.session.commit()
        return jsonify({'message': 'New input added'}), 201
    
    if request.method == 'GET':
        latest_input = Inputs.query.order_by(Inputs.id.desc()).first()
        return jsonify({
            'X': latest_input.X,
            'Y': latest_input.Y,
            'Z': latest_input.Z,
            'Roll': latest_input.Roll,
            'Pitch': latest_input.Pitch,
            'Yaw': latest_input.Yaw,
            'Torp1': latest_input.Torp1,
            'Torp2': latest_input.Torp2,
            'Claw': latest_input.Claw
        }), 200

# API Endpoints for Outputs
@app.route('/outputs', methods=['GET', 'POST'])
def handle_outputs():
    if request.method == 'POST':
        data = request.get_json()
        new_output = Outputs(M1=data['M1'], M2=data['M2'], M3=data['M3'], M4=data['M4'], 
                             M5=data['M5'], M6=data['M6'], M7=data['M7'], M8=data['M8'], 
                             Torp1=data['Torp1'], Torp2=data['Torp2'], Claw=data['Claw'])
        db.session.add(new_output)
        db.session.commit()
        return jsonify({'message': 'New output added'}), 201
    
    if request.method == 'GET':
        latest_output = Outputs.query.order_by(Outputs.id.desc()).first()
        return jsonify({
            'M1': latest_output.M1,
            'M2': latest_output.M2,
            'M3': latest_output.M3,
            'M4': latest_output.M4,
            'M5': latest_output.M5,
            'M6': latest_output.M6,
            'M7': latest_output.M7,
            'M8': latest_output.M8,
            'Torp1': latest_output.Torp1,
            'Torp2': latest_output.Torp2,
            'Claw': latest_output.Claw
        }), 200

# API Endpoints for Sonar
@app.route('/sonar', methods=['GET', 'POST'])
def handle_sonar():
    if request.method == 'POST':
        data = request.get_json()
        new_sonar = Sonar(Distance=data['Distance'], Angle=data['Angle'])
        db.session.add(new_sonar)
        db.session.commit()
        return jsonify({'message': 'New sonar reading added'}), 201
    
    if request.method == 'GET':
        latest_sonar = Sonar.query.order_by(Sonar.id.desc()).first()
        return jsonify({
            'Distance': latest_sonar.Distance,
            'Angle': latest_sonar.Angle
        }), 200
        
# API Endpoints for Batteries
@app.route('/batteries', methods=['GET', 'POST'])
def handle_batteries():
    if request.method == 'POST':
        data = request.get_json()
        new_battery = Batteries(Voltage1=data['Voltage1'], Voltage2=data['Voltage2'], 
                                Voltage3=data['Voltage3'], Current1=data['Current1'], 
                                Current2=data['Current2'], Current3=data['Current3'], 
                                Error=data['Error'])
        db.session.add(new_battery)
        db.session.commit()
        return jsonify({'message': 'New battery reading added'}), 201
    
    if request.method == 'GET':
        latest_battery = Batteries.query.order_by(Batteries.id.desc()).first()
        return jsonify({
            'Voltage1': latest_battery.Voltage1,
            'Voltage2': latest_battery.Voltage2,
            'Voltage3': latest_battery.Voltage3,
            'Current1': latest_battery.Current1,
            'Current2': latest_battery.Current2,
            'Current3': latest_battery.Current3,
            'Error': latest_battery.Error
        }), 200
        
# API Endpoints for IMU
@app.route('/imu', methods=['GET', 'POST'])
def handle_imu():
    if request.method == 'POST':
        data = request.get_json()
        new_imu = IMU(AccelX=data['AccelX'], AccelY=data['AccelY'], AccelZ=data['AccelZ'], 
                      GyroX=data['GyroX'], GyroY=data['GyroY'], GyroZ=data['GyroZ'])
        db.session.add(new_imu)
        db.session.commit()
        return jsonify({'message': 'New IMU reading added'}), 201
    
    if request.method == 'GET':
        latest_imu = IMU.query.order_by(IMU.id.desc()).first()
        return jsonify({
            'AccelX': latest_imu.AccelX,
            'AccelY': latest_imu.AccelY,
            'AccelZ': latest_imu.AccelZ,
            'GyroX': latest_imu.GyroX,
            'GyroY': latest_imu.GyroY,
            'GyroZ': latest_imu.GyroZ
        }), 200

# API Endpoints for Sensors
@app.route('/sensors', methods=['GET', 'POST'])
def handle_sensors():
    if request.method == 'POST':
        data = request.get_json()
        new_sensor = Sensors(Temp=data['Temp'], Humidity=data['Humidity'], 
                             Pressure=data['Pressure'], Depth=data['Depth'])
        db.session.add(new_sensor)
        db.session.commit()
        return jsonify({'message': 'New sensor reading added'}), 201
    
    if request.method == 'GET':
        latest_sensor = Sensors.query.order_by(Sensors.id.desc()).first()
        return jsonify({
            'Temp': latest_sensor.Temp,
            'Humidity': latest_sensor.Humidity,
            'Pressure': latest_sensor.Pressure,
            'Depth': latest_sensor.Depth
        }), 200
        
# API Endpoints for Debug
@app.route('/debug', methods=['GET', 'POST'])
def handle_debug():
    if request.method == 'POST':
        data = request.get_json()
        new_debug = Debug(Package=data['Package'], ErrorType=data['ErrorType'], Message=data['Message'])
        db.session.add(new_debug)
        db.session.commit()
        return jsonify({'message': 'New debug message added'}), 201
    
    if request.method == 'GET':
        latest_debug = Debug.query.order_by(Debug.id.desc()).first()
        return jsonify({
            'Package': latest_debug.Package,
            'ErrorType': latest_debug.ErrorType,
            'Message': latest_debug.Message
        }), 200

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the Flask server')
    parser.add_argument('--ip', type=str, default='localhost', help='IP to run the application on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    parser.add_argument('--debug', action='store_true', help='Run the application in debug mode')
    args = parser.parse_args()

    if args.debug:
        app.logger.debug('Debug mode is enabled')
    
    app.run(host=args.ip, port=args.port, debug=args.debug)
