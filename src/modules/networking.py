import socket
import logging
import numpy as np
from io import BytesIO


class Networking(socket.socket):
    def send_numpy(self, frame):
        if not isinstance(frame, np.ndarray):
            raise TypeError("Input frame is not a valid numpy array")
        data = self.__pack_frame(frame)
        super().sendall(data)
        logging.debug("Frame sent")

    def send_string(self, string):
        if not isinstance(string, str):
            raise TypeError("Input string is not a valid string")
        string += '\n'  # add a newline character as the end marker of the string
        data = string.encode()  # convert string to bytes
        super().sendall(data)
        logging.debug("String sent")

    def recv_numpy(self, bufsize=1024):
        length = None
        frameBuffer = bytearray()
        while True:
            data = super().recv(bufsize)
            if len(data) == 0:
                return np.array([])
            frameBuffer += data
            if len(frameBuffer) == length:
                break
            while True:
                if length is None:
                    if b':' not in frameBuffer:
                        break
                    # remove the length bytes from the front of frameBuffer
                    # leave any remaining bytes in the frameBuffer!
                    length_str, ignored, frameBuffer = frameBuffer.partition(b':')
                    length = int(length_str)
                if len(frameBuffer) < length:
                    break
                # split off the full message from the remaining bytes
                # leave any remaining bytes in the frameBuffer!
                frameBuffer = frameBuffer[length:]
                length = None
                break

        frame = np.load(BytesIO(frameBuffer), allow_pickle=True)['frame']
        logging.debug("Frame received")
        return frame

    def recv_string(self, bufsize=1024):
        data = super().recv(bufsize)
        string = data.decode()  # decode bytes to string
        string = string.rstrip('\n')  # remove the newline character at the end of the string
        logging.debug("String received")
        return string

    def accept(self):
        fd, addr = super()._accept()
        sock = Networking(super().family, super().type, super().proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super().gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame):
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = '{0}:'.format(packet_size)
        header = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header

        f.seek(0)
        out += f.read()
        return out
