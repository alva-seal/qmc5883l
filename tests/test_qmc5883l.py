import pytest
import

import qmc5883l

"""
def test_convert_data():
    data = [128, 128]
    offset = 0
    a = qmc5883l._convert_data(data, offset)
    b = qmc5883l.qmc5883l.QMC5883L._convert_data(data, offset)
    print(a, b)
"""


def test_init__empty_params__():
    magnet_sensor = qmc5883l.QMC5883L()
    assert magnet_sensor.busnum is 1
    ^
