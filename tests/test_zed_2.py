import pyzed.sl as sl
from numpysocket import NumpySocket
import cv2
import numpy as np

def grab_image():
    with NumpySocket() as s:
        # Create the client connection
        s.connect(('192.168.0.105', 5555))

        # Create the camera object
        zed = sl.Camera()

        # Set configuration parameters
        init = sl.InitParameters()
        init.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
        init.depth_mode = sl.DEPTH_MODE.NEURAL # Use the neural depth mode
        init.coordinate_units = sl.UNIT.METER  # Use meter units (for depth measurements)
        init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP  # Use a right-handed Y-up coordinate system
        init.camera_fps = 30  # Set the frame rate to 30 fps

        # Open the camera
        status = zed.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            exit()
        
        # Create a runtime parameters object and set the image flip option to false
        runtime = sl.RuntimeParameters()

        # Enable point cloud retrieval
        res = sl.Resolution()
        res.width = 720
        res.height = 404
        point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)

        right_image = sl.Mat()
        left_image = sl.Mat()

        while True:
            if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
                # A new image is available if grab() returns SUCCESS
                zed.retrieve_image(left_image, sl.VIEW.LEFT)
                zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, res)

                # Convert the image to a numpy array
                left_image_np = left_image.get_data()
                point_cloud_np = point_cloud.get_data()
                combinded_data = np.array([left_image_np, point_cloud_np])

                # Send the data to the server
                s.sendall(left_image_np)

if __name__ == '__main__':
    grab_image()
    print('Done!')