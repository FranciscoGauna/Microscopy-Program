from Model.AnfatecDriver import AnfatecAMU24
from lantz.qt import Backend, Frontend, InstrumentSlot


class LockinControl(Backend):
    lockin: AnfatecAMU24 = InstrumentSlot

    last_amplitude = None

    def update_amplitude(self):
        self.log_debug('Updating Amplitude')
        self.last_amplitude = self.lockin.amplitude


class LockinControlUi(Frontend):

    backend: LockinControl

    # gui = 'UI/mainWindow.ui'
    gui = 'UI/test.ui'

    def setupUi(self):
        super().setupUi()
        print(90)
        # self.widget.doubleSpinBox.setValue(90.0)
        # self.widget.radioButton.pressed.connect(self.update_amplitude)
        self.widget.button.clicked.connect(lambda: print("asd"))

    def connect_backend(self):
        super().connect_backend()

        #self.connect_feat(self.widget.doubleSpinBox, self.backend.lockin, 'amplitude')
        #self.widget.radioButton.pressed.connect(self.update_amplitude)

    def update_amplitude(self):
        print("Success")
        exit()


if __name__ != '__main__':
    from lantz.core.log import log_to_screen, DEBUG
    from lantz.qt import start_gui_app, wrap_driver_cls

    log_to_screen(DEBUG)

    QAmplitudeSensor = wrap_driver_cls(AnfatecAMU24)

    with QAmplitudeSensor() as lockin:
        app = LockinControl(lockin=lockin)

        start_gui_app(app, LockinControlUi)
