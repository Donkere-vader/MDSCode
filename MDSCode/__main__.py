from compiler import Compiler
import sys


__author__ = "donkere-vader"
__version__ = "beta"


class InvalidCommand(Exception):
    pass


def run_compiler(file_name):
    compiler = Compiler(file_name)
    code = compiler.compile()

    print("\n# COMPILED CODE #")
    print(code)


if __name__ == "__main__":
    try:
        file_name_argument = sys.argv[1]
    except IndexError:
        raise InvalidCommand("Please specify a \
file you want to compile: ``python3 MDSCode/ code.mdsc``")

    run_compiler(file_name_argument)
