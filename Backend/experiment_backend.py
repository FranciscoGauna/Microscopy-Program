from lantz.qt import Backend, InstrumentSlot

from Model.run_experiment import ExperimentWorker


class ExperimentBackend(Backend):
    worker: ExperimentWorker = InstrumentSlot

    def lockin_backend(self):
        return self.worker.lockin

    def results(self):
        return self.worker.results