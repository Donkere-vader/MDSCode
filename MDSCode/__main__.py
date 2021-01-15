from compiler import Compiler
import sys


__author__ = "donkere-vader"
__version__ = "development"


class InvalidCommand(Exception):
    pass


def run_compiler(file_name, output_file=None):
    print(f"Compiling '{file_name}'")
    compiler = Compiler(file_name)
    code = compiler.compile()

    print("\n# COMPILED CODE #")
    print(code)

    if output_file is not None:
        with open(output_file, 'w') as f:
            f.write(code)

        print()
        print(f"Saved to: '{output_file}'")


if __name__ == "__main__":
    output_file = None
    for idx, arg in enumerate(sys.argv):
        if arg == "--output" or arg == "-o":
            try:
                output_file = sys.argv[idx + 1]
            except IndexError:
                raise InvalidCommand("Please specify a value for the output flag")

    try:
        file_name_argument = sys.argv[1]
    except IndexError:
        raise InvalidCommand("Please specify a file you want to compile: ``python3 MDSCode/ code.mdsc``")

    run_compiler(file_name_argument, output_file=output_file)
