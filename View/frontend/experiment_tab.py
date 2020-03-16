from PyQt5.QtWidgets import QGraphicsScene
from lantz.qt import Frontend

from View.frontend.run_experiment import ExperimentWorker


class ExperimentTab(Frontend):
    gui = ("UI", "experiment_tab.ui")
    backend: ExperimentWorker
    scene: QGraphicsScene

    def setupUi(self):
        pass

    def connect_backend(self):
        self.scene = QGraphicsScene(0, 0, 200, 200)
        self.widget.map_view.setScene(self.scene)