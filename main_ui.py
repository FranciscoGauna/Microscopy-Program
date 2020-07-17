from Drivers.Lockin.anfatec_driver import AnfatecAMU24
from Backend.lockin_options import LockinBackend
from View.lockin_window import LockinControlUi
from lantz.core.log import log_to_screen, INFO
from lantz.qt import start_gui_app, wrap_driver_cls

log_to_screen(INFO)

QAmplitudeSensor = wrap_driver_cls(AnfatecAMU24)

with QAmplitudeSensor() as lockin:
    app = LockinBackend(lockin=lockin)
    start_gui_app(app, LockinControlUi)
    pass
