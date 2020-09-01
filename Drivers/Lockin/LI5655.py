# -*- coding: utf-8 -*-
"""
    lantz.drivers.stanford.sr830
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2015 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from collections import OrderedDict

import numpy as np
from lantz import Action, Feat, DictFeat, ureg
from lantz import MessageBasedDriver


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
    ('10 us', 0),
    ('30 us', 1),
    ('100 us', 2),
    ('300 us', 3),
    ('1 ms', 4),
    ('3 ms', 5),
    ('10 ms', 6),
    ('30 ms', 7),
    ('100 ms', 8),
    ('300 ms', 9),
    ('1 s', 10),
    ('3 s', 11),
    ('10 s', 12),
    ('30 s', 13),
    ('100 s', 14),
    ('300 s', 15),
    ('1 ks', 16),
    ('3 ks', 17),
    ('10 ks', 18),
    ('30 ks', 19),
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

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}

    @Feat(limits=(1, 19999, 1))
    def harmonic(self):
        """Detection harmonic.
        """
        return self.query(':FREQ:MULT?')

    @harmonic.setter
    def harmonic(self, value):
        self.query(':FREQ:MULT {}'.format(value))


class ResourceDummy:
    response = 0
    ofsl = 6

    def write(self, command, termination=None, encoding=None):
        if "OFSL?" in command:
            self.response = self.ofsl
        elif "OFSL " in command:
            self.oflt = int(command[5:])
        else:
            self.response = 0

    def read(self, termination=None, encoding=None):
        return self.response
