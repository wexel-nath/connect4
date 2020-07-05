class File:
    def __init__(self, name: str, mode: str):
        self.file = open(name, mode)

    def write(self, line: str):
        self.file.write(line + "\n")

    def write_dict(self, dict):
        for key, val in dict.items():
            self.write(f"{key}: {val}")

    def close(self):
        self.file.close()
