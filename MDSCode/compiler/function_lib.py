

class FunctionLib:
    def __init__(self):
        self.standard_functions = {
            "printnow": "print printnow_par0 \nprintflush printnow_par1",
            "print": "print print_par0",
            "printflush": "printflush printflush_par0",
            "write": "write write_par0 write_par1 write_par2",
            "read": "read result read_par0 read_par1",
            "sensor": "sensor result sensor_par0 sensor_par1"
        }
        self.custom_functions = {

        }

    def __getitem__(self, key):
        if key in self.standard_functions:
            fn = self.standard_functions[key]
        elif key in self.custom_functions:
            fn = self.custom_functions[key]

        return fn + "\n" + "set @counter return_addr"
