from lex.lexer import Lexer
from par.paraser_and_res import Parser


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    for ty, va in enumerate(tokens):
        print(va, end='')
        print('\t', end='')
        if ty % 7 == 0:
            print()
    print()
    # 生成 AST
    parser = Parser(tokens)
    ast = parser.parse()
    # return tokens, error
    return ast.node, ast.error
