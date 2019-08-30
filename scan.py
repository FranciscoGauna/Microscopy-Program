from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from lantz.qt import QtGui

from Model.AnfatecDriver import AnfatecAMU24

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.lockin = AnfatecAMU24()

        layout = QVBoxLayout()

        self.amplitude_widget = QLCDNumber(self)
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.amplitude_widget)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def oh_no(self):
        pass

    def recurring_timer(self):
        self.amplitude_widget.display(self.lockin.amplitude.magnitude)

app = QApplication([])
window = MainWindow()
app.exec_()
