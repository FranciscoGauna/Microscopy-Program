# -*- coding: utf-8 -*-
"""
    lantz.drivers.stanford.LI5655
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2015 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from collections import OrderedDict

import numpy as np
from lantz import Action, Feat, DictFeat, ureg
from lantz import MessageBasedDriver
from lantz.core import messagebased

SENS = OrderedDict([
        ('2 nV/fA', 0),
        ('5 nV/fA', 1),
        ('10 nV/fA', 2),
        ('20 nV/fA', 3),
        ('50 nV/fA', 4),
        ('100 nV/fA', 5),
        ('200 nV/fA', 6),
        ('500 nV/fA', 7),
        ('1 uV/pA', 8),
        ('2 uV/pA', 9),
        ('5 uV/pA', 10),
        ('10 uV/pA', 11),
        ('20 uV/pA', 12),

        ('50 uV/pA', 13),
        ('100 uV/pA', 14),
        ('200 uV/pA', 15),
        ('500 uV/pA', 16),
        ('1 mV/nA', 17),
        ('2 mV/nA', 18),
        ('5 mV/nA', 19),
        ('10 mV/nA', 20),
        ('20 mV/nA', 21),
        ('50 mV/nA', 22),
        ('100 mV/nA', 23),
        ('200 mV/nA', 24),
        ('500 mV/nA', 25),
        ('1 V/uA', 26)
        ])

TCONSTANTS = OrderedDict([
    ('0 µs', "0"),
    ('1 µs', "1.000000e-06"),
    ('2 µs', "2.000000e-06"),
    ('5 µs', "3.000000e-06"),
    ('10 µs', "1.000000e-05"),
    ('20 µs', "2.000000e-05"),
    ('50 µs', "5.000000e-05"),
    ('100 µs', "1.000000e-04"),
    ('200 µs', "2.000000e-04"),
    ('500 µs', "5.000000e-04"),
    ('1 ms', "1.000000e-03"),
    ('2 ms', "2.000000e-03"),
    ('5 ms', "5.000000e-03"),
    ('10 ms', "1.000000e-02"),
    ('20 ms', "2.000000e-02"),
    ('50 ms', "5.000000e-02"),
    ('100 ms', "1.000000e-01"),
    ('200 ms', "2.000000e-01"),
    ('500 ms', "5.000000e-01"),
    ('1 s', "1.000000e+00"),
    ('2 s', "2.000000e+00"),
    ('5 s', "5.000000e+00"),
    ('10 s', "1.000000e+01"),
    ('20 s', "2.000000e+01"),
    ('50 s', "5.000000e+01"),
    ('100 s', "1.000000e+02"),
    ('200 s', "2.000000e+02"),
    ('500 s', "5.000000e+02"),
    ('1 ks', "1.000000e+03"),
    ('2 ks', "2.000000e+03"),
    ('5 ks', "5.000000e+03"),
    ('10 ks', "1.000000e+04"),
    ('20 ks', "2.000000e+04"),
    ('50 ks', "5.000000e+04"),
])

SAMPLE_RATES = OrderedDict([
    ('62.5 mHz', 0),
    ('125 mHz', 1),
    ('250 mHz', 2),
    ('500 mHz', 3),
    ('1 Hz', 4),
    ('2 Hz', 5),
    ('4 Hz', 6),
    ('8 Hz', 7),
    ('16 Hz', 8),
    ('32 Hz', 9),
    ('64 Hz', 10),
    ('128 Hz', 11),
    ('256 Hz', 12),
    ('512 Hz', 13),
    ('trigger', 14)
])


class LI5655(MessageBasedDriver):
    MANUFACTURER_ID = '0x0D4A'
    MODEL_CODE = '0x004D'
    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}

    def write(self, command, termination=None, encoding=None):
        self.resource.write(command, termination, encoding)

    def setup(self):
        self.write(":CALC1:FORM MLIN")
        self.write(":CALC2:FORM PHAS")
        self.write(":CALC3:FORM REAL")
        self.write(":CALC4:FORM IMAG")

    @Feat(values={1: "IE6", 100: "IE8"})
    def sensitivity(self):
        """Detection Sensitivity, or gain.
        """
        return self.query(':INP:GAIN?')

    @sensitivity.setter
    def sensitivity(self, value):
        self.write(':INP:GAIN {}'.format(value))

    @Feat(limits=(1, 19999, 1))
    def harmonic(self):
        """Detection harmonic.
        """
        return int(self.query(':FREQ:MULT?'))

    @harmonic.setter
    def harmonic(self, value):
        self.write(':FREQ:MULT {}'.format(value))

    @Feat(values={6, 12, 18, 24})
    def filter_slope(self):
        """Time constant.
        """
        return int(self.query(':FILT:SLOP?'))

    @filter_slope.setter
    def filter_slope(self, value):
        self.write(':FILT:SLOP {}'.format(value))

    @Feat(values=TCONSTANTS)
    def time_constants(self):
        """Time constant.
        """
        return self.query(':FILT:TCON?')

    @time_constants.setter
    def time_constants(self, value):
        self.write(':FILT:TCON {}'.format(value))

    @Feat(values={'AC', 'DC'})
    def coupling(self):
        """Input coupling.
        """
        return self.query(':INP:COUP?')

    @coupling.setter
    def coupling(self, value):
        self.write(':INP:COUP {}'.format(value))

    @Feat(values={True: 'IOSC', False: 'RINP'})
    def reference_on(self):
        """Reference source.
        """
        return self.query(':ROUT2?')

    @reference_on.setter
    def reference_on(self, value):
        self.write(':ROUT2 {}'.format(value))

    @Feat(values={True, False})
    def overloaded(self):
        self.write(':DATA 1')
        return int(self.query(':FETCh?')) != 0

    @Feat(units='V')
    def amplitude(self):
        """Returns the value of the amplitude channel, which measures from the input signal"""
        self.write(':DATA 2')
        return self.query(':FETCh?')

    @Feat(units='degrees')
    def phase(self):
        """phase returns the value of the phase channel, which measures from the input signal"""
        self.write(':DATA 4')
        return self.query(':FETCh?')

    @Feat(units='V')
    def real_part_x(self):
        """Real Part x returns the value of the x channel , which measures from the input signal"""
        self.write(':DATA 8')
        return self.query(':FETCh?')

    @Feat(units='V')
    def imaginary_part_y(self):
        """Imaginaty part y returns the value of the x channel , which measures from the input signal"""
        self.write(':DATA 16')
        return self.query(':FETCh?')

    @Feat(units='Hz', limits=(0.001, 102000, 0.00001))
    def reference_frequency(self):
        """Reference reference_frequency.
        """
        return float(self.query(':SOUR:FREQ?'))

    @reference_frequency.setter
    def reference_frequency(self, value):
        self.write(':SOUR:FREQ {}'.format(value))

    @Feat(units='volt', limits=(0.004, 5., 0.002))
    def reference_amplitude(self):
        """Amplitude of the sine output.
        """
        return self.query(':SOUR:VOLT?')

    @reference_amplitude.setter
    def reference_amplitude(self, value):
        self.write(':SOUR:VOLT {}'.format(value))

    @Feat(units='degrees', limits=(-360, 729.99, 0.01))
    def reference_phase(self):
        """Phase shift of the reference.
        """
        return self.query(':PHAS?')

    @reference_phase.setter
    def reference_phase(self, value):
        self.write(':PHAS {}'.format(value))


class ResourceDummy:
    response = 0
    ofsl = 6
    tconst = '1E-6'
    sens = 1
    coupling = 'AC'
    ref = 'IOSC'
    icpl_coup = 0

    def write(self, command, termination=None, encoding=None):
        if "OFSL?" in command or ':FILT:SLOP?' in command:
            self.response = self.ofsl
        elif "OFSL " in command:
            self.ofsl = int(command[5:])
        elif ':FILT:SLOP ' in command:
            self.ofsl = int(command[11:])
        elif ':FILT:TCON ' in command:
            self.tconst = int(command[11:])
        elif ':FILT:TCON?' in command:
            self.response = self.tconst
        elif ':CALC:MULT ' in command:
            self.sens = int(command[11:])
        elif ':CALC:MULT?' in command:
            self.response = self.sens
        elif ':INP:COUP ' in command:
            self.coupling = command[10:]
        elif ':INP:COUP?' in command:
            self.response = self.coupling
        elif ':ROUT2 ' in command:
            self.ref = str(command[7:])
        elif ':ROUT2?' in command:
            self.response = self.ref
        elif 'ICPL?' in command:
            self.response = self.icpl_coup
        elif 'ICPL ' in command:
            self.response = int(command[-1])
        else:
            self.response = 0

    def read(self, termination=None, encoding=None):
        return self.response


if __name__ == "__main__":
    messagebased._resource_manager = messagebased.visa.ResourceManager()
    driver = LI5655.via_usb(manufacturer_id=LI5655.MANUFACTURER_ID, model_code=LI5655.MODEL_CODE)
    driver.initialize()
    print(driver.amplitude)
