

class FunctionLib:
    def __init__(self):
        self.functions = {
            "printnow": "print <value> \nprintflush <target>",
            "print": "print <value>",
            "printflush": "printflush <target>",
            "write": "write <value> <target> <location>",
            "read": "read mdsc_return_value <target> <location>",
            "sensor": "sensor mdsc_return_value <target> @<value>",
            "opperation": "op <op> mdsc_return_value <value1> <value2>"
        }

    def build_function(self, function_name, *args, **kwargs):
        function = self.functions[function_name]

        for key in kwargs:
            function = function.replace(f"<{key}>", kwargs[key])

        parameters = []
        new_par = ""
        adding_to_par = False
        for char in function:
            if char == "<":
                adding_to_par = True
                continue
            elif char == ">":
                adding_to_par = False
                parameters.append(new_par)
                new_par = ""

            if adding_to_par:
                new_par += char

        for idx, arg in enumerate(args):
            function = function.replace(f"<{parameters[idx]}>", str(arg))

        # if return value not set in function
        if "mdsc_return_value" not in function:
            function = f"set mdsc_return_value null\n{function}"

        return function
