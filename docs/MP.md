# MP Class Documentation

## Overview

The `MP` class provides a model for simulating the thruster configuration and controls for a motion platform, specifically tailored for Autonomous Underwater Vehicles (AUVs). It comes with two types of thruster matrices, one for real-world operation and another for simulation. It also provides functionalities to update thruster outputs based on desired vehicle movements, map the thruster data to specific output ranges, and print out the current thruster data.

---

## Table of Contents

1. [Initialization](#Initialization)
2. [Methods](#Methods)
    1. [create_thruster_matrix_real_world](#create_thruster_matrix_real_world)
    2. [create_thruster_matrix_simulation](#create_thruster_matrix_simulation)
    3. [update](#update)
    4. [map_data](#map_data)
    5. [print_out](#print_out)
    6. [run](#run)
3. [Examples](#Examples)

---

## Initialization

### `__init__(self, simulation=False)`

Initializes the `MP` class, and sets up the appropriate thruster matrix for either real-world operation or simulation based on the `simulation` parameter.

**Parameters:**

- `simulation (bool)`: Specifies whether to initialize the real-world or simulation thruster matrix. Default is `False` for real-world operation.

**Example:**

```python
mp = MP(simulation=True)
```

---

## Methods

### `create_thruster_matrix_real_world()`

Returns a thruster matrix for real-world operation.

**Returns:**

- `np.array`: The real-world thruster matrix.

### `create_thruster_matrix_simulation()`

Returns a thruster matrix for simulation.

**Returns:**

- `np.array`: The simulation thruster matrix.

### `update(self, data)`

Updates the thruster outputs based on desired vehicle movements.

**Parameters:**

- `data (list)`: A list of desired movements in the form of [X, Y, Z, Roll, Pitch, Yaw].

**Returns:**

- `np.array`: The updated thruster outputs.

### `map_data()`

Maps the thruster outputs to a specific range. Useful for transforming thruster values to PWM signals.

**Returns:**

- `np.array`: The mapped thruster outputs.

### `print_out()`

Prints out the current thruster outputs.

### `run()`

Runs the main loop, prompting the user for movement data and updating the thruster outputs accordingly.

---

## Examples

### Example 1: Create an MP object for simulation

```python
mp = MP(simulation=True)
```

### Example 2: Update thruster data

```python
mp.update([1, 0, 0, 0, 0, 0])
```

### Example 3: Print the current thruster outputs

```python
mp.print_out()
```

### Example 4: Run the main loop

```python
if __name__ == "__main__":
    mp = MP()
    mp.run()
```

In this example, the program will continuously prompt the user to enter the desired movements. After entering the values, the updated thruster outputs will be printed to the console.

By following this documentation, you can efficiently utilize the `MP` class for modeling the thruster configurations and controls of AUVs.