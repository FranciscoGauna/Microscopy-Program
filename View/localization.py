from os.path import join

locale_debug = {}  # Always empty

locale_en = {
    "linear": "Linear",
    "box_gain": "Gain",
    "time_constant": "Time Constant",
    "1_ms": "1 ms",
    "high_reserve": "High Reserve",
    "normal": "Normal",
    "low_noise": "Low Noise",
    "fungen_models": "Function Generators",
    "load_conf": "Load Configuration",
    "pos_order": "Order by Position",
    "freq_order": "Order by Frequency",
    "virtual_camera": "Virtual Camera",
    "virtual_daq": "Virtual DAQ",
    "lockin_models": "Lockin Models",
    "exposure": "Exposure",
    "lockin_configuration": "Lockin Configuration",
    "sample_alignment": "Sample Alignment",
    "protocol_selection": "Protocol Selection",
    "thermal_imaging": "Thermal Imaging",
    "auto_limits": "Auto Limit",
    "roll_off": "Roll Off",
    "harmonic": "Harmonic",
    "input_gain": "Input Gain",
    "coupling": "Coupling",
    "external_reference": "External Reference",
    "external_frequency": "External Frequency",
    "lockin_frequency": "Internal Frequency",
    "lockin_amplitude": "Internal Amplitude",
    "lockin_phase": "Internal Phase",
    "real_part_mv": "Real Part (mV)",
    "imaginary_part_mv": "Imaginary Party (mV)",
    "x_motor": "Motor X",
    "y_motor": "Motor Y",
    "next_pos": "Next Position",
    "current_pos": "Current Position",
    "prev_pos": "Previous Position",
    "freq_start": "Frequency Start",
    "freq_end": "Frequency End",
    "freq_amount": "Frequency Amount",
    "repeat_amount": "Repeat Amount",
    "oper_order": "Operation Order",
    "scale": "Scale",
    "save": "Save",
    "load": "Load",
    "reset": "Reset",
    "point": "Point",
    "line": "Line",
    "rect": "Rectangle",
    "x": "X",
    "y": "Y",
    "draw_point": "Draw Point",
    "add_point": "Add Point",
    "line_steps": "Line Steps",
    "draw_line": "Draw Line",
    "add_line": "Add Line",
    "start_x": "Start X",
    "end_x": "End X",
    "start_y": "Start Y",
    "end_y": "End Y",
    "x_steps": "X Steps",
    "y_steps": "Y Steps",
    "draw_rect": "Draw Rectangle",
    "add_rect": "Add Rectangle",
    "load_offset": "Load Offset",
    "use_fixed_time_constant": "Use Fixed Time Constant",
    "period_number": "Period Number",
    "fixed_time_constant": "Fixed Time Constant",
    "start": "Start",
    "progress": "Progress",
    "current_point": "Current Point",
    "time_remaining": "Time Remaining",
    "amplitude": "Amplitude",
    "plus_zoom": "+ Zoom",
    "minus_zoom": "- Zoom",
    "reset_zoom": "Reset Zoom",
    "image": "Image",
    "histogram": "Histogram",
    "run_exp": "Run Experiment",
    "phase": "Phase",
    "control_focus": "Control Focus",
    "fc_current_percent": "FC Current %",
    "probe_current_percent": "Probe Current %",
    "on_off": "On/Off",
    "efocus": "E Focus",
    "sum": "Sum",
    "reflectance": "Reflectance",
    "min_sum": "Minimum Sum",
    "z_focus": "Z Focus",
    "dn": "Δn",
    "range": "Range",
    "offset_sum_fe": "Offset Sum FE (V)",
    "shutdown_on_end": "Shutdown on End",
    "enable": "Enable",
    "stop": "Stop",
    "speed_2": "Speed Z",
    "focus": "Focus",
    "amplitude_mv": "mV",
    "pop_out_camera": "Pop Out Camera Window",
    "close_camera": "Close Camera Window",
}

locale_es = {
    "box_gain": "Ganancia",
    "fungen_models": "Generador de Funciones",
    "load_conf": "Cargar Configuracion",
}

_local_meta_dict = {
    "debug": locale_debug,
    "en": locale_en,
    "es": locale_es
}


class Locale:
    log = open(join("logs", "text.log"), "w+", encoding="utf-8")

    def __init__(self):
        self.loc_keys = _local_meta_dict["debug"]

    def get(self, key: str, backup: str) -> str:
        if key not in self.loc_keys:
            self.log.write(key + ": key missing\n")
            self.log.flush()
        return self.loc_keys.get(key, backup)

    def set_locale(self, language):
        self.loc_keys = _local_meta_dict.get(language, _local_meta_dict["en"])


locale = Locale()


def set_locale(lang):
    """Changes the locale dictionary to the one with appropiate language"""
    locale.set_locale(lang)
