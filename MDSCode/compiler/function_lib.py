import json
import os
import pathlib
from .exceptions import ModuleNotFoundError


class FunctionLib:
    def __init__(self, parent):
        self.parent = parent
        self.modules = {}

        self.function_locations = {}
        self.class_locations = {}

        self.path_to_fn_lib = str(pathlib.Path(__file__).parent.absolute()) + "/../function_lib"

        # load std module
        self.import_module("std", add_to_global=True)

    def import_module(self, module_name, add_to_global=False):
        """
        Import a module
        add_to_global would be the same as from module_x import *
        every function from module_x will be accessible as a normal function.
        Without the module_x. prefix
        """
        if module_name in os.listdir(self.path_to_fn_lib):
            module_path = self.path_to_fn_lib + "/" + module_name
        else:
            raise ModuleNotFoundError(f"Module '{module_name}' not found")

        new_module = Module(self, module_path, module_name)
        self.modules[module_name] = new_module

        if add_to_global:
            for function in new_module.functions:
                self.function_locations[function] = module_name
            for clss in new_module.classes:
                self.class_locations[clss] = module_name

    def build_function(self, function_name, module_name=None, class_name=None, *args, **kwargs):
        """ Build a function from one of the modules """
        if module_name is None and class_name is None:
            loc = self.function_locations[function_name]
        elif module_name is not None and class_name is None:
            loc = module_name
        else:
            loc = self.class_locations[self.parent.classes[class_name]['type']]

        code = self.modules[loc].build_function(function_name, class_name, *args, **kwargs)
        return code


class Module:
    def __init__(self, parent, module_path, module_name, all=False):
        self.parent = parent
        self.module_path = module_path
        self.module_name = module_name

        self.functions = {}
        self.classes = {}

        module_init = json.load(open(f"{self.module_path}/init.json", "r"))
        module_type = module_init["type"]

        if module_type == "machinecode":
            for file in module_init["files"]:
                file_data = json.load(open(f"{self.module_path}/{file}.json", "r"))

                for clss in file_data['classes']:
                    if ":" in clss:
                        class_name = clss.split(":")[0]
                        inherited_from = clss.split(":")[1:]
                        clss_data = file_data['classes'][clss]

                        for inh in inherited_from:
                            for function in file_data['classes'][inh]['functions']:
                                clss_data['functions'][function] = {
                                    "type": "inherited",
                                    "inherited_from": inh
                                }

                    else:
                        class_name = clss
                        clss_data = file_data['classes'][clss]
                    self.classes[class_name] = clss_data
                self.functions = file_data['functions']

    def get_function(self, function_name, class_name):
        if class_name is not None:
            function = self.classes[self.parent.parent.classes[class_name]['type']]['functions'][function_name]
        else:
            function = self.functions[function_name]

        if function['type'] in ["forward", "function"]:
            return function
        elif function['type'] == "inherited":
            pass

    def build_function(self, function_name, class_name=None, *args, **kwargs):
        function = self.get_function(function_name, class_name)

        # forward if function is forward else get the code
        if function['type'] == "forward":
            k = {}

            arg_idx = 0
            for par in function['pass_parameters']:
                value = function['pass_parameters'][par]
                if value.startswith("$"):
                    if par in kwargs:
                        k[par] = kwargs[par]
                    else:
                        k[par] = args[arg_idx]
                        arg_idx += 1
                else:
                    if value == "self":
                        k[par] = self.parent.parent.classes[class_name]['name']
                    if value == "return_val":
                        k[par] = self.parent.parent.tree_compiler.latest_return_val

            return self.build_function(function['function'], None, **k)
        # get the code if this is just a normal function
        elif function['type'] == "function":
            code = function['code']

        # compile the kwargs into the code
        for key in kwargs:
            if key in function['parameters']:
                parameter_idx = function['parameters'].index(key)

                code = code.replace(
                    f"${parameter_idx}",
                    str(kwargs[key])
                )

        # compile the args into the code
        args_idx = 0
        for i in range(len(function['parameters'])):
            if args_idx + 1 >= len(args):
                break

            value = None
            rplc = None
            if f"${i}" in code:
                rplc = f"${i}"
                value = str(args[args_idx])
            elif f"$:{i}" in code:
                rplc = f"$:{i}"
                value = str(args[args_idx])
                for char in ["'", '"']:
                    if value.startswith(char) and value.endswith(char):
                        value = value[1:-1]
                        break

            if value is not None:
                code = code.replace(
                    rplc,
                    value
                )
                args_idx += 1

        return code

    def __repr__(self):
        return f"<Module '{self.module_name}'>"
