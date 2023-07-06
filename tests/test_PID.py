import yaml
import math
import pytest
import socket
import struct
from unittest.mock import patch, mock_open, Mock
from src.movement_package.modules.PID.pid import PID  # Replace with your actual module name


def test_PID_initialization():
    with patch("builtins.open", mock_open(read_data=yaml.dump({
            'connect': True,
            'ip': '192.168.1.1',
            'port': 1234,
            'in_min': -0.5,
            'in_max': 0.5,
            'out_min': 1000,
            'out_max': 2000,
            'mew': 0.02,
            'prop': 0.1,
            'dh': 0.2,
            'dv': 0.2,
            'w': 0.4,
            'l': 0.4,
            'h': 0.3
        }))) as mock_file:
        pid = PID()
        assert pid.config["connect"] is True
        assert pid.config["ip"] == '192.168.1.1'
        assert pid.config["port"] == 1234
        assert pid.in_min == -0.5
        mock_file.assert_called_once_with('configs/pid.yml')


def test_PID_initialization_with_error():
    with patch("builtins.open", side_effect=FileNotFoundError):
        pid = PID()
        assert pid.config["connect"] is False
        assert pid.config["ip"] == 'localhost'
        assert pid.config["port"] == 9999
        assert pid.in_min == -0.4


def test_map():
    pid = PID()
    assert pid.map(-0.4) == 1000
    assert pid.map(0.4) == 2000


def test_parse():
    pid = PID()
    data = struct.pack('6f', 1.1, 2.2, 3.3, 4.4, 5.5, 6.6)
    result = pid.parse(data)
    assert len(result) == 6
    assert math.isclose(result[0], 1.1, rel_tol=1e-5)
    assert math.isclose(result[1], 2.2, rel_tol=1e-5)
    assert math.isclose(result[2], 3.3, rel_tol=1e-5)
    assert math.isclose(result[3], 4.4, rel_tol=1e-5)
    assert math.isclose(result[4], 5.5, rel_tol=1e-5)
    assert math.isclose(result[5], 6.6, rel_tol=1e-5)

@patch('socket.socket')
def test_run(mock_socket):
    data = struct.pack('6f', 1.1, 2.2, 3.3, 4.4, 5.5, 6.6)
    instance = mock_socket.return_value
    instance.recv.return_value = data

    pid = PID()
    pid.run()
    
    assert instance.connect.call_args[0][0] == ('localhost', 9999)
    assert len(pid.records) == 1
    assert len(pid.motors) == 8
