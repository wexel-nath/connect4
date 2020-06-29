import os


def get_full_file_path(file: str):
    return os.path.join(os.getcwd(), "out", file)
