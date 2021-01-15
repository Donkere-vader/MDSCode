

class TreeCompiler:
    def __init__(self, parent):
        # for accesing Compiler.function_lib
        self.parent = parent

        # compiling vars
        self.pre_code = []
        self.in_use_return_val = []

    def reset(self):
        self.pre_code = []
        self.in_use_return_val = []

    def __get_free_variable_num(self):
        i = 0
        while i in self.in_use_return_val:
            i += 1
        return i

    def occupy_variable_num(self):
        num = self.__get_free_variable_num()
        self.in_use_return_val.append(num)
        return num

    @property
    def latest_return_val(self):
        val = self.in_use_return_val[-1]
        del self.in_use_return_val[-1]
        return f"msdc_return_val_{val}"

    def compile_return_obj(self, tree):
        obj_type = tree.children[0].data

        return_val = f"msdc_return_val_{self.occupy_variable_num()}"

        if obj_type == "class_function_call":
            self.pre_code.append(
                self.compile_class_function_call(tree.children[0])
            )
        elif obj_type == "class_variable_call":
            self.pre_code.append(
                self.compile_class_variable_call(tree.children[0])
            )
        elif obj_type == "function_call":
            self.pre_code.append(
                self.compile_function_call(tree.children[0])
            )

        elif obj_type == "opperation":
            self.pre_code.append(
                self.compile_opperation(tree.children[0])
            )
        elif obj_type == "evaluation":
            pass  # TODO

        return return_val

    def compile_class_variable_call(self, tree):
        target = self.parent.classes[tree.children[0]]['name']
        variable = tree.children[1]

        code = self.parent.function_lib.build_function(
            "sensor",
            None,
            None,
            **{
                "return_val": self.latest_return_val,
                "target": target,
                "value": variable
            }
        )

        return code

    def compile_obj(self, tree):
        child = tree.children[0]

        if child.data == "value":
            return child.children[0]
        elif child.data == "return_obj":
            return self.compile_return_obj(child)

    def compile_opperation(self, tree):
        opperator = tree.children[1].children[0]
        num1 = self.compile_obj(tree.children[0])
        num2 = self.compile_obj(tree.children[2])

        opperator = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div",
            "//": "idiv",
            "**": "pow",
            "%": "mod"
        }[opperator]

        return f"op {opperator} {self.latest_return_val} {num1} {num2}"

    def compile_set(self, tree):
        variable_name = tree.children[0]
        value = self.compile_obj(tree.children[1])
        return variable_name, value

    def compile_parameter(self, tree):
        """ returns a parname with a not None value if it is a kwarg else only return parvalue as not None value, thus a arg """
        parname = None
        parvalue = None

        if len(tree.children) == 2:
            parname = tree.children[0]
            parvalue = self.compile_obj(tree.children[1])
        else:
            parvalue = self.compile_obj(tree.children[0])
        return parname, parvalue

    def compile_parameter_list(self, tree):
        """ Make a list of args and dict of kwargs """
        args = []
        kwargs = {}
        for child in tree.children:
            parname, parvalue = self.compile_parameter(child)
            if parname is not None:
                kwargs[parname] = parvalue
            else:
                args.append(parvalue)

        return args, kwargs

    def compile_function_call(self, tree, class_name=None):
        function_name = tree.children[0]
        a, k = self.compile_parameter_list(tree.children[1])

        code = self.parent.function_lib.build_function(
            function_name,
            None,
            class_name,
            *a,
            **k
        )

        return code

    def compile_class_function_call(self, tree):
        class_name = tree.children[0]
        code = self.compile_function_call(tree.children[1], class_name)
        return code
