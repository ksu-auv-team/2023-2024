#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2
import serial
import time

# Initialize serial connection
ser = serial.Serial('/dev/ttyTHS0', 115200)

# Create a list of integers
data = [1, 1, 1, 1, 126, 126, 126, 126, 0, 0, 0, 0]

# Convert the list to bytes
data_bytes = bytes(data)

# Try to send the data
try:
    ser.write(data_bytes)
    time.sleep(1)  # Allow time for data to be transmitted
except Exception as e:
    print(f"Error sending data: {e}")
    ser.close()
    exit(1)

# # Initialize the camera
# cap = cv2.VideoCapture(2)  # Adjust the index as needed
# if not cap.isOpened():
#     print("Error: Camera could not be opened.")
#     exit(1)

# # Set camera properties
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
#     if width is None and height is None:
#         return image
#     (h, w) = image.shape[:2]
#     if width is None:
#         r = height / float(h)
#         dim = (int(w * r), height)
#     else:
#         r = width / float(w)
#         dim = (width, int(h * r))
#     return cv2.resize(image, dim, interpolation=inter)

# with NumpySocket() as s:
#     s.connect(("10.0.0.163", 9999))
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: No frame received from the camera.")
#             break

#         frame = maintain_aspect_ratio_resize(frame, width=480)

#         try:
#             s.sendall(frame)
#         except Exception as e:
#             print(f"Error sending data: {e}")
#             break

# cap.release()
