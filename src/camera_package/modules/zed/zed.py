import pyzed.sl as sl
from src.modules.networking.networking import Networking

class Zed:
    def __init__(self, host, port):
        self.zed = sl.Camera()

        # Create a InitParameters object and set configuration parameters
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
        init_params.camera_fps = 30  # Set fps at 30

        # Open the camera
        err = self.zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            exit(1)

        self.host = host
        self.port = port

    def bind(self):
        try:
            # Create a networking socket
            self.np_socket = Networking()
            # Bind the socket to host and port
            self.np_socket.bind((self.host, self.port))
            # Start listening for incoming connections
            self.np_socket.listen(1)
            # Accept the client connection
            self.client, _ = self.np_socket.accept()
            print('Client connected')
        except Exception as e:
            print("Error in connect: ", e)

    def send_frame(self, data):
        """
            Send the frame to the client.

            Args:
                img (numpy.ndarray): The frame to send.
                mat_type (int): The type of the frame.
                shape (tuple): The shape of the frame.
        """
        # Convert the frame to bytes
        frame_bytes = data.tobytes()
        # Send the frame to the client
        self.np_socket.send_numpy(frame_bytes)
        
    def get_image(self):
        pass

    def get_depth_perception(self):
        pass

    def get_point_cloud(self):
        pass

    def get_objects(self):
        pass

    def run(self):
        pass
