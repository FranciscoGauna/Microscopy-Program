from time import sleep

from PyQt5.QtCore import QThread
from lantz import Feat
from lantz.qt import Backend, InstrumentSlot


class FocusBackend(Backend):
    """
    This class exists to administer the focus daq and provide a simpler and cleaner interface to the Focus Frontend
    """

    def __init__(self, daq, motor_backend, *args, **kwargs):
        self.daq = daq
        self.motor_backend = motor_backend
        super().__init__(*args, **kwargs)
        self.focus = True
        self._fc_current = 0
        self._probe_current = 0
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

    @Feat(limits=(0, 100))
    def fc_current(self):
        return self._fc_current

    @fc_current.setter
    def fc_current(self, percentage):
        self._fc_current = percentage

    @Feat(limits=(0, 100))
    def probe_current(self):
        return self._probe_current

    @probe_current.setter
    def probe_current(self, percentage):
        self._probe_current = percentage

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
