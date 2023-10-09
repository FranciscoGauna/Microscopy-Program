import pyvisa
from lantz import MessageBasedDriver, Feat
from lantz.core.messagebased import get_resource_manager


class HP33120AFungen(MessageBasedDriver):
    """Lantz Signal Generator.
    """

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}

    @Feat()
    def idn(self):
        return self.query('?IDN')


if __name__ == '__main__':
    device = HP33120AFungen.via_gpib(10)
    device.initialize()
    print(device.idn)
