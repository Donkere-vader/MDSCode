from compiler import Compiler

# file_name = input("File name: ").strip()
file_name = "code.mds"

compiler = Compiler(file_name)
print(compiler.compile())
