import inspect
from os import path

from SER.interfaces import Component
from lantz.core import messagebased
from lantz.qt import wrap_driver_cls

from .LI5655 import LI5655
from .instrument_ui import Lockin, LockinUI
from .anfatec_driver import AnfatecAMU24, VirtualLockin


class AnfatecLockin(Component):
    conf_ui: LockinUI

    def __init__(self, lockin):
        self.instrument = Lockin(lockin=lockin)
        self.conf_ui = LockinUI(backend=self.instrument)

    @classmethod
    def virtual(cls):
        return cls(wrap_driver_cls(VirtualLockin)())

    @classmethod
    def real(cls):
        return cls(wrap_driver_cls(AnfatecAMU24)())

    @classmethod
    def LI5655(cls):
        messagebased._resource_manager = messagebased.visa.ResourceManager()
        return cls(wrap_driver_cls(LI5655).via_usb(manufacturer_id=LI5655.MANUFACTURER_ID, model_code=LI5655.MODEL_CODE))

    @classmethod
    def demo(cls):
        messagebased._resource_manager = messagebased.visa.ResourceManager()
        folder = path.dirname(inspect.getfile(cls))
        return cls(wrap_driver_cls(VirtualLockin)(path.join(folder, "demo.txt")))

    def close_component(self):
        self.conf_ui.close_graphs()
