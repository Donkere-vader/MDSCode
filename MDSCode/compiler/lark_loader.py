from lark import Lark
from lark import Transformer
import pathlib


class MyTransformer(Transformer):
    def letter(self, items):
        return str(items[0])

    def digit(self, items):
        return int(items[0])

    def int(self, items):
        return int("".join([str(i) for i in items]))

    def underscore(self, items):
        return "_"

    def variable(self, items):
        return "".join([str(i) for i in items])

    def variable_character(self, items):
        return items[0]

    def STRING(self, items):
        return str(items)


def load_lark_tree(file):
    path_to_this_file = pathlib.Path(__file__).parent.absolute()

    gramar = open(f'{path_to_this_file}/grammer.lark').read()
    code = open(file).read()
    lark = Lark(gramar)

    tree = lark.parse(code)
    return MyTransformer().transform(tree)


if __name__ == "__main__":
    print(load_lark_tree().pretty())
