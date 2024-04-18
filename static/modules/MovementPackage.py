import logging
import numpy as np
import pandas as pd
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


# PID class
def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value


class PID(object):
    """A simple PID controller."""

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
        """
        Initialize a new PID controller.

        :param Kp: The value for the proportional gain Kp
        :param Ki: The value for the integral gain Ki
        :param Kd: The value for the derivative gain Kd
        :param setpoint: The initial setpoint that the PID will try to achieve
        :param sample_time: The time in seconds which the controller should wait before generating
            a new output value. The PID works best when it is constantly called (eg. during a
            loop), but with a sample time set so that the time difference between each update is
            (close to) constant. If set to None, the PID will compute a new output value every time
            it is called.
        :param output_limits: The initial output limits to use, given as an iterable with 2
            elements, for example: (lower, upper). The output will never go below the lower limit
            or above the upper limit. Either of the limits can also be set to None to have no limit
            in that direction. Setting output limits also avoids integral windup, since the
            integral term will never be allowed to grow outside of the limits.
        :param auto_mode: Whether the controller should be enabled (auto mode) or not (manual mode)
        :param proportional_on_measurement: Whether the proportional term should be calculated on
            the input directly rather than on the error (which is the traditional way). Using
            proportional-on-measurement avoids overshoot for some types of systems.
        :param differential_on_measurement: Whether the differential term should be calculated on
            the input directly rather than on the error (which is the traditional way).
        :param error_map: Function to transform the error value in another constrained value.
        :param time_fn: The function to use for getting the current time, or None to use the
            default. This should be a function taking no arguments and returning a number
            representing the current time. The default is to use time.monotonic() if available,
            otherwise time.time().
        :param starting_output: The starting point for the PID's output. If you start controlling
            a system that is already at the setpoint, you can set this to your best guess at what
            output the PID should give when first calling it to avoid the PID outputting zero and
            moving the system away from the setpoint.
        """
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint
        self.sample_time = sample_time

        self._min_output, self._max_output = None, None
        self._auto_mode = auto_mode
        self.proportional_on_measurement = proportional_on_measurement
        self.differential_on_measurement = differential_on_measurement
        self.error_map = error_map

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = None
        self._last_output = None
        self._last_error = None
        self._last_input = None

        if time_fn is not None:
            # Use the user supplied time function
            self.time_fn = time_fn
        else:
            import time

            try:
                # Get monotonic time to ensure that time deltas are always positive
                self.time_fn = time.monotonic
            except AttributeError:
                # time.monotonic() not available (using python < 3.3), fallback to time.time()
                self.time_fn = time.time

        self.output_limits = output_limits
        self.reset()

        # Set initial state of the controller
        self._integral = _clamp(starting_output, output_limits)

    def __call__(self, input_, dt=None):
        """
        Update the PID controller.

        Call the PID controller with *input_* and calculate and return a control output if
        sample_time seconds has passed since the last update. If no new output is calculated,
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

    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'Kp={self.Kp!r}, Ki={self.Ki!r}, Kd={self.Kd!r}, '
            'setpoint={self.setpoint!r}, sample_time={self.sample_time!r}, '
            'output_limits={self.output_limits!r}, auto_mode={self.auto_mode!r}, '
            'proportional_on_measurement={self.proportional_on_measurement!r}, '
            'differential_on_measurement={self.differential_on_measurement!r}, '
            'error_map={self.error_map!r}'
            ')'
        ).format(self=self)

    @property
    def components(self):
        """
        The P-, I- and D-terms from the last computation as separate components as a tuple. Useful
        for visualizing what the controller is doing or when tuning hard-to-tune systems.
        """
        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):
        """The tunings used by the controller as a tuple: (Kp, Ki, Kd)."""
        return self.Kp, self.Ki, self.Kd

    @tunings.setter
    def tunings(self, tunings):
        """Set the PID tunings."""
        self.Kp, self.Ki, self.Kd = tunings

    @property
    def auto_mode(self):
        """Whether the controller is currently enabled (in auto mode) or not."""
        return self._auto_mode

    @auto_mode.setter
    def auto_mode(self, enabled):
        """Enable or disable the PID controller."""
        self.set_auto_mode(enabled)

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

    @property
    def output_limits(self):
        """
        The current output limits as a 2-tuple: (lower, upper).

        See also the *output_limits* parameter in :meth:`PID.__init__`.
        """
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        """Set the output limits."""
        if limits is None:
            self._min_output, self._max_output = None, None
            return

        min_output, max_output = limits

        if (None not in limits) and (max_output < min_output):
            raise ValueError('lower limit must be less than upper limit')

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        self._last_output = _clamp(self._last_output, self.output_limits)

    def reset(self):
        """
        Reset the PID controller internals.

        This sets each term to 0 as well as clearing the integral, the last output and the last
        input (derivative calculation).
        """
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._integral = _clamp(self._integral, self.output_limits)

        self._last_time = self.time_fn()
        self._last_output = None
        self._last_input = None

class MovementPackage:
    def __init__(self, movement_logger : logging.Logger, db : SQLAlchemy, InputControlDB : SQLAlchemy, OutputControlDB : SQLAlchemy, SensorsInputDB : SQLAlchemy):
        """
        Movement Package:
        - Handles the generation of motor and claw commands based on either controller input or neural network output.
        - All input comes from two databases, and all output is saved to a different database. 
        - The databases are updated every microsecond.
        - 
        """
        self.movement_logger = movement_logger
        self.InputControlDB = InputControlDB
        self.OutputControlDB = OutputControlDB
        self.SensorsInputDB = SensorsInputDB
        self.db = db

        self.PIDs = []
        self.PWM_To_Force_Conversion = {}
        self.controller_data = {}
        self.neural_network_data = {}
        self.sensors_data = {}
        self.output_control_data_part_1 = [1500, 1500, 1500, 1500]
        self.output_control_data_part_2 = [1500, 1500, 1500, 1500]

        d1 = 0.3
        d2 = 0.15
        d3 = 0.2
        dh = np.sqrt(d1**2 + d3**2)
        dv = np.sqrt(d2**2 + d3**2)
        Fx = np.sin(45) * dh
        Fy = np.cos(45) * dv
        Fz = -1
        self.PID_Matrix_1 = np.array([
            [Fx, Fx, Fx, Fx],
            [Fy, Fy, Fy, Fy],
            [dh, dh, dh, dh]
        ]).transpose()
        self.PID_Matrix_2 = np.array([
            [Fz, Fz, Fz, Fz],
            [Fy, -Fy, -Fy, Fy],
            [Fx, -Fx, -Fx, Fx]
        ]).transpose()

        self.initialize_PIDs()
        self.initialize_PWM_To_Force_Conversion()

        self.in_min = -1
        self.in_max = 1
        self.out_min = 1300
        self.out_max = 1700

        self.movement_logger.info('Movement Package initialized')

    def initialize_PIDs(self):
        self.PIDs.append(PID(Kp=1.0, Ki=0.0, Kd=0.0, setpoint=0, sample_time=0.01, output_limits=(None, None), auto_mode=True, proportional_on_measurement=False, differential_on_measurement=True, error_map=None, time_fn=None, starting_output=0.0))
        self.PIDs.append(PID(Kp=1.0, Ki=0.0, Kd=0.0, setpoint=0, sample_time=0.01, output_limits=(None, None), auto_mode=True, proportional_on_measurement=False, differential_on_measurement=True, error_map=None, time_fn=None, starting_output=0.0))

    def initialize_PWM_To_Force_Conversion(self):
        df = pd.read_excel('static/data/T200-PWM-Force-Current.xlsx', engine='openpyxl')
        return df.to_dict()

    def get_sensors_data(self):
        data = self.SensorsInputDB.query.order_by(self.InputControlDB.Date.desc()).first()
        return {
            'Date': data.Date, 'X': data.X, 'Y': data.Y, 'Z': data.Z, 
            'Pitch': data.Pitch, 'Roll': data.Roll, 'Yaw': data.Yaw, 
            'Claw': data.Claw
        }

    def get_data(self):
        data = self.InputControlDB.query.order_by(self.InputControlDB.Date.desc()).first()
        return [data.X, data.Y, data.Z, data.Pitch, data.Roll, data.Yaw]

    def map_data(self, data):
        sensor_value = self.get_sensors_data() # Comes from sensors
        desired_value = [data[0], data[1], data[2], data[3], data[4], data[5]] # Comes from controller

        PID1_desired_data = [desired_value[0], desired_value[1], desired_value[5]]
        PID2_desired_data = [desired_value[2], desired_value[3], desired_value[4]]

        max_desired_PID1_index = max.index(PID1_desired_data)
        max_desired_PID2_index = max.index(PID2_desired_data)

        self.PIDs[0].setpoint = max(PID1_desired_data)
        self.PIDs[1].setpoint = max(PID2_desired_data)

        PID1_sensor_data = [sensor_value[0], sensor_value[1], sensor_value[5]]
        PID2_sensor_data = [sensor_value[2], sensor_value[3], sensor_value[4]]

        PID1_output = self.PIDs[0](PID1_sensor_data)
        PID2_output = self.PIDs[1](PID2_sensor_data)

        for i in range(4):
            self.output_control_data_part_1[i] = self.mapping(self.PID_Matrix_1[max_desired_PID1_index][i] * PID1_output)
            self.output_control_data_part_2[i] = self.mapping(self.PID_Matrix_2[max_desired_PID2_index][i] * PID2_output)
        
        self.save_data(self.output_control_data_part_1, self.output_control_data_part_2, data[6])

    def save_data(self, data1, data2, data3):
        output_data = self.OutputControlDB(
            Date=datetime.now()(),
            M1=self.mapping(data1[0]),
            M2=self.mapping(data1[1]),
            M3=self.mapping(data1[2]),
            M4=self.mapping(data1[3]),
            M5=self.mapping(data2[0]),
            M6=self.mapping(data2[1]),
            M7=self.mapping(data2[2]),
            M8=self.mapping(data2[3]),
            Claw=data3
        )
        self.db.session.add(output_data)
        self.db.session.commit()

    def delete_data(self):
        self.OutputControlDB.query.delete()
        self.db.session.commit()

    def mapping(self, x):
        return (x - self.in_min) * (self.out_max - self.out_min) / (self.in_max - self.in_min) + self.out_min