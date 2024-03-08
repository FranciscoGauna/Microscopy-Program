import gc
from threading import enumerate as threading_enumerate
from pprint import pprint
from logging import DEBUG

from PyQt5.QtWidgets import QApplication
from lantz.core.log import log_to_screen

from UI.main_window import MainWindow
from components.Platina import Motor


def main():
    app = QApplication([])

    log_to_screen(DEBUG)
    window = MainWindow()

    app.exec()
    window.close_components()


if __name__ == '__main__':
    main()
