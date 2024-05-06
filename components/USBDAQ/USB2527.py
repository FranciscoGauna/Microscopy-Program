from typing import Union
from time import sleep

from lantz.core.foreign import Driver
from mcculw import ul
from mcculw.enums import ULRange, DigitalPortType, DigitalIODirection


class USB2527(Driver):
    """
    Class that represents an instance of an USB2527. Requires an external driver to be installed and configured.
    Manual: https://files.digilent.com/manuals/USB-2527.pdf
    Link to driver: https://digilent.com/reference/software/universal-library/windows/start
    """

    board_num: int

    def __init__(self, board_num: int):
        """
        Parameters
        ----------
        board_num : int
            The number od the associated board, this number is assigned by the instacal program that comes with
            the measurement computing downloader.
        """
        super().__init__()
        self.board_num = board_num
        self.range = ULRange.BIP10VOLTS  # Should always be this range for input in the board

    def read_analog_input(self, channel, input_range=ULRange.BIP10VOLTS) -> float:
        value = ul.a_in(self.board_num, channel, input_range)
        return ul.to_eng_units(self.board_num, input_range, value)

    def write_analog_input(self, channel, value):
        """
        Function that writes the analog input. Note that for this model, the range is always BBIP10VOLTS
        """
        value = ul.from_eng_units(self.board_num, self.range, value)
        ul.a_out(self.board_num, channel, self.range, value)

    def configure_digital_port(self, port: DigitalPortType, write: DigitalIODirection):
        """
        @param port: DigitalPortType, valid inputs DigitalPortType.FIRSTPORTA, DigitalPortType.FIRSTPORTB,
         DigitalPortType.FIRSTPORTC
        @param write: DigitalIODirection indicating if the port is set up to for input or output.
        """
        ul.d_config_port(self.board_num, port, write)

    def read_digital_input(self, port: DigitalPortType, bit):
        return ul.d_bit_in(self.board_num, port, bit)

    def write_digital_input(self, port: DigitalPortType, bit, value: bool):
        ul.d_bit_out(self.board_num, port, bit, value)


if __name__ == "__main__":
    device = USB2527(0)
    device.configure_digital_port(DigitalPortType.FIRSTPORTA, DigitalIODirection.OUT)
    device.write_digital_input(DigitalPortType.FIRSTPORTA, 2, True)

    for i in range(50):
        device.write_digital_input(DigitalPortType.FIRSTPORTA, 0, True)
        sleep(0.1)
        device.write_digital_input(DigitalPortType.FIRSTPORTA, 0, False)
        sleep(0.1)
    