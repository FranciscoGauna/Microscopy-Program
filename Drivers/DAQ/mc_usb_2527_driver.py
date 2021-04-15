from lantz import Driver
from lantz.qt import Backend
from mcculw.enums import ULRange
from mcculw.ul import a_in, a_out, d_in, d_out


class USB2527(Driver):
    """The Software for this program is InstaCal"""
    board_num: int

    def __init__(self, board_num):
        super().__init__()
        self.board_num = board_num

    def read_analog_channel(self, channel):
        return a_in(self.board_num, channel, ULRange.BIP5VOLTS)

    def write_analog_channel(self, channel, value):
        a_out(self.board_num, channel, ULRange.BIP5VOLTS, value)

    def read_digital_channel(self, channel):
        return d_in(self.board_num, channel)

    def write_digital_channel(self, channel, value):
        d_out(self.board_num, channel, value)


class USB2527DaqBackend(Backend):
    daq: USB2527

    def __init__(self, board_num):
        super().__init__()
        self.daq = USB2527(board_num)

    def focus(self):
        return True

    """This method returns the focus of the laser more quickly but with less precision. It utilizes the ef adapter"""
    def focus_fast(self):
        return True

    def potencia_lazer(self):
        return 0