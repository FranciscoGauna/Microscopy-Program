import gc
from pprint import pprint
from logging import DEBUG

from PyQt5.QtWidgets import QApplication
from lantz.core.log import log_to_screen

from UI.main_window import MainWindow
from components.Platina import Motor


def main():
    app = QApplication([])

    # log_to_screen(DEBUG)
    window = MainWindow()

    app.exec()


if __name__ == '__main__':
    main()
    objects = gc.get_objects(generation=None)
    objects = list(filter(lambda x:  isinstance(x, Motor), objects))
    for i in range(15):
        refs = gc.get_referrers(objects[0])
        refs.remove(objects)
        print(refs)
        objects = refs
    print("end")
