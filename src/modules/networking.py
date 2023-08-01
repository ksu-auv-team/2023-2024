import socket
import logging
import numpy as np
from io import BytesIO


class Networking(socket.socket):
    """
    The Networking class inherits from the socket.socket class. 
    It is a subclass that provides additional methods for sending and receiving numpy arrays 
    and strings over a socket connection. 
    """

    def send_numpy(self, frame):
        """
        Method for sending numpy array data over a socket connection.

        Args:
            frame (np.ndarray): A numpy array that needs to be sent.

        Raises:
            TypeError: An error occurs if the input frame is not a valid numpy array.

        Returns:
            None
        """
        if not isinstance(frame, np.ndarray):
            raise TypeError("Input frame is not a valid numpy array")
        
        data = self.__pack_frame(frame)  # pack the frame into byte format
        super().sendall(data)  # use the inherited sendall method to send data
        logging.debug("Frame sent")  # log that the frame has been sent

    def send_string(self, string):
        """
        Method for sending string data over a socket connection.

        Args:
            string (str): A string that needs to be sent.

        Raises:
            TypeError: An error occurs if the input is not a valid string.

        Returns:
            None
        """
        if not isinstance(string, str):
            raise TypeError("Input string is not a valid string")

        string += '\n'  # add a newline character as the end marker of the string
        data = string.encode()  # convert string to bytes
        super().sendall(data)  # use the inherited sendall method to send data
        logging.debug("String sent")  # log that the string has been sent

    def recv_numpy(self, bufsize=1024):
        """
        Method for receiving numpy array data from a socket connection.

        Args:
            bufsize (int, optional): Maximum amount of data to be received at once. Default is 1024.

        Returns:
            np.ndarray: Numpy array received from the connection.
        """
        length = None
        frameBuffer = bytearray()  # define a byte array to hold incoming data
        while True:
            data = super().recv(bufsize)  # receive data from the socket
            if len(data) == 0:
                return np.array([])  # if no data, return an empty numpy array
            frameBuffer += data  # add incoming data to the buffer

            # following is to handle the case when the message length is known
            while True:
                if length is None:
                    if b':' not in frameBuffer:
                        break
                    # remove the length bytes from the front of frameBuffer
                    length_str, ignored, frameBuffer = frameBuffer.partition(b':')
                    length = int(length_str)
                if len(frameBuffer) < length:
                    break
                # split off the full message from the remaining bytes
                frameBuffer = frameBuffer[length:]
                length = None
                break

        frame = np.load(BytesIO(frameBuffer), allow_pickle=True)['frame']
        logging.debug("Frame received")  # log that the frame has been received
        return frame

    def recv_string(self, bufsize=1024):
        """
        Method for receiving string data from a socket connection.

        Args:
            bufsize (int, optional): Maximum amount of data to be received at once. Default is 1024.

        Returns:
            str: String received from the connection.
        """
        data = super().recv(bufsize)  # receive data from the socket
        string = data.decode()  # decode bytes to string
        string = string.rstrip('\n')  # remove the newline character at the end of the string
        logging.debug("String received")  # log that the string has been received
        return string

    def accept(self):
        """
        Override the accept() method from socket class to use the Networking class 
        for the new socket object that is created.

        Returns:
            tuple: A tuple containing the new socket object and the address of the client.
        """
        fd, addr = super()._accept()
        sock = Networking(super().family, super().type, super().proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super().gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame):
        """
        Helper method to convert a numpy array to byte format.

        Args:
            frame (np.ndarray): Numpy array to be converted to bytes.

        Returns:
            bytearray: Byte array representation of the numpy array.
        """
        f = BytesIO()  # use BytesIO as a buffer
        np.savez(f, frame=frame)  # save the numpy array to the buffer

        packet_size = len(f.getvalue())  # get the size of the byte representation of the numpy array
        header = '{0}:'.format(packet_size)
        header = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header

        f.seek(0)  # move the cursor back to the beginning of the buffer
        out += f.read()  # add the numpy array bytes to the output byte array
        return out
