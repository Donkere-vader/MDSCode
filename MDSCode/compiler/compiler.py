from .function_lib import FunctionLib
from .lark_loader import load_lark_tree
from .exceptions import CompileError
from .tree_compiler import TreeCompiler
from string import ascii_letters


class Compiler:
    def __init__(self, file_name):
        self.file_name = file_name

    def start(self):
        self.function_lib = FunctionLib(self)
        self.tree_compiler = TreeCompiler(self)
        self.included_functions = []
        self.classes = {}
        self.return_value = []

    def load_tree(self):
        self.tree = load_lark_tree(self.file_name)

    def compile_line(self, line):
        machine_line = ""
        # get the thing the line is acctually about
        line = line.children[0]
        line_type = line.data  # for readabillity

        if line_type == "class_function_call":
            machine_line = self.tree_compiler.compile_class_function_call(line)
        elif line_type == "function_call":
            machine_line = self.tree_compiler.compile_function_call(line)
        elif line_type == "game_obj_set":
            set_statement = line.children[0]
            variable_name, value = self.tree_compiler.compile_set(set_statement)
            self.classes[variable_name] = {
                "name": value,
                "type": "".join([i for i in value if i in ascii_letters])
            }
        elif line_type == "set":
            variable_name, value = self.tree_compiler.compile_set(line)
            machine_line = f"set {variable_name} {value}"

        return machine_line

    def compile_code(self, code):
        script = ""

        # compile all lines
        for child in code.children:
            self.tree_compiler.reset()
            code = self.compile_line(child)
            script += "\n".join(self.tree_compiler.pre_code) + "\n" + code + "\n"

        return script.replace("\n\n", "\n")

    def compile(self):
        self.start()

        self.load_tree()

        first_code_block = self.tree.children[0]
        code = self.compile_code(first_code_block)

        return code.strip()
