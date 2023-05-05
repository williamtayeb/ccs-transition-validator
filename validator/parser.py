import os
from lark import Lark

# Path to the grammar file located relative to this module.
DEFAULT_GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'grammar.lark')

def generate_parser(
  grammar_file_path: str = DEFAULT_GRAMMAR_FILE,
  grammar_start: str = 'start'
) -> Lark:
  with open(grammar_file_path) as grammar:
    parser = Lark(grammar, parser='lalr', start=grammar_start)

  return parser