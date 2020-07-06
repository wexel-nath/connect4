import os

from hyperparameters import DECAY, GAMMA, LEARNING_RATE


def get_folder_name():
    folder = f"leaky-relu_d-{DECAY}_g-{GAMMA}_lr-{LEARNING_RATE}"
    dir = os.path.join(os.getcwd(), "out", folder)
    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir


def get_full_file_path(file: str):
    return os.path.join(get_folder_name(), file)
