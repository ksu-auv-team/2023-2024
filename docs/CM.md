# CM Class with Pygame and NumPy

This class, `CM` (Control Mapping), is designed for the purpose of gathering data from an RC flight controller. It makes use of `pygame` to interact with the joystick interface and `NumPy` for efficient data storage. This document describes the various methods and attributes provided by the `CM` class for initializing the joystick and fetching, updating, and printing control data.

## Dependencies
- `pygame`
- `numpy`

## Installation
To install the required dependencies, run the following commands:

```bash
pip install pygame
pip install numpy
```

## How to Run
To use the `CM` class in your code:

1. Initialize a `CM` object.
2. Call its `get_data` and `print` methods within a loop.

## Class Overview

### Class Definition

```python
class CM:
```

### Attributes

- `joystick`: This attribute holds a Pygame Joystick object, which is initialized in the `init_joystick` method.
- `data`: A NumPy array where joystick data is stored.

### Methods

#### `__init__(self, num_of_axis: int = 5)`

This method initializes the `CM` object and calls the `init_joystick` method to initialize the joystick.

**Parameters:**
- `num_of_axis`: The number of axes to initialize in the data array. The default is 5.

#### `init_joystick(self)`

This method initializes the Pygame library and the joystick. It will keep retrying until a joystick is detected.

#### `get_data(self)`

This method updates the `data` array with the latest values from the joystick.

**Returns:**
- `data`: The updated data array.

#### `print(self)`

This method prints the current state of the `data` array.

### Example Usage

Below is a sample program that demonstrates how to use the `CM` class:

```python
if __name__ == "__main__":
    cm = CM()
    while True:
        cm.get_data()
        cm.print()
        pygame.time.wait(10)
```

### Output
Upon running the example code, the output will display the X, Y, Z, Roll, and Yaw values gathered from the joystick. The output will be continuously updated as you interact with the joystick.