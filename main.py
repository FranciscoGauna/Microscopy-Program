from lantz.drivers.examples import LantzSignalGenerator
from lantz.qt.app import start_gui
from Model.AnfatecDriver import AnfatecAMU24

inst = AnfatecAMU24()
start_gui('View\\UI\\fungen.ui', inst)
