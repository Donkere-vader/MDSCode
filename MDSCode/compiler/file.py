

class File:
    def __init__(self, file_name):
        self.name = file_name
        self.contents = [line.strip() for line in open(self.name).readlines()]
