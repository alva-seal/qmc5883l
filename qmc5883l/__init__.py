# -*- coding: utf-8 -*-
from smbus2 import SMBus


"""Driver for the QMC5883l 3-Axis Magnetic Sensor
Datasheet: https://github.com/e-Gizmo/QMC5883L-GY-271-Compass-module/blob/master/QMC5883L%20Datasheet%201.0%20.pdf # noqa
"""

__author__ = "Fabian Mruck"
__email__ = "github@ffabi.com"
__license__ = 'MIT'
__version__ = 'v0.1'

"""HISTORY
v.01 - First
"""
RATES = {
    10: 0,
    50: 1,
    100: 2,
    200: 3,
}

OSR = {
    64: 3,
    128: 2,
    256: 1,
    512: 0,
}

REG_OUT_X_LSB = 0x00
REG_OUT_X_MSB = 0x01
REG_OUT_Y_LSB = 0x02
REG_OUT_Y_MSB = 0x03
REG_OUT_Z_LSB = 0x04
REG_OUT_Z_MSB = 0x05
REG_STATUS = 0x06
REG_TEMP_LSB = 0x07
REG_TEMP_MSB = 0x08
REG_CONF_1 = 0x09
REG_CONF_2 = 0x0a
REG_RST_PERIOD = 0x0b
REG_CHIP_ID = 0x0d


class QMC5883L(object):
    '''Driver for the QMC5883l 3-Axis Magnetic Sensor'''
    def __init__(self,
                 adress=13,
                 busnum=1,
                 cont_mode=True,
                 rate=10,
                 full_scale=True,
                 over_sampling_rate=256,
                 interupt=True,
                 pointer_roll=False,
                 restore=False
                 ):
        """
        TODO: explain allwed values in ValueError
        """
        if over_sampling_rate in OSR:
            self.over_sampling_rate = OSR.get(over_sampling_rate)
        else:
            raise ValueError('oversampling rate is not a allwed value')
        if rate in RATES:
            self.rate = RATES.get(rate)
        else:
            raise ValueError('rate is not a allowed value')

        self.bus = SMBus(busnum)
        self.adress = adress
        self.full_scale = full_scale
        self.interupt = interupt
        self.pointer_roll = pointer_roll
        self.restore = restore
        self.cont_mode = cont_mode

        """
        TODO: Maybe a warning is better than print
        """
        if self.bus.read_byte_data(self.adress, REG_CHIP_ID) != 0xff:
            print("Wrong Chip ID, are you shure this is the correct Chip?")
        self.set_config(self)

    def set_config(self):
        if self.cont_mode:
            self.cntrl_reg1 = 1
        if self.full_scale:
            self.cntrl_reg1 = self.cntrl_reg1 + 1 * (2**2)
        self.cntrl_reg1 = self.cntrl_reg1 + self.over_sampling_rate * (2**4)
        self.cntrl_reg1 = self.cntrl_reg1 + self.rate * (2**6)
        self.cntrl_reg2 = self.interupt
        self.cntrl_reg2 = self.cntrl_reg2 + self.pointer_roll * (2 ** 6)
        self.cntrl_reg2 = self.cntrl_reg2 + self.restore * (2 ** 7)
        self.bus.write_byte_data(self.adress, REG_CONF_1, self.cntrl_reg1)
        self.bus.write_byte_data(self.adress, REG_CONF_2, self.cntrl_reg2)
        
    def get_temp(self):
        return self.bus.read_byte_data(self.adress, REG_TEMP_MSB) * 2.56 + self.bus.read_byte_data(self.adress, REG_TEMP_LSB) / 100
    
    def get_magnet(self):
        self.read_byte_data(self.adress, REG_OUT_X_LSB)
        return [0 0 0]
        
