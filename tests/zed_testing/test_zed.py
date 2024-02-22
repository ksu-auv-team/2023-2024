# import pyzed.sl as sl
# import sys

# init = sl.InitParameters(depth_mode=sl.DEPTH_MODE.ULTRA,
#                                  coordinate_units=sl.UNIT.METER,
#                                  coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)

# zed = sl.Camera()
# status = zed.open(init)
# if status != sl.ERROR_CODE.SUCCESS:
#     print(repr(status))
#     exit()

# res = sl.Resolution()
# res.width = 720
# res.height = 404

# point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)

# while True:
#     if zed.grab() == sl.ERROR_CODE.SUCCESS:
#             zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
#             print(point_cloud.get_data())

# import pyzed.sl as sl

# def main():
#     # Create a Camera object
#     zed = sl.Camera()

#     # Create a InitParameters object and set configuration parameters
#     init_params = sl.InitParameters()
#     init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 opr HD1200 video mode, depending on camera type.
#     init_params.camera_fps = 30  # Set fps at 30

#     # Open the camera
#     err = zed.open(init_params)
#     if err != sl.ERROR_CODE.SUCCESS:
#         print("Camera Open : "+repr(err)+". Exit program.")
#         exit()


#     # Capture 50 frames and stop
#     i = 0
#     image = sl.Mat()
#     runtime_parameters = sl.RuntimeParameters()
#     while i < 50:
#         # Grab an image, a RuntimeParameters object must be given to grab()
#         if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
#             # A new image is available if grab() returns SUCCESS
#             zed.retrieve_image(image, sl.VIEW.LEFT)
#             timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
#             print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(),
#                   timestamp.get_milliseconds()))
#             i = i + 1

#     # Close the camera
#     zed.close()

# if __name__ == "__main__":
#     main()

import pyzed.sl as sl
import numpy as np
import cv2
from io import BytesIO
import logging
import socket
from typing import Any, Tuple, Union
import numpy as np


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

# Main function
def main():
    # Initialize logging
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

    # Runtime parameters
    runtime_parameters = sl.RuntimeParameters()

    # Initialize NumpySocket
    sender = NumpySocket()
    sender.connect(('192.168.0.109', 9999))  # Replace 'RECEIVER_IP' and 'PORT' with the receiver's IP address and port

    # Capture and send 50 frames
    image = sl.Mat()
    depth = sl.Mat()
    for i in range(50):
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

            # Convert SL Mat to numpy array for both image and depth
            image_np = image.get_data()
            depth_np = depth.get_data()

            # Send image and depth map
            sender.sendall(image_np)
            sender.sendall(depth_np)

            # Display image and depth (optional, can be removed if not needed)
            # cv2.imshow("ZED", image_np)
            # cv2.imshow("Depth", depth_np)
            cv2.waitKey(5)

    # Cleanup
    zed.close()
    sender.close()

if __name__ == "__main__":
    main()