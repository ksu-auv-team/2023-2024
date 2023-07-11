import socket
import logging
import numpy as np
from io import BytesIO

class Networking(socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer_size = 1024

    def connect(self, host, port):
        super().connect((host, port))
        logging.debug("Connected to {}:{}".format(host, port))

    def send_numpy(self, array):
        if not isinstance(array, np.ndarray):
            raise TypeError("Input should be a numpy array")
        data = self._pack_numpy(array)
        self.sendall(data)
        logging.debug("Array sent")

    def recv_numpy(self):
        data = self._recvall()
        array = np.load(BytesIO(data), allow_pickle=True)['array']
        logging.debug("Array received")
        return array

    def send_string(self, string):
        if not isinstance(string, str):
            raise TypeError("Input should be a string")
        data = string.encode()
        self.sendall(data)
        logging.debug("String sent")

    def recv_string(self):
        data = self._recvall()
        string = data.decode()
        logging.debug("String received")
        return string

    def _recvall(self):
        data = bytearray()
        while len(data) < 4 or data[-4:] != b'END\n':
            packet = self.recv(self.buffer_size)
            if not packet:
                break
            data.extend(packet)
        return data[:-4]

    @staticmethod
    def _pack_numpy(array):
        f = BytesIO()
        np.savez(f, array=array)
        data = f.getvalue() + b'END\n'
        return data

    def close_connection(self):
        # Close the socket
        self.close()