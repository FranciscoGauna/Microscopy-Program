from time import sleep

from PyQt5.QtCore import QThread
from lantz import Feat
from lantz.qt import Backend, InstrumentSlot


class FocusBackend(Backend):
    """
    This class exists to administer the focus daq and provide a simpler and cleaner interface to the Focus Frontend
    """

    def __init__(self, daq, *args, **kwargs):
        self.daq = daq
        super().__init__(*args, **kwargs)
        self.focus = True
        self.focus_check_thread = FocusCheck(self)
        self.focus_check_thread.start()

    def set_widget(self, widget):

        self.focus_check_thread.widget = widget
    @Feat(bool)
    def focus_status(self):
        return self.focus

    @focus_status.setter
    def focus_status(self, focus):
        self.focus = focus

    def update_status(self):
        """
        Updates the status of the focus
        :return:
        """
        self.focus = not self.focus
        return

    def get_focus_status(self):
        return self.focus


class FocusCheck(QThread):
    """
    This thread exists to continually refresh the focus status of the sample, and update the focus if it's incorrect.
    """

    def __init__(self, target: FocusBackend):
        QThread.__init__(self)
        self.target = target
        self.widget = None

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.target.update_status()
            if self.widget:
                self.widget.setChecked(self.target.get_focus_status())
            sleep(0.5)
