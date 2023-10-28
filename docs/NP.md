# NP Class Documentation

The `NP` class is a specialized socket class for sending and receiving NumPy arrays and strings over a socket. This class inherits from Python's built-in `socket.socket` class and extends it by providing methods tailored for NumPy array and string communication.

## Table of Contents
- [NP Class Documentation](#np-class-documentation)
  - [Table of Contents](#table-of-contents)
  - [Installation Requirements](#installation-requirements)
  - [Quick Start](#quick-start)
  - [Methods](#methods)
    - [sendall](#sendall)
    - [send\_string\_as\_bytes](#send_string_as_bytes)
    - [recv](#recv)
    - [recv\_string\_as\_bytes](#recv_string_as_bytes)
    - [accept](#accept)
    - [\_\_pack\_frame (private)](#__pack_frame-private)
  - [Examples](#examples)
    - [Sending and Receiving NumPy Arrays](#sending-and-receiving-numpy-arrays)
    - [Sending and Receiving Strings](#sending-and-receiving-strings)
    - [Handling Multiple Types of Data](#handling-multiple-types-of-data)

---

## Installation Requirements
Before using the `NP` class, make sure you have the following packages installed:

- numpy
- logging

You can install them using pip:

```bash
pip install numpy logging
```

## Quick Start

Here is a quick example of creating an `NP` object and using its methods:

```python
from my_np_class import NP  # Replace 'my_np_class' with the name of your python file
import numpy as np

# Initialize NP object
server_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

# Accepting a new connection
client_socket, client_address = server_socket.accept()

# Sending a numpy array
array_to_send = np.array([1, 2, 3])
client_socket.sendall(array_to_send)

# Receiving a numpy array
received_array = client_socket.recv()

# Closing the sockets
client_socket.close()
server_socket.close()
```

## Methods

### sendall
**Description**: Sends a NumPy array over the socket.

**Arguments**:
- `frame (np.ndarray)`: The NumPy array to send.

**Returns**: None

---

### send_string_as_bytes
**Description**: Sends a string as a byte array over the socket.

**Arguments**:
- `string (str)`: The string to send.

**Returns**: None

---

### recv
**Description**: Receives a NumPy array over the socket.

**Arguments**:
- `bufsize (int, optional)`: The size of the buffer to use for receiving data. Defaults to 1024.

**Returns**:
- `np.ndarray`: The received NumPy array.

---

### recv_string_as_bytes
**Description**: Receives string data in the form of a byte array and returns the string.

**Arguments**:
- `bufsize (int, optional)`: The size of the buffer to use for receiving data. Defaults to 1024.

**Returns**:
- `str`: The received string.

---

### accept
**Description**: Accepts a connection and returns an object of this class (`NP`) instead of `socket.socket`.

**Returns**:
- `tuple`: Tuple containing a new `NP` object and the address of the client.

---

### __pack_frame (private)
**Description**: Packs a NumPy array into a byte array with a header indicating its size.

**Arguments**:
- `frame (np.ndarray)`: The NumPy array to pack.

**Returns**:
- `bytearray`: The packed byte array.

---

## Examples

### Sending and Receiving NumPy Arrays
Server:
```python
server_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

client_socket, client_address = server_socket.accept()
array_to_send = np.array([1, 2, 3])
client_socket.sendall(array_to_send)
```

Client:
```python
client_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

received_array = client_socket.recv()
print(received_array)  # Output should be [1, 2, 3]
```

### Sending and Receiving Strings
Server:
```python
server_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

client_socket, client_address = server_socket.accept()
client_socket.send_string_as_bytes("Hello, client!")
```

Client:
```python
client_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

received_string = client_socket.recv_string_as_bytes()
print(received_string)  # Output should be "Hello, client!"
```

### Handling Multiple Types of Data
Server:
```python
server_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

client_socket, client_address = server_socket.accept()

# Send NumPy array
array_to_send = np.array([1, 2, 3])
client_socket.sendall(array_to_send)

# Send String
client_socket.send_string_as_bytes("Hello, client!")
```

Client:
```python
client_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Receive NumPy array
received_array = client_socket.recv()
print(received_array)  # Output should be [1, 2, 3]

# Receive String
received_string = client_socket.recv_string_as_bytes()
print(received_string)  # Output should be "Hello, client!"
```

Remember to close the sockets once communication is complete.