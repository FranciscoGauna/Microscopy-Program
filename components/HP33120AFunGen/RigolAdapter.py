from lantz.drivers.rigol.dg1022 import DG1022
from lantz.core import messagebased


class RigolAdapter:
    rigol: DG1022

    def __init__(self):
        messagebased._resource_manager = messagebased.visa.ResourceManager()
        self.rigol = DG1022.via_usb(manufacturer_id="0x1AB1")

    def initialize(self):
        self.rigol.initialize()
        self.rigol.write("VOLT:UNIT VPP")

    def apply(self, shape, freq, amplitude, offset):
        self.rigol.write(f"APPL:{shape} {freq},{amplitude},{offset}")


if __name__ == "__main__":
    driver = RigolAdapter()
    driver.initialize()
    driver.apply("SQU", 10000, 2.5, 0)
