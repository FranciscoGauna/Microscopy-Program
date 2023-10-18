from PyQt5.QtWidgets import QApplication
from SER import launch_app
from SER.interfaces import ComponentInitialization
from components.HP33120AFunGen import HPFunGen

app = QApplication([])
fungen_component = ComponentInitialization(HPFunGen(10), -9000, 0, 0, "Fungen 1")
launch_app(app, [fungen_component], [], [], [])