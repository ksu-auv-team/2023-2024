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

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
    init_params.camera_fps = 30  # Set fps at 30

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit()

    # Create a RuntimeParameters object and set configuration parameters
    runtime_parameters = sl.RuntimeParameters()

    # Capture 50 frames and stop
    i = 0
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()
    while i < 50:
        # A new image is available if grab() returns SUCCESS
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.VIEW.LEFT)
            # Retrieve depth map. Depth is aligned on the left image
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            # Retrieve colored point cloud. Point cloud is aligned on the left image.
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)

            # Get and print distance value in mm at the center of the image
            # We measure the distance camera - object using Euclidean distance
            x = image.get_width() // 2
            y = image.get_height() // 2
            err, point_cloud_value = point_cloud.get_value(x, y)
            distance = np.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                               point_cloud_value[1] * point_cloud_value[1] +
                               point_cloud_value[2] * point_cloud_value[2])
            print("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))

            # Display image and depth using OpenCV
            cv2.imshow("ZED", image.get_data())
            cv2.imshow("Depth", depth.get_data())
            key = cv2.waitKey(5)
            i = i + 1

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()