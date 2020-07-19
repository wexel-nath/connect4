import os

from hyperparameters import DECAY, DEPTH, GAMMA, LEARNING_RATE

VERSION = 7

folders = {}


def get_folder_name(sub_dir: str):
    global folders
    path = folders.get(sub_dir, "")
    if path != "":
        return path

    folder = f"v-{VERSION}_d-{DECAY}_g-{GAMMA}_lr-{LEARNING_RATE}"
    folder_name = os.path.join(os.getcwd(), "out", folder, sub_dir)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    folders[sub_dir] = folder_name
    return folder_name


def get_full_file_path(file: str, sub_dir: str = ""):
    return os.path.join(get_folder_name(sub_dir), file)
