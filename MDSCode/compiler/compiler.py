from .file import File
from .function_lib import FunctionLib
from.lark_loader import load_lark_tree


class Compiler:
    def __init__(self, file_name):
        self.file = File(file_name)

    def start(self):
        self.function_lib = FunctionLib()
        self.included_functions = []
        self.game_objects = {}

    def load_tree(self):
        self.tree = load_lark_tree(self.file.name)

    def compile_return_obj(self, tree, num=0):
        parameter_calculations = []
        code = ""

        if tree.data == 'class_function_call':
            # get target class
            target = tree.children[0]
            target = self.game_objects[target]

            # get function information
            function_call = tree.children[1]
            function_name = function_call.children[0]

            if function_name == "print":
                function_name = "printnow"

            parameter_list_obj = function_call.children[1]
            parameter_list = []

            # p.children[0] for p in parameter_list_obj.children

            for p in parameter_list_obj.children:
                num += 1
                pc, c = self.compile_return_obj(p.children[0], num=num)
                parameter_calculations.append(pc)
                parameter_list.append(c)

            parameter_calculations.append(self.function_lib.build_function(
                function_name,
                *parameter_list,
                target=target
            ))
            parameter_calculations.append(
                f"set mdsc_return_value{num} mdsc_return_value"
            )
            code = f"mdsc_return_value{num}"
        elif tree.data == 'class_variable_call':
            # get target class
            target = tree.children[0]
            target = self.game_objects[target]

            parameter_calculations.append(self.function_lib.build_function(
                'sensor',
                target=target,
                value=tree.children[1]
            ))

            parameter_calculations.append(
                f"set mdsc_return_value{num} mdsc_return_value"
            )
            code = f"mdsc_return_value{num}"
        elif tree.data == 'value':
            code = tree.children[0]
        elif tree.data == 'return_obj' or tree.data == 'obj':
            pc, c = self.compile_return_obj(
                tree.children[0], num=num+1
            )
            parameter_calculations, code = [pc], c
        elif tree.data == 'opperation':
            opperator = {
                "+": "add",
                "-": "sub",
                "*": "mul",
                "/": "div",
                "//": "idiv",
                "%": "mod",
                "**": "pow"
            }[tree.children[1].children[0]]

            values = []
            for value in [tree.children[0], tree.children[2]]:
                num += 1
                pc, c = self.compile_return_obj(value, num)
                parameter_calculations.append(pc)
                values.append(c)

            parameter_calculations.append(self.function_lib.build_function(
                "opperation",
                op=opperator,
                *values
            ))

            parameter_calculations.append(
                f"set mdsc_return_value{num} mdsc_return_value"
            )
            code = f"mdsc_return_value{num}"
        else:
            print(f"UNKNOWN TREE: {tree}")

        return "\n".join([
            str(i) for i in parameter_calculations]), code

    def compile_code(self, tree):
        code = ""

        for line in tree.children:
            new_code = ""
            line_action = line.children[0]
            # print(line_action)

            # load %DEFINE objects
            if line_action.data == 'game_obj_def':
                set_obj = line_action.children[0]
                obj_name = set_obj.children[0]
                in_game_name = set_obj.children[1].children[0].children[0]
                self.game_objects[obj_name] = in_game_name
            # msg_block.print() functionallity
            elif line_action.data == 'class_function_call':
                pc, c = self.compile_return_obj(line_action)
                new_code = pc + new_code
            elif line_action.data == 'set':
                var_name = line_action.children[0]
                pc, c = self.compile_return_obj(line_action.children[1])
                new_code = pc + new_code + f"\nset {var_name} {c}\n"

            code += new_code

        while "\n\n" in code:
            code = code.replace("\n\n", "\n")

        return code

    def compile(self):
        self.start()

        self.load_tree()

        first_code_block = self.tree.children[0]
        code = self.compile_code(first_code_block)

        return code
