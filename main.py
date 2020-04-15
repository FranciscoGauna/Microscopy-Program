import configparser
import argparse

from lantz.qt import start_gui_app
from lantz.core.log import log_to_screen, DEBUG

from Backend.main_backend import MainBackend

from View.localization import set_locale
from View.program_window import MainFrontend

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locale", dest='locale', action='store', help="Indicates in which language should be launched the program")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        config["DEFAULT"]["env"]
    except KeyError:
        config["DEFAULT"]["env"] = "usr"
    if config["DEFAULT"]["env"] == "dev":
        pass
        #log_to_screen(DEBUG)
    if args.locale:
        set_locale(args.locale)
    elif config["DEFAULT"]["env"] != "dev":
        try:
            set_locale(config["DEFAULT"]["locale"])
        except KeyError:
            set_locale("en")


app = MainBackend()
start_gui_app(app, MainFrontend)
