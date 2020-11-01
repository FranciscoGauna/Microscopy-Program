import cv2
from lantz import Driver
from lantz.qt import Backend
from lantz.core import Feat


class VirtualDaq(Driver):
    channels = {}

    def __init__(self):
        super().__init__()

    def read_channel(self, channel):
        return self.channels[channel]

    def write_channel(self, channel, value):
        return self.channels.get(channel, 0)


class VirtualDaqBackend(Backend):
    daq: VirtualDaq

    def __init__(self):
        super().__init__()
        self.daq = VirtualDaq()

    def focus(self):
        return True
