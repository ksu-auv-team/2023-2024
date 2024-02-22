import pyzed.sl as sl
import numpy as np
import cv2
from io import BytesIO
import logging
import socket
from typing import Any, Tuple, Union
import numpy as np
from multiprocessing import Process, Queue


class NumpySocket(socket.socket):
    def sendall(self, frame: np.ndarray) -> None:
        out = self.__pack_frame(frame)
        super().sendall(out)
        logging.debug("frame sent")

    def recv(self, bufsize: int = 1024) -> np.ndarray:
        length = None
        frame_buffer = bytearray()
        while True:
            data = super().recv(bufsize)
            if len(data) == 0:
                return np.array([])
            frame_buffer += data
            if len(frame_buffer) == length:
                break
            while True:
                if length is None:
                    if b":" not in frame_buffer:
                        break
                    length_str, ignored, frame_buffer = frame_buffer.partition(b":")
                    length = int(length_str)
                if len(frame_buffer) < length:
                    break

                frame_buffer = frame_buffer[length:]
                length = None
                break

        frame = np.load(BytesIO(frame_buffer), allow_pickle=True)["frame"]
        logging.debug("frame received")
        return frame

    def accept(self) -> Tuple['NumpySocket', Union[Tuple[str, int], Tuple[Any, ...]]]:
        fd, addr = super()._accept()
        sock = NumpySocket(super().family, super().type, super().proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super().gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame: np.ndarray) -> bytearray:
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = "{0}:".format(packet_size)
        header_bytes = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header_bytes

        f.seek(0)
        out += f.read()
        return out

def send_images(queue):
    """
    Function to run in a separate process for sending images.
    """
    logging.basicConfig(level=logging.INFO)
    sender = NumpySocket()
    try:
        sender.connect(('192.168.0.106', 9999))  # Replace with the receiver's IP and port
        while True:
            image_np = queue.get()  # Wait for an image from the queue
            if image_np is None:
                break  # None is sent as a signal to stop
            sender.sendall(image_np)
    finally:
        sender.close()

def main():
    logging.basicConfig(level=logging.INFO)

    # Create a Camera object
    zed = sl.Camera()

    # Camera configuration
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.camera_fps = 30

    # Open the camera
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        logging.error("Camera Open Failed")
        exit(1)

    image = sl.Mat()
    depth = sl.Mat()

    # Create a multiprocessing Queue and start the sender process
    queue = Queue(maxsize=5)  # Limit the queue size to prevent memory issues
    sender_process = Process(target=send_images, args=(queue,))
    sender_process.start()

    try:
        while True:
            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_image(image, sl.VIEW.LEFT)
                zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

                # Convert SL Mat to numpy array for both image and depth
                image_np = image.get_data()
                depth_np = depth.get_data()

                # Send image and depth map through the queue
                if not queue.full():
                    queue.put(image_np.copy())  # Use .copy() to ensure correct memory handling
                    queue.put(depth_np.copy())
                else:
                    logging.warning("Queue is full, dropping frame.")

    finally:
        # Cleanup
        zed.close()
        queue.put(None)  # Signal the sender process to stop
        sender_process.join()

if __name__ == "__main__":
    main()