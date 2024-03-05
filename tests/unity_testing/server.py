from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle
from sqlalchemy.types import TypeDecorator, LargeBinary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unity_tests.db'
db = SQLAlchemy(app)

class NumpyArray(TypeDecorator):
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = pickle.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = pickle.loads(value)
        return value

class MotorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m1 = db.Column(db.Float, nullable=False)
    m2 = db.Column(db.Float, nullable=False)
    m3 = db.Column(db.Float, nullable=False)
    m4 = db.Column(db.Float, nullable=False)
    m5 = db.Column(db.Float, nullable=False)
    m6 = db.Column(db.Float, nullable=False)
    m7 = db.Column(db.Float, nullable=False)
    m8 = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<MotorData(m1={self.m1}, m2={self.m2}, ..., m8={self.m8})>"

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front_camera = db.Column(NumpyArray, nullable=False)
    bottom_camera = db.Column(NumpyArray, nullable=False)

    def __repr__(self):
        return f"<ImageData(front_camera={self.front_camera}, bottom_camera={self.bottom_camera})>"

@app.route('/motor_data/latest', methods=['GET'])
def get_latest_motor_data():
    motor_data = MotorData.query.order_by(MotorData.id.desc()).first()
    if motor_data:
        return jsonify({
            'id': motor_data.id,
            'm1': motor_data.m1, 'm2': motor_data.m2,
            'm3': motor_data.m3, 'm4': motor_data.m4,
            'm5': motor_data.m5, 'm6': motor_data.m6,
            'm7': motor_data.m7, 'm8': motor_data.m8
        })
    else:
        return jsonify({'message': 'Motor data not found'}), 404


@app.route('/motor_data', methods=['POST'])
def add_motor_data():
    data = request.get_json()
    new_motor_data = MotorData(
        m1=data['m1'], m2=data['m2'],
        m3=data['m3'], m4=data['m4'],
        m5=data['m5'], m6=data['m6'],
        m7=data['m7'], m8=data['m8']
    )
    db.session.add(new_motor_data)
    db.session.commit()
    app.logger.info(f"Motor data added: {new_motor_data}")
    return jsonify({'message': 'Motor data added successfully'}), 201

@app.route('/image_data/<int:id>', methods=['GET'])
def get_image_data(id):
    image_data = ImageData.query.get(id)
    if image_data:
        # Note: The actual image data is serialized and might need decoding or processing before sending
        return jsonify({'id': image_data.id})
    else:
        return jsonify({'message': 'Image data not found'}), 404

@app.route('/image_data', methods=['POST'])
def add_image_data():
    # Assuming the incoming request contains serialized image data for front and bottom cameras
    data = request.get_json()
    new_image_data = ImageData(
        front_camera=data['front_camera'],  # This data should be appropriately serialized
        bottom_camera=data['bottom_camera']  # This data should be appropriately serialized
    )
    db.session.add(new_image_data)
    db.session.commit()
    return jsonify({'message': 'Image data added successfully'}), 201

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)