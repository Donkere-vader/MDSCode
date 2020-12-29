from .file import File


class Compiler:
    def __init__(self, file_name):
        self.file = File(file_name)

    def compile_block(self, block):
        """ Compile a code block between {} """
        for line in block:
            print(block)

    def compile(self):
        output = self.compile_block(self.file.contents)
        return output
