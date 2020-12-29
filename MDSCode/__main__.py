from compiler import Compiler

# file_name = input("File name: ").strip()
file_name = "code.mds"

compiler = Compiler(file_name)
code = compiler.compile()
print(code)
# print("\n".join([f"{idx}. {line}" for idx, line in enumerate(code.split("\n"))]))
