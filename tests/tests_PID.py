from src.movement_package.modules.PID import pid as PID

import unittest
from unittest.mock import patch, mock_open
import numpy as np
import struct


class TestPID(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="in_min: '0'\nin_max: '10'\nout_min: '100'\nout_max: '1000'\nmew: '1.0'\nprop: '1.0'\ndh: '1.0'\ndv: '1.0'\nw: '1.0'\nl: '1.0'\nh: '1.0'")
    def test_init(self, mock_file):
        pid = PID.PID()
        self.assertEqual(pid.in_min, 0.0)
        self.assertEqual(pid.in_max, 10.0)
        self.assertEqual(pid.out_min, 100)
        self.assertEqual(pid.out_max, 1000)
        self.assertIsNotNone(pid.config)

    def test_map(self):
        pid = PID.PID()
        pid.in_min = 0.0
        pid.in_max = 10.0
        pid.out_min = 100
        pid.out_max = 1000
        self.assertEqual(pid.map(5), 550)  # simple case

    def test_controller(self):
        pid = PID.PID()
        pid.mew = 1.0
        pid.prop = 1.0
        pid.l = 1.0
        pid.h = 1.0
        pid.ah = np.arctan(1)  # assume w and l are 1
        pid.av = np.arctan(1)  # assume h, w, l are 1
        pid.controller(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)  # simple case
        self.assertIsNotNone(pid.horizontal)
        self.assertIsNotNone(pid.vertical)

    def test_parse(self):
        pid = PID.PID()
        data = struct.pack('6f', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        result = pid.parse(data)
        self.assertEqual(result, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0))  # simple case


if __name__ == '__main__':
    unittest.main()