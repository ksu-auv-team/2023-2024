#!/usr/bin/env python3

import logging
import socket
import pickle
from io import BytesIO
from typing import Any, Tuple
import numpy as np

class NetworkingProtocol(socket.socket):
    def send_data(self, data: Any) -> None:
        """Send data which can be any picklable object."""
        out = self.__pack_data(data)
        super().sendall(out)
        logging.debug("Data sent")

    def recv_data(self, bufsize: int = 4096) -> Any:
        """Receive data that can be any picklable object."""
        length = None
        data_buffer = bytearray()
        while True:
            data = super().recv(bufsize)
            if len(data) == 0:
                if length is None:
                    raise ValueError("No data received")
                else:
                    raise ValueError("Incomplete data received")
            data_buffer += data
            if length is None:
                if b":" not in data_buffer:
                    continue
                length_str, ignored, data_buffer = data_buffer.partition(b":")
                length = int(length_str)
            if len(data_buffer) >= length:
                break

        received_data = data_buffer[:length]
        return pickle.loads(received_data)

    def accept(self) -> Tuple['NetworkingProtocol', Tuple[str, int]]:
        """Accept a new connection and return a socket object with the same type."""
        fd, addr = super()._accept()
        sock = NetworkingProtocol(super().family, super().type, super().proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super().gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_data(data: Any) -> bytearray:
        """Pack data into a bytearray with a length header."""
        packed_data = pickle.dumps(data)
        packet_size = len(packed_data)
        header = f"{packet_size}:"
        header_bytes = header.encode()

        out = bytearray()
        out += header_bytes
        out += packed_data
        return out

if __name__ == "__main__":
    # Example usage:
    from socket import AF_INET, SOCK_STREAM
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Networking Protocol example")
    parser.add_argument("--server", action="store_true", help="Run as server")
    args = parser.parse_args()

    if args.server:
        # Server side
        server = NetworkingProtocol(AF_INET, SOCK_STREAM)
        server.bind(('localhost', 6000))
        server.listen(1)

        conn, addr = server.accept()
        received = conn.recv_data()
        print("Received:", received)
    else:
        # Client side
        client = NetworkingProtocol(AF_INET, SOCK_STREAM)
        client.connect(('localhost', 6000))
        client.send_data({"numpy_array": np.array([1, 2, 3]), "message": "Hello, world!"})
