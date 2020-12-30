GRAMMAR = open('grammer.ebnf').read()

CODE = open('../../code.mds').read()

print(CODE)

if __name__ == '__main__':
    import pprint
    import json
    from tatsu import parse
    from tatsu.util import asjson

    ast = parse(GRAMMAR, CODE)
    print('# PPRINT')
    pprint.pprint(ast, indent=4, width=20)
    print()

    print('# JSON')
    print(json.dumps(asjson(ast), indent=4))
    print()
