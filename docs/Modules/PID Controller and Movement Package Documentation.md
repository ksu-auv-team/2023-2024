## Overview
This software consists of two main components:
1. **PID Controller**: A simple proportional-integral-derivative (PID) controller implemented as a Python class.
2. **Movement Package**: A class that handles the generation of motor and claw commands based on controller input or neural network output. It uses HTTP requests to fetch input and sensor data and to send output data.
## Dependencies
The following libraries are required to run this software:
- `time`: For handling time-related functions.
- `logging`: For logging information, errors, and debugging messages.
- `numpy`: For numerical operations and matrix handling.
- `requests`: For making HTTP requests to fetch and send data.
- `json`: For handling JSON data.
- `datetime`: For handling date and time.
- `argparse`: For handling command-line arguments.
## PID Controller
The PID controller is a control loop feedback mechanism widely used in industrial control systems. It calculates an error value as the difference between a desired setpoint and a measured process variable and applies a correction based on proportional, integral, and derivative terms.
### PID Class
#### Initialization
```python
class PID(object):
    def __init__(
        self,
        Kp=1.0,
        Ki=0.0,
        Kd=0.0,
        setpoint=0,
        sample_time=0.01,
        output_limits=(None, None),
        auto_mode=True,
        proportional_on_measurement=False,
        differential_on_measurement=True,
        error_map=None,
        time_fn=None,
        starting_output=0.0,
    ):
        # Initialization code here
```
- `Kp`: Proportional gain.
- `Ki`: Integral gain.
- `Kd`: Derivative gain.
- `setpoint`: Desired target value.
- `sample_time`: Time in seconds between updates.
- `output_limits`: Tuple specifying the lower and upper limits of the output.
- `auto_mode`: Enables or disables the controller.
- `proportional_on_measurement`: If `True`, the proportional term is calculated on the input.
- `differential_on_measurement`: If `True`, the differential term is calculated on the input.
- `error_map`: Function to transform the error value.
- `time_fn`: Function to get the current time.
- `starting_output`: Initial output value.
#### Methods
- `__call__(input_, dt=None)`: Updates the PID controller and returns the control output.
- `reset()`: Resets the controller internals.
- `set_auto_mode(enabled, last_output=None)`: Enables or disables the controller.
- `components`: Returns the P, I, and D terms.
- `tunings`: Gets or sets the PID tunings.
- `output_limits`: Gets or sets the output limits.
#### Detailed Method Descriptions
**`__call__` Method**
```python
def __call__(self, input_, dt=None):
    """
    Update the PID controller.

    Call the PID controller with *input_* and calculate and return a control output if
    sample_time seconds have passed since the last update. If no new output is calculated,
    return the previous output instead (or None if no value has been calculated yet).

    :param dt: If set, uses this value for timestep instead of real time. This can be used in
        simulations when simulation time is different from real time.
    """
    if not self.auto_mode:
        return self._last_output

    now = self.time_fn()
    if dt is None:
        dt = now - self._last_time if (now - self._last_time) else 1e-16
    elif dt <= 0:
        raise ValueError('dt has negative value {}, must be positive'.format(dt))

    if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
        # Only update every sample_time seconds
        return self._last_output

    # Compute error terms
    error = self.setpoint - input_
    d_input = input_ - (self._last_input if (self._last_input is not None) else input_)
    d_error = error - (self._last_error if (self._last_error is not None) else error)

    # Check if must map the error
    if self.error_map is not None:
        error = self.error_map(error)

    # Compute the proportional term
    if not self.proportional_on_measurement:
        # Regular proportional-on-error, simply set the proportional term
        self._proportional = self.Kp * error
    else:
        # Add the proportional error on measurement to error_sum
        self._proportional -= self.Kp * d_input

    # Compute integral and derivative terms
    self._integral += self.Ki * error * dt
    self._integral = _clamp(self._integral, self.output_limits)  # Avoid integral windup

    if self.differential_on_measurement:
        self._derivative = -self.Kd * d_input / dt
    else:
        self._derivative = self.Kd * d_error / dt

    # Compute final output
    output = self._proportional + self._integral + self._derivative
    output = _clamp(output, self.output_limits)

    # Keep track of state
    self._last_output = output
    self._last_input = input_
    self._last_error = error
    self._last_time = now

    return output
```
**`reset` Method**
```python
def reset(self):
    """
    Reset the PID controller internals.

    This sets each term to 0 as well as clearing the integral, the last output, and the last
    input (derivative calculation).
    """
    self._proportional = 0
    self._integral = 0
    self._derivative = 0

    self._integral = _clamp(self._integral, self.output_limits)

    self._last_time = self.time_fn()
    self._last_output = None
    self._last_input = None
```
**`set_auto_mode` Method**
```python
def set_auto_mode(self, enabled, last_output=None):
    """
    Enable or disable the PID controller, optionally setting the last output value.

    This is useful if some system has been manually controlled and if the PID should take over.
    In that case, disable the PID by setting auto mode to False and later when the PID should
    be turned back on, pass the last output variable (the control variable) and it will be set
    as the starting I-term when the PID is set to auto mode.

    :param enabled: Whether auto mode should be enabled, True or False
    :param last_output: The last output, or the control variable, that the PID should start
        from when going from manual mode to auto mode. Has no effect if the PID is already in
        auto mode.
    """
    if enabled and not self._auto_mode:
        # Switching from manual mode to auto, reset
        self.reset()

        self._integral = last_output if (last_output is not None) else 0
        self._integral = _clamp(self._integral, self.output_limits)

    self._auto_mode = enabled
```
### Example Usage

