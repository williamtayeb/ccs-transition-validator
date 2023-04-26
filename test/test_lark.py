from unittest import TestCase
from validator.parser import generate_parser
from lark import GrammarError, ParseError

class TestLark(TestCase):
  def test_grammar_error(self):
    try:
      generate_parser()
    except GrammarError:
      print("Error within the CCS transition validator grammar has been detected.")
    else:
      pass

  def test_parse_error(self):
    try:
      generate_parser()
    except ParseError:
      print("Error while parsing the CCS transition validator grammar.")
    else:
      pass