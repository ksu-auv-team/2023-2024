import socket
import struct
import time

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 9999))
    s.listen()
    conn, addr = s.accept()
    
    # while True:
    # d = [-1, -1, -1, -1, -1, -1]
    # d = [0, 0, 0, 0, 0, 0]
    d = [1, 1, 1, 1, 1, 1]
    
    data = struct.pack('6f', *d)
    conn.sendall(data)
    time.sleep(0.1)
                
if __name__ == '__main__':
    client()