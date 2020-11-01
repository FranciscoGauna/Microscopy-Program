from pathlib import Path
from importlib import import_module
import pydoc
import os


def import_all_files(folder: Path, i_list):
    for sub_file in folder.iterdir():
        if sub_file.is_file() and sub_file.suffix == ".py":
            i_list.append(import_module(str(sub_file).replace("\\", ".")[:-3]))
        if sub_file.is_dir():
            import_all_files(sub_file, i_list)


main_folder = Path(".")
import_list = []
for file in main_folder.iterdir():
    if file.is_dir():
        import_all_files(file, import_list)
os.chdir("Documentation")
for imported_file in import_list:
    pydoc.writedoc(imported_file)
