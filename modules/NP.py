#!/usr/bin/env python3

from io import BytesIO
import logging
import socket
from typing import Any

import numpy as np


class NP(socket.socket):
    """
    ## NP class
    Inherits from `socket.socket` and provides specialized methods to send and receive numpy arrays and strings as bytes.
    """

    def sendall(self, frame: np.ndarray) -> None:
        """
        ### sendall method
        Send the numpy frame over the socket.
        
        **Arguments:**
        - `frame (np.ndarray)`: The numpy array frame to send.

        **Returns:**
        - None
        """
        out = self.__pack_frame(frame)
        super_socket = super()
        super_socket.sendall(out)
        logging.debug("frame sent")

    def send_string_as_bytes(self, string: str) -> None:
        """
        ### send_string_as_bytes method
        Send a string as a byte array over the socket.
        
        **Arguments:**
        - `string (str)`: The string to send.

        **Returns:**
        - None
        """
        byte_array = string.encode('utf-8')
        super().sendall(byte_array)
        logging.debug(f"String '{string}' sent as bytes")

    def recv(self, bufsize: int = 1024) -> np.ndarray:
        """
        ### recv method
        Receive a numpy frame over the socket.
        
        **Arguments:**
        - `bufsize (int, optional)`: The size of the buffer to use for receiving data. Defaults to 1024.

        **Returns:**
        - `np.ndarray`: The received numpy array.
        """
        length = None
        frame_buffer = bytearray()
        while True:
            data = super().recv(bufsize)
            if len(data) == 0:
                return np.array([])
            frame_buffer += data

            while True:
                if length is None:
                    if b":" not in frame_buffer:
                        break
                    length_str, _, frame_buffer = frame_buffer.partition(b":")
                    length = int(length_str)

                if len(frame_buffer) < length:
                    break

                frame_data = frame_buffer[:length]
                frame_buffer = frame_buffer[length:]
                frame = np.load(BytesIO(frame_data), allow_pickle=True)["frame"]
                logging.debug("frame received")
                return frame

    def recv_string_as_bytes(self, bufsize: int = 1024) -> str:
        """
        ### recv_string_as_bytes method
        Receive string data in the form of a byte array and returns the string.
        
        **Arguments:**
        - `bufsize (int, optional)`: The size of the buffer to use for receiving data. Defaults to 1024.

        **Returns:**
        - `str`: The received string.
        """
        data = super().recv(bufsize)
        if len(data) == 0:
            return ""
        decoded_string = data.decode('utf-8')
        logging.debug(f"Received string as bytes: {decoded_string}")
        return decoded_string

    def accept(self) -> tuple["NP", tuple[str, int] | tuple[Any, ...]]:
        """
        ### accept method
        Accept a connection. Overrides the base class method to return an object of this class instead of `socket.socket`.

        **Returns:**
        - `tuple`: Tuple containing a new NP object and the address of the client.
        """
        super_socket = super()
        fd, addr = super_socket._accept()
        sock = NP(super_socket.family, super_socket.type, super_socket.proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super_socket.gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame: np.ndarray) -> bytearray:
        """
        ### __pack_frame static method
        Packs a numpy frame into a byte array with a header indicating its size.
        
        **Arguments:**
        - `frame (np.ndarray)`: The numpy array frame to pack.

        **Returns:**
        - `bytearray`: The packed byte array.
        """
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = f"{packet_size}:"
        header_bytes = bytes(header.encode())  # prepend length of array

        out = bytearray(header_bytes)
        f.seek(0)
        out += f.read()

        return out
