from .line import Line


class File:
    def __init__(self, file_name):
        self.name = file_name
        self.contents = [line.strip() for line in open(self.name).readlines()]
        self.load_file()
        self.__lines = []

    def load_file(self):
        for line in self.contents:
            new_line = Line()
            if "=" in line:
                line = [part.strip() for part in line.split("=")]
                new_line.var = line[0]

    @property
    def lines(self):
        pass
