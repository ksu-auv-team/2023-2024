import json
import time
import requests
import logging

class StateMachine:
    def __init__(self):
        """
        movements = [X, Y, Z, Pitch, Roll, Yaw, Torp, Torp, Claw]
        """
        
        self.movements = {
            "forward": [1, 0, 0, 0, 0, 0, 0, 0, 0],
            "backward": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            "left": [0, 1, 0, 0, 0, 0, 0, 0, 0],
            "right": [0, -1, 0, 0, 0, 0, 0, 0, 0],
            "up": [0, 0, 1, 0, 0, 0, 0, 0, 0],
            "down": [0, 0, -1, 0, 0, 0, 0, 0, 0],
            "yaw_left": [0, 0, 0, 0, 0, 1, 0, 0, 0],
            "yaw_right": [0, 0, 0, 0, 0, -1, 0, 0, 0],
            "claw_open": [0, 0, 0, 0, 0, 0, 0, 0, 1],
            "claw_close": [0, 0, 0, 0, 0, 0, 0, 0, -1]
        }
        
        self.base_url = 'http://localhost:5000'
    
    def get_data(self):
        """
        Retrieves data from objects and sonar
        """
        get_url = self.base_url + '/objects'
        response = requests.get(get_url)
        if response.status_code == 200:
            objects = response.json()
        else:
            self.movement_logger.error("Failed to fetch objects data")
        
        get_url = self.base_url + '/sonar'
        response = requests.get(get_url)
        if response.status_code == 200:
            sonar = response.json()
        else:
            self.movement_logger.error("Failed to fetch sonar data")
    
        return objects, sonar
    
    def send_data(self, data):
        """
        Sends input data to the server
        """
        send_url = self.base_url + '/input'
        data = {
            'X': data[0],
            'Y': data[1],
            'Z': data[2],
            'Pitch': data[3],
            'Roll': data[4],
            'Yaw': data[5],
            'Torp1': data[6],
            'Torp2': data[7],
            'Claw': data[8]
        }
        try:
            response = requests.post(send_url, json=data)
            if response.status_code == 200:
                logging.info("Data successfully sent to the server.")
            else:
                logging.error(f"Failed to send data: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending data: {str(e)}")
    
    def gate(self):
        """
        Process to pass through gate
        """
        gate_passed = False
        while not gate_passed:
            objects, sonar = self.get_data()
            if objects['object_name'] == 'Gate':
                x, y = objects['object_center']
                cam_x, cam_y = sonar['camera_center']
                if (x + 20) <= cam_x <= (x - 20) and (y - 20) <= cam_y <= (y + 20):
                    self.send_data(self.movements['forward'])
                else:
                    if x < cam_x:
                        self.send_data(self.movements['yaw_left'])
                    elif x > cam_x:
                        self.send_data(self.movements['yaw_right'])
                    if y < cam_y:
                        self.send_data(self.movements['up'])
                    elif y > cam_y:
                        self.send_data(self.movements['down'])
            else:
                gate_passed = True
    
    def extra(self):
        """
        Process to get extra points
        """
        start = time.time()
        while True:
            if time.time() - start >= 180:
                break
            else:
                self.send_data(self.movements['yaw_left'])
    
    def bouy(self):
        """
        Process to circle bouy
        """
        bouy_done = False
        while not bouy_done:
            objects, sonar = self.get_data()
            if objects['object_name'] == 'Bouy':
                x, y = objects['object_center']
                cam_x, cam_y = sonar['camera_center']
                if (x + 100) <= cam_x <= (x - 100) and (y + 100) <= cam_y <= (y - 100):
                    self.send_data(self.movements['left'])
                else:
                    if x < cam_x:
                        self.send_data(self.movements['yaw_left'])
                    elif x > cam_x:
                        self.send_data(self.movements['yaw_right'])
                    if y < cam_y:
                        self.send_data(self.movements['up'])
                    elif y > cam_y:
                        self.send_data(self.movements['down'])
            else:
                bouy_done = True
                
    def bin(self):
        """
        Process to drop bin
        """
        start = time.time()
        while start - time.time() >= 10:
            self.send_data(self.movements('down'))
        start = time.time()
        while start - time.time() >= 10:
            self.send_data(self.movements['claw_open'])
    
    def run(self):
        self.get_data()
        self.gate()
        self.extra()
        self.bouy()
        self.gate()
        time.sleep(10)
        

if __name__ == "__main__":
    sm = StateMachine()
    sm.run()