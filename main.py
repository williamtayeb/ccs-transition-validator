from sys import argv
from lark import Lark

grammar = open("grammar.lark")
parser = Lark(grammar, parser='lalr', start='definition')

def p(src):
  print(parser.parse(src).pretty())

if __name__ == "__main__":
  src = argv[1]
  p(src)