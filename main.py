from lark import Lark

grammar = open("grammar.lark")
parser = Lark(grammar, parser='lalr', start='definition')