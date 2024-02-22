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

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def send_data(queue, ip, port):
    """
    Function to run in a separate process for sending images or depth maps.
    """
    logging.basicConfig(level=logging.INFO)
    sender = NumpySocket()
    try:
        sender.connect((ip, port))
        while True:
            data_np = queue.get()
            if data_np is None:
                break
            sender.sendall(data_np)
    finally:
        sender.close()

def main():
    logging.basicConfig(level=logging.INFO)

    # Create a Camera object
    zed = sl.Camera()

    # Camera configuration
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.camera_fps = 15

    # Open the camera
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        logging.error("Camera Open Failed")
        exit(1)

    image = sl.Mat()
    depth = sl.Mat()

    # Queues for images and depth maps
    queue_image = Queue(maxsize=5)
    queue_depth = Queue(maxsize=5)

    # Start sender processes for images and depth maps
    ip_address = '192.168.0.109'
    image_port = 9998
    depth_port = 9999
    sender_process_image = Process(target=send_data, args=(queue_image, ip_address, image_port))
    sender_process_depth = Process(target=send_data, args=(queue_depth, ip_address, depth_port))
    sender_process_image.start()
    sender_process_depth.start()

    try:
        while True:
            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_image(image, sl.VIEW.LEFT)
                zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

                # Convert SL Mat to numpy array for both image and depth
                image_np = image.get_data()
                depth_np = depth.get_data()

                # Resize the image to a smaller size for faster transmission
                image_np = image_resize(image_np, width=320, height=180)
                depth_np = image_resize(depth_np, width=320, height=180)

                if not queue_image.full():
                    queue_image.put(image_np.copy())

                if not queue_depth.full():
                    queue_depth.put(depth_np.copy())
    finally:
        # Cleanup
        queue_image.put(None)
        queue_depth.put(None)
        sender_process_image.join()
        sender_process_depth.join()

if __name__ == "__main__":
    main()