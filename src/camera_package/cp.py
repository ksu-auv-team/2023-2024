import threading

from src.camera_package.modules.regular.regular import Regular
from src.camera_package.modules.zed.zed import Zed


class cp:
    def __init__(self, zed, reg, host, zed_port, reg_port, camera_id):
        if zed:
            self.zed = Zed(host, zed_port)
        if reg:
            self.reg = Regular(host, reg_port, camera_id)

    def start(self):
        self.zed.start()
        self.reg.start()
