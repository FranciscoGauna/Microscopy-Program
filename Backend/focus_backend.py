from time import sleep

from PyQt5.QtCore import QThread
from lantz import Feat
from lantz.qt import Backend, InstrumentSlot


class FocusBackend(Backend):
    """
    This class exists to administer the focus daq and provide a simpler and cleaner interface to the Focus Frontend
    """
    focus = True

    def __init__(self, daq, *args, **kwargs):
        self.daq = daq
        super().__init__(*args, **kwargs)
        self.focus_check_thread = FocusCheck(self)
        self.focus_check_thread.start()

    @Feat
    def focus_status(self):
        return self.focus

    @focus_status.setter
    def focus_status(self, focus):
        self.focus = focus


class FocusCheck(QThread):
    """
    This thread exists to continually refresh the focus status of the sample, and update the focus if it's incorrect.
    """
    def __init__(self, target):
        QThread.__init__(self)
        self.target = target

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            sleep(1)
