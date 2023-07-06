import math
import yaml
import socket
import struct

import numpy as np


class PID:
    def __init__(self):
        try:
            with open('configs/pid.yml') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        except:
            self.config = {
                'connect': False,
                'ip': 'localhost',
                'port': 9999,
                'in_min': -0.4,
                'in_max': 0.4,
                'out_min': 1000,
                'out_max': 2000,
                'mew': 0.01,
                'prop': 0.08,
                'dh': 0.15,
                'dv': 0.15,
                'w': 0.3,
                'l': 0.3,
                'h': 0.25
            }

        self.in_min = float(self.config['in_min'])
        self.in_max = float(self.config['in_max'])
        self.out_min = int(self.config['out_min'])
        self.out_max = int(self.config['out_max'])
        self.mew = float(self.config['mew'])
        self.prop = float(self.config['prop'])
        self.dh = float(self.config['dh'])
        self.dv = float(self.config['dv'])
        self.w = float(self.config['w'])
        self.l = float(self.config['l'])
        self.h = float(self.config['h'])
        self.ah = math.atan(self.w / self.l)
        self.av = math.atan(self.h / (math.sqrt(self.w ** 2 + self.l ** 2)))
        
        self.motors = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        
        self.records = []
        

    def controller(self,w:float, p: float, q: float, u:float, v:float, r:float):
        self.horizontal = (self.mew/self.prop) * np.array(
            [
                [-1*(1/math.sin(self.ah)), 1*(1/math.cos(self.ah)), 1*self.l],
                [-1*(1/math.sin(self.ah)), -1*(1/math.cos(self.ah)), -1*self.l],
                [-1*(1/math.sin(self.ah)), 1*(1/math.cos(self.ah)), -1*self.l],
                [-1*(1/math.sin(self.ah)), -1*(1/math.cos(self.ah)), 1*self.l]
            ]
        ) @ np.array([[u], [v], [r]])
        self.vertical = (self.mew/self.prop) * np.array(
            [
                [1*(1/math.cos(self.av)), 1*self.h, -1*self.h],
                [1*(1/math.cos(self.av)), -1*self.h, -1*self.h],
                [1*(1/math.cos(self.av)), -1*self.h, 1*self.h],
                [1*(1/math.cos(self.av)), 1*self.h, 1*self.h],
            ]
        ) @ np.array([[w], [p], [q]])

    def map(self, x: float):
        return (x - self.in_min) * (self.out_max - self.out_min) / (self.in_max - self.in_min) + self.out_min
    def parse(self, data):
        d = struct.unpack('6f', data)
        return d
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.config['ip'], self.config['port']))

        data = s.recv(1024)
        self.in_data = self.parse(data)
        
        self.controller(float(self.in_data[0]), float(self.in_data[1]), float(self.in_data[2]), float(self.in_data[3]), float(self.in_data[4]), float(self.in_data[5]))
        self.records.append([self.horizontal, self.vertical])
        
        for i in range(4):
            self.motors[i] = int(self.map(self.horizontal[i]))
            
        for i in range(4, 8):
            self.motors[i] = int(self.map(self.vertical[i-4]))
        
        # Debug
        print(self.horizontal)
        print(self.motors)


if __name__ == '__main__':
    pid = PID()
    pid.run()
