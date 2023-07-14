from modules.regular.regular import Regular
from modules.zed.zed import Zed
from src.modules.networking.networking import Networking


class cp:
    def __init__(self, forward:bool = True, bottom:bool = True, server:str = '10.0.0.34', ports:list = [9999, 9998], camera_ids:list = [0, 1]):
        self.host = server
        self.port_1 = ports[0]
        self.port_2 = ports[1]

        if forward:
            self.forward = Zed(self.host, self.port_1, camera_ids[0])
        if bottom:
            self.bottom = Regular(self.host, self.port_2, camera_ids[1])

    def start(self):
        # Zed camera package is not set up yet. TODO: Set up Zed camera package.
        # if self.forward:
        #     self.forward.start()
        if self.bottom:
            self.bottom.run()

    def stop(self):
        # Zed camera package is not set up yet. TODO: Set up Zed camera package.
        # if self.forward:
        #     self.forward.close()
        if self.bottom:
            self.bottom.close()


if __name__ == '__main__':
    # The host address where the socket server runs.
    host = '10.0.0.34'
    
    # The port number where the socket server listens.
    port = 9999
    
    # The ID of the camera to capture frames from.
    camera_id = 0

    # Initialize the camera package.
    cam_pack = cp(forward=False, bottom=True, server=host, ports=[port, port+1], camera_ids=[camera_id, camera_id+1])

    # Start the camera package.
    cam_pack.start()