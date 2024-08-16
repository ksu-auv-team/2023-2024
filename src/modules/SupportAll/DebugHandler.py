import json
import requests
import time

class DebugHandler:
    def __init__(self, Package : str, ip : str, port : int):
        self.Package = Package
        self.ip = ip
        self.port = port
        self.MessageType = None
        self.Message = None

    def set_data(self, MessageType : str, Message : str):
        self.MessageType = MessageType
        self.Message = Message
        self.send_data()
    
    def send_data(self):
        data = {
            "Package": self.Package,
            "MessageType": self.MessageType,
            "Message": self.Message
        }
        requests.post(f'http://{self.ip}:{self.port}/debug', json=data)
        return True
