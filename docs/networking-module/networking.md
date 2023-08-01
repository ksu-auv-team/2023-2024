# Networking Class

The `Networking` class provides a way to send and receive both numpy arrays and strings over a socket connection. The class is a subclass of the `socket.socket` class, so it also has all the methods and attributes of a standard socket object.

## Usage

You can use the `Networking` class just like you would use a standard socket object, but with the added benefit of being able to send and receive numpy arrays and strings.

```python
server = Networking(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)

while True:
    client, addr = server.accept()
    client.send_numpy(np.array([1, 2, 3, 4, 5]))
    client.send_string('Hello, World!')
    client.close()
```

## Methods

### send_numpy

```python
def send_numpy(self, frame: np.ndarray) -> None
```

This method sends a numpy array over the socket connection. The numpy array is converted to bytes, then sent. If the array is not a valid numpy array, a `TypeError` will be raised. After the array has been sent, a debug log message is created stating that the frame has been sent.

### send_string

```python
def send_string(self, string: str) -> None
```

This method sends a string over the socket connection. The string is converted to bytes, then sent. If the input is not a valid string, a `TypeError` will be raised. After the string has been sent, a debug log message is created stating that the string has been sent.

### recv_numpy

```python
def recv_numpy(self, bufsize: int = 1024) -> np.ndarray
```

This method receives a numpy array from the socket connection. The incoming bytes are converted back into a numpy array and returned. A debug log message is created when a frame is received.

### recv_string

```python
def recv_string(self, bufsize: int = 1024) -> str
```

This method receives a string from the socket connection. The incoming bytes are converted back into a string and returned. A debug log message is created when a string is received.

### accept

```python
def accept(self) -> tuple
```

This method overrides the accept() method from the `socket` class. It returns a new socket object and the address of the client. The new socket object is of the `Networking` class.

## Private Methods

### __pack_frame

```python
def __pack_frame(frame: np.ndarray) -> bytearray
```

This private method is used to convert a numpy array into bytes, it is used by the `send_numpy` method.