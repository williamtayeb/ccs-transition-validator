from sys import argv
from validator import parser

# from lark import Lark, ParseError, GrammarError
# import inspect

def p(src):
  print(parser.parse(src).pretty())

if __name__ == "__main__":
  src = argv[1]
  p(src)

# except ParseError as parse_error:
  # print("Error while parsing grammar")
# except GrammarError as grammar_error:
  # print("Grammar error")
# except Exception as e:
  # print(e.__class__)
  # print(e.__class__.__base__)
  # print(inspect.getmro(type(e)))