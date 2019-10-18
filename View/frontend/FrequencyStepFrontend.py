from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from Backend.frequency_backend import FrequencyController
from View.localization import locale


class FrequencyStepFrontend(Frontend):
    backend: FrequencyController
    gui = ("UI", "frequency_spread.ui")

    def setupUi(self):
        self.widget.freq_start_label.setText(locale.get("freq_start", "str_freq_start"))
        self.widget.freq_end_label.setText(locale.get("freq_end", "str_freq_end"))
        self.widget.freq_amount_label.setText(locale.get("freq_amount", "str_freq_amount"))
        self.widget.repeat_n_label.setText(locale.get("repeat_amount", "str_repeat_amount"))
        self.widget.oper_order_label.setText(locale.get("oper_order", "str_oper_order"))
        self.widget.scale_label.setText(locale.get("scale", "str_scale"))

    def connect_backend(self):
        connect_feat(self.widget.freq_start_input, self.backend, "start_f")
        connect_feat(self.widget.freq_end_input, self.backend, "end_f")
        connect_feat(self.widget.freq_amount_input, self.backend, "amount_f")
        connect_feat(self.widget.repeat_n_input, self.backend, "amount_repeat")
        connect_feat(self.widget.scale_cb, self.backend, "scale")

        connect_feat(self.widget.oper_order_cb, self.backend, "point_order")
