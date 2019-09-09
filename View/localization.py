locale_en = {
    "box_gain": "Gain",
    "time_constant": "Time Constant",
    "1_ms": "1 ms",
    "high_reserve": "High Reserve",
    "normal": "Normal",
    "low_noise": "Low Noise",
}
locale_es = {
    "box_gain": "Ganancia"
}
_local_meta_dict = {
    "en": locale_en,
    "es": locale_es
}
locale = dict()


def set_locale(lang):
    locale.update(_local_meta_dict.get(lang, _local_meta_dict["en"]))
