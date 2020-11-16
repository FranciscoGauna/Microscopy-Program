from lantz.qt import Backend, InstrumentSlot

from Drivers.Lockin.anfatec_driver import VirtualLockin
from Model.run_experiment import ExperimentWorker


class ExperimentBackend(Backend):
    """
    Experiment Backend is a class that administers and gives an interface to access the Experiment Worker
    """
    worker: ExperimentWorker = InstrumentSlot

    def lockin_backend(self) -> VirtualLockin:
        """
        Returns the Lockin Driver that the experiment worker is associated with
        :return: Lockin Driver
        """
        return self.worker.lockin

    def results(self) -> list:
        """
        This returns a reference to the list the experiment worker uses to store the current results

        :return: List of ResultPoint
        """
        return self.worker.results
