import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, kp, ki, kd, max_output=None, min_output=None):
        """
        Initialize PID Controller.

        :param kp: Proportional gain
        :param ki: Integral gain
        :param kd: Derivative gain
        :param max_output: Optional maximum output value
        :param min_output: Optional minimum output value
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_output = max_output
        self.min_output = min_output
        self.prev_error = 0
        self.integral = 0

    def update(self, error, dt):
        """
        Update the PID controller and compute the control output.

        :param error: Current error value (difference between desired and actual value)
        :param dt: Time step (difference in time between updates)
        :return: Control output
        """
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        if self.max_output is not None:
            output = min(output, self.max_output)
        if self.min_output is not None:
            output = max(output, self.min_output)

        self.prev_error = error
        return output

dt = 0.1
des_x = 0.1 * 100
act_x = 0

count = 0

act_x_values = []
pid_x_values = []
time_values = []

time = 0

while True:
    a = PIDController(1.0, 0.1, 0.01)
    PID_X = a.update(des_x - act_x, dt)
    print(f'Act_X: {act_x:.2f}, PID_X: {PID_X:.2f}')

    act_x_values.append(act_x)
    pid_x_values.append(PID_X)
    time_values.append(time)

    if PID_X <= 0:
        act_x -= 0.1
    else:
        act_x += 0.1

    if act_x - 0.1 <= des_x <= act_x + 0.1:
        count += 1
        if count == 10:
            break

    time += dt

plt.plot(time_values, act_x_values, label='ACT_X')
plt.plot(time_values, pid_x_values, label='PID_X')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()
