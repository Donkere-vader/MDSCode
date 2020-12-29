from .file import File
from .function_lib import FunctionLib
from .line import Line
import json


class Compiler:
    def __init__(self, file_name):
        self.file = File(file_name)
        self.function_lib = FunctionLib()
        self.included_functions = []

    def load_lines(self, lines):
        code_lines = []
        for line in lines:
            new_line = Line()
            if "=" in line:
                line = [part.strip() for part in line.split("=")]
                new_line.var = line[0]
                new_line.value = line[1]
                new_line.type = "set"
            elif "(" in line and line.endswith(")"):
                new_line.type = "function"
                new_line.name = line[:line.index("(")]
                pars = line[
                    line.index("(") + 1:][:-1].split(",")
                new_line.parameters = [
                    par.strip() for par in pars
                ]

            code_lines.append(new_line)

        return code_lines

    def compile_block(self, block):
        """ Compile a code block between {} """
        block_str = []
        for line in self.load_lines(block):
            if line.type == "set":
                block_str.append(f"set {line.var} {line.value}")
            elif line.type == "function":
                if line.name not in self.included_functions:
                    self.included_functions.append(line.name)

                function_info = json.dumps({
                    "name": line.name,
                    "parameters": line.parameters
                })

                block_str.append(f"functioncall:{function_info}")

        return "\n".join(block_str)

    def compile_function_call(self, main_script, function_on_line, line_num):
        main_script = main_script.split("\n")

        line_num = line_num
        for idx, line in enumerate(main_script):
            if not line.startswith("functioncall"):
                line_num += 1
                continue
            inject_script = []
            line = line[line.index(":") + 1:]
            function_info = json.loads(line)

            for i, par in enumerate(function_info['parameters']):
                inject_script.append(
                    f"set {function_info['name']}_par{i} {par}"
                )

            line_num += i + 3
            inject_script.append(f"set return_addr {line_num}")

            inject_script.append(f"set @counter {function_on_line[function_info['name']]}")

            inject_script = "\n".join(inject_script)
            main_script[idx] = inject_script

        return "\n".join(main_script)

    def compile(self):
        # build code blocks
        main_script = self.compile_block(self.file.contents)

        # add functions
        functions_script = []

        function_on_line = {}
        line_num = 1
        for fn in self.included_functions:
            fn_str = self.function_lib[fn]
            functions_script.append(fn_str)
            function_on_line[fn] = line_num
            line_num += fn_str.count("\n") + 1

        functions_script = f"set @counter {line_num}\n" + "\n".join(
            functions_script)

        main_script = self.compile_function_call(main_script, function_on_line, line_num)

        return "\n".join([functions_script, main_script])