```python
pid = PID(Kp=2.0, Ki=1.0, Kd=0.5, setpoint=10)
output = pid(8)  # Calculates the control output
```
## Movement Package
The Movement Package class handles the generation of motor and claw commands based on input data. It fetches input and sensor data via HTTP requests and sends output data to a specified URL.
### MovementPackage Class
#### Initialization
```python
class MovementPackage:
    def __init__(self, movement_logger: logging.Logger, base_url: str):
        """
        Movement Package:
        - Handles the generation of motor and claw commands based on either controller input or neural network output.
        - All input and output are handled via HTTP requests.

        :param movement_logger: Logger instance for logging.
        :param base_url: Base URL for HTTP requests.
        """
        self.movement_logger = movement_logger
        self.base_url = base_url
        self.controller_data = {}
        self.neural_network_data = {}
        self.sensors_data = {}
        
        self.in_min = -1
        self.in_max = 1
        self.out_min = 64
        self.out_max = 191
        
        self.Thruster_Values = [127, 127, 127, 127, 127, 127, 127, 127]
```
#### Methods
- `get_sensors_data()`: Fetches sensor data from the server.
- `get_data()`: Fetches input data from the server.
- `convert_to_motor_values(data)`: Converts input data to motor values using PID matrices.
- `newConversion(input_data)`: Placeholder for a new conversion method.
- `save_data()`: Sends motor values to the server.
- `mapping(x)`: Maps input values to the desired range.
- `run()`: Main loop to fetch data, convert it, and send the motor values.
- `test_run()`: Interactive test method for manual input.
#### Detailed Method Descriptions
**`get_sensors_data` Method**
```python
def get_sensors_data(self):
    """
    Fetch sensor data from the server.

    :return: JSON data of the sensors if the request is successful, None otherwise.
    """
    response = requests.get(f"{self.base_url}/sensors")
    if response.status_code == 200:
        return response.json()
    else:
        self.movement_logger.error("Failed to fetch sensors data")
        return None
```
**`get_data` Method**
```python
def get_data(self):
    """
    Fetch input data from the server.

    :return: JSON data of the input if the request is successful, None otherwise.
    """
    response = requests.get(f"{self.base_url}/input")
    if response.status_code == 200:
        return response.json()
    else:
        self.movement_logger.error("Failed to fetch input data")
        return None
```
**`convert_to_motor_values` Method**
```python
def convert_to_motor_values(self, data):
    """
    Convert the received data into motor values using PID matrices.

    :param data: An array representing sensor or controller data
    """
    X = data[0]
    Y = data[1]
    Z = data[2]
    Pitch = data[3]
    Roll = data[4]
    Yaw = data[5]
    
    deadzone = 0.1
    motor_mapping = np.array([[-1, 1, 1, -1], # Forward
                              [-1, -1, 1, 1], # Strafe
                              [-1, 1, -1, 1], # Yaw
                              [-1, 1, 1, -1]]) # Vertical
    
    # Horizontal Motor Mapping
    if abs(X) >= deadzone:
        df = X
        for i in range(0, 4):
            self.Thruster_Values[i] = int(self.mapping(df * motor_mapping[0][i]))
    elif abs(Y) >= deadzone:
        df = Y
        for i in range(0, 4):
            self.Thruster_Values[i] = int(self.mapping(df * motor_mapping[1][i]))
    elif abs(Yaw) >= deadzone:
        df = Yaw
        for i in range(0, 4):
            self.Thruster_Values[i] = int(self.mapping(df * motor_mapping[2][i]))
    else:
        for i in range(4):
            self.Thruster_Values[i] = 127
    
    # Vertical Motor Mapping
    if abs(Z) >= deadzone:
        df = Z
        for i in range(4, 8):
            self.Thruster_Values[i] = int(self.mapping(df * motor_mapping[3][i-4]))
    elif abs(Pitch) >= deadzone:
        df = Pitch
        for i in range(4, 8):
            self.Thruster_Values[i] = int(self.mapping(df))
    elif abs(Roll) >= deadzone:
        df = Roll
        self.Thruster_Values[4] = int(self.mapping(df))
        self.Thruster_Values[5] = int(self.mapping(df * -1))
        self.Thruster_Values[6] = int(self.mapping(df))
        self.Thruster_Values[7] = int(self.mapping(df * -1))
    else:
        for i in range(4, 8):
            self.Thruster_Values[i] = 127
```
**`save_data` Method**
```python
def save_data(self):
    """
    Send motor values to the server.

    :return: None
    """
    output_data = {
        "M1": self.Thruster_Values[0],
        "M2": self.Thruster_Values[1],
        "M3": self.Thruster_Values[2],
        "M4": self.Thruster_Values[3],
        "M5": self.Thruster_Values[4],
        "M6": self.Thruster_Values[5],
        "M7": self.Thruster_Values[6],
        "M8": self.Thruster_Values[7],
        "Claw": 127,
        "Torp1": 0,
        "Torp2": 0
    }
    response = requests.post(f"{self.base_url}/output", json=output_data)
    if response.status_code != 201:
        self.movement_logger.error("Failed to post output data")
```
**`run` Method**
```python
def run(self):
    """
    Main loop to fetch data, convert it, and send the motor values.

    :return: None
    """
    time.sleep(10)
    while True:
        data = self.get_data()
        data = [data["X"], data["Y"], data["Z"], data["Pitch"], data["Roll"], data["Yaw"], data["Claw"], data["Torpedo_1"], data["Torpedo_2"]]
        self.convert_to_motor_values(data)
        self.save_data()
        time.sleep(0.01)
        # self.movement_logger.info(f"Thruster Values: {self.Thruster_Values}")
```
**`test_run` Method**
```python
def test_run(self):
    """
    Interactive test method for manual input.

    :return: None
    """
    while True:
        try:
            input_axis = input("Enter which axis to test (X, Y, Z, pitch, roll, yaw): ")
            input_value = float(input("Enter the value to test: "))
            data = [0, 0, 0, 0, 0, 0]
            if input_axis == "X":
                data[0] = input_value
            elif input_axis == "Y":
                data[1] = input_value
            elif input_axis == "Z":
                data[2] = input_value
            elif input_axis == "Pitch":
                data[3] = input_value
            elif input_axis == "Roll":
                data[4] = input_value
            elif input_axis == "Yaw":
                data[5] = input_value
            else:
                print("Invalid axis")
                continue

            self.convert_to_motor_values(data)
            print(self.Thruster_Values)
        except KeyboardInterrupt as e:
            exit()      
```
### Example Usage
```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler("./logs/movement.log"), logging.StreamHandler()])
    movement_logger = logging.getLogger("MovementPackage")
    movement_logger.setLevel(logging.INFO)
    
    args = argparse.ArgumentParser()
    args.add_argument("--P", help="Use the pool IP address", action="store_true")
    args.add_argument("--L", help="Use the lab IP address", action="store_true")
    args = args.parse_args()
    
    with open('./configs/movement_package.json') as f:
        config = json.load(f)
    
    base_url = "http://192.168.1.246:5000"
    movement_package = MovementPackage(movement_logger, base_url)
    movement_package.run()
```
### `_clamp` Function
```python
def _clamp(value, limits):
    """
    Clamp a value within given limits.

    :param value: The value to clamp.
    :param limits: Tuple containing the lower and upper limits.
    :return: The clamped value.
    """
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value
```
This function is used internally to ensure that values stay within specified bounds. It is particularly useful for preventing integral windup in the PID controller.