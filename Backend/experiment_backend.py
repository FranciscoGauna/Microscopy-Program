from lantz.qt import Backend, InstrumentSlot

from Model.run_experiment import ExperimentWorker


class ExperimentBackend(Backend):
    worker: ExperimentWorker = InstrumentSlot
