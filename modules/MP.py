import numpy as np

class MP:
    def __init__(self, simulation=False):
        """
        Initialize the MP class with given parameters.

        Parameters:
            simulation (bool): Determines if the thruster matrix should be
                               set up for a real-world or simulation environment.

        """
        # Define number of thrusters and degrees of freedom
        self.num_thrusters = 8  # Total number of thrusters
        self.num_dof = 6  # Degrees of freedom (X, Y, Z, Roll, Pitch, Yaw)

        # Thruster angle and distance from the center of mass
        self.angle_in_degrees = 45  # Thruster angle in degrees
        self.distance_from_center = 1.0  # Distance from the center of mass to thrusters

        # Convert angle from degrees to radians
        self.angle_in_radians = self.angle_in_degrees * (np.pi / 180)

        # Initialize thruster data array
        self.thruster_data = np.zeros(self.num_thrusters)

        # Create the thruster matrix based on the simulation flag
        if simulation:
            self.thruster_matrix = self.create_thruster_matrix_real_world()
        else:
            self.thruster_matrix = self.create_thruster_matrix_simulation()

    def create_thruster_matrix_real_world(self):
        """
        Create the thruster matrix for a real-world scenario.

        Returns:
            np.ndarray: The real-world thruster matrix.
        """
        # Initialize thruster matrix with zeros
        thruster_matrix = np.zeros((self.num_thrusters, self.num_dof))

        # Compute forces and moments for horizontal thrusters
        for i in range(4):
            angle_adjustment = np.pi if i % 2 == 1 else 0
            d = np.array([np.cos(self.angle_in_radians + angle_adjustment), np.sin(self.angle_in_radians + angle_adjustment), 0])
            m = np.array([0, 0, self.distance_from_center * np.sin(self.angle_in_radians + angle_adjustment)])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        # Configure vertical thrusters for Z-axis, Roll, and Pitch
        for i in range(4, 8):
            d = np.array([0, 0, 1])  # Vertical thrusters only affect Z-axis
            m = np.array([(-1)**((i - 4) // 2) * self.distance_from_center,  (-1)**((i - 4) % 2) * self.distance_from_center, 0])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        return thruster_matrix

    def create_thruster_matrix_simulation(self):
        """
        Create the thruster matrix for a simulated scenario.

        Returns:
            np.ndarray: The simulation thruster matrix.
        """
        # Initialize thruster matrix with zeros
        thruster_matrix = np.zeros((self.num_thrusters, self.num_dof))

        # Compute forces and moments for horizontal thrusters
        for i in range(4):
            angle_adjustment = np.pi if i % 2 == 1 else 0
            d = np.array([np.cos(self.angle_in_radians + angle_adjustment), np.sin(self.angle_in_radians + angle_adjustment), 0])
            m = np.array([0, 0, self.distance_from_center * np.sin(self.angle_in_radians + angle_adjustment)])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        # Configure vertical thrusters for Z-axis, Roll, and Pitch
        for i in range(4, 8):
            d = np.array([0, 0, -1])  # In simulation, vertical thrusters are oriented differently
            m = np.array([(-1)**((i - 4) // 2) * self.distance_from_center,  (-1)**((i - 4) % 2) * self.distance_from_center, 0])
            thruster_matrix[i, :3] = d
            thruster_matrix[i, 3:] = m

        return thruster_matrix

    def update(self, data):
        """
        Update thruster outputs based on desired vehicle movements.

        Parameters:
            data (list): List of desired movements in the 6 DOF.

        Returns:
            np.ndarray: Updated thruster data.
        """
        # Convert input data to a column vector
        data = np.array(data).reshape(-1, 1)

        # Update thruster data based on thruster matrix and input data
        self.thruster_data = np.dot(self.thruster_matrix, data).flatten()

        return self.thruster_data

    def map_data(self):
        """
        Map the thruster outputs to a new range suitable for actuation.

        Returns:
            np.ndarray: Mapped thruster data.
        """
        in_min, in_max = -1, 1  # Input range
        out_min, out_max = 1000, 2000  # Output range

        # Initialize the output data array
        out_data = np.zeros(len(self.thruster_data))

        # Map the thruster data to the new range
        for x in range(len(self.thruster_data)):
            out_data[x] = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

        return out_data

    def print_out(self):
        """
        Print the current thruster outputs.
        """
        print(f'Thruster outputs: {self.thruster_data}')

    def run(self):
        """
        Main loop to run the program. Takes user input for desired movements.
        """
        while True:
            # Read movement data from the user
            data = input("Enter movement data (comma separated, 5 values): ")

            # Convert string data to a list of floats
            data = data.split(',')
            data = [float(i) for i in data]

            # Update and print thruster data
            self.update(data)
            self.print_out()

if __name__ == "__main__":
    mp = MP()
    mp.run()
