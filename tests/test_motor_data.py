import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

PWM = []
Force = []

with open('data/T200_Data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        PWM.append(int(row[0]))
        Force.append(float(row[1]))

# Define the form of the polynomial function (e.g., second-degree polynomial)
def func(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

# Perform the curve fit
params, params_covariance = curve_fit(func, PWM, Force)

# Print the parameters
print('Function parameters:', params)

# Generate the polynomial equation
a, b, c, d = params
equation = f"f(x) = {a:.6f}x³ + {b:.6f}x² + {c:.6f}x + {d:.6f}"

print('Equation:', equation)

def create_mixing_matrix():
    thruster_configurations = [
        {'position': [0.2, 0, 0], 'orientation': [np.cos(np.pi/4), np.sin(np.pi/4), 0]},  # M1
        {'position': [-0.2, 0, 0], 'orientation': [-np.cos(np.pi/4), np.sin(np.pi/4), 0]}, # M2
        {'position': [-0.2, 0, 0], 'orientation': [-np.cos(np.pi/4), -np.sin(np.pi/4), 0]}, # M3
        {'position': [0.2, 0, 0], 'orientation': [np.cos(np.pi/4), -np.sin(np.pi/4), 0]},  # M4
        {'position': [0.2, 0, -0.2], 'orientation': [0, 0, -1]},  # M5
        {'position': [-0.2, 0, -0.2], 'orientation': [0, 0, -1]}, # M6
        {'position': [-0.2, 0, 0.2], 'orientation': [0, 0, 1]},   # M7
        {'position': [0.2, 0, 0.2], 'orientation': [0, 0, 1]},    # M8
    ]

    mixing_matrix = np.zeros((8, 6))

    for i, config in enumerate(thruster_configurations):
        r = np.array(config['position'])
        d = np.array(config['orientation'])

        mixing_matrix[i, :3] = d
        mixing_matrix[i, 3:] = np.cross(r, d)

    return mixing_matrix

def compute_thruster_commands(mixing_matrix, desired_forces_and_torques):
    # Use the mixing matrix directly to compute the thruster commands
    # necessary to achieve the desired forces and torques
    thruster_commands = mixing_matrix.dot(desired_forces_and_torques)
    return thruster_commands

# Create the mixing matrix using the function
mixing_matrix = create_mixing_matrix()

# Print the shape of the mixing matrix to verify its dimensions
print("Mixing Matrix Shape:", mixing_matrix.shape)

# Define the desired forces and torques (replace with your actual values)
# These are the inputs to the plant (Out of the PID controller for each axis)
desired_forces_and_torques = np.array([0, 0, 0, 0, 0, 0])

# Compute the thruster commands
thruster_commands = compute_thruster_commands(mixing_matrix, desired_forces_and_torques)

# Print the thruster commands
print("Thruster Commands:", thruster_commands)
