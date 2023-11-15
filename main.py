from logging import DEBUG

from PyQt5.QtWidgets import QApplication
from lantz.core.log import log_to_screen

from UI.main_window import MainWindow

app = QApplication([])

log_to_screen(DEBUG)
window = MainWindow()

app.exec()
