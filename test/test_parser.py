import sys

from colored import fg, bg, attr
from unittest import TestCase
from difflib import unified_diff

from validator.parser import generate_parser

class SnapshotTestCase(TestCase):
  def assert_match_snapshot(self, value, name = ""):
    parser = generate_parser()

    parse_tree1 = parser.parse("E:49 + Z")
    parse_tree2 = parser.parse("E:49 | Z")

    output1 = parse_tree1.pretty().split('\n')
    output2 = parse_tree2.pretty().split('\n')

    output1 = [f"{s}" for s in output1]
    output2 = [f"{s}" for s in output2]

    result = unified_diff(output1, output2)
    result2 = []

    result2.append(f"{bg(15)}\n")
    result2.append(f"{attr(0)}")

    result2.append(f"{bg(15)}\n")
    result2.append(f"{fg(1)}   FAIL")
    result2.append(f"{fg(0)} Snapshot name: `renders correctly 1`")
    result2.append(f"{attr(0)}")

    result2.append(f"{bg(15)}\n")
    result2.append(f"{attr(0)}")

    for i, x in enumerate(result):
      if i < 3:
        continue

      if len(x) > 0:
        if x[0] == '-':
          x2 = x.replace('\t', ' ' * 4)

          result2.append(f"{bg(225)}\n")
          result2.append(f"{fg(89)}{x2}")
          result2.append(f"{attr(0)}")
        elif x[0] == '+':
          x2 = x.replace('\t', ' ' * 4)

          result2.append(f"{bg(150)}\n")
          result2.append(f"{fg(29)}{x2}")
          result2.append(f"{attr(0)}")
        else:
          result2.append(f"{bg(15)}\n")
          result2.append(f"{fg(240)}{x}")
          result2.append(f"{attr(0)}")

    sys.stdout.writelines(result2)
    print(f"{attr(0)}\n")

class TestParser(SnapshotTestCase):
  def test_debug(self):
    parser = generate_parser()

    parse_tree = parser.parse("E:49 + Z")
    self.assert_match_snapshot(parse_tree)
    self.fail()