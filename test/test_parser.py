import sys

from colored import fg, bg, attr
from unittest import TestCase
from difflib import unified_diff
from typing import List

from validator.parser import generate_parser

class SnapshotTestCase(TestCase):
  def __diff_parse_trees(self, parse_tree1, parse_tree2) -> List[str]:
    parse_tree_list1 = parse_tree1.pretty().split('\n')
    parse_tree_list2 = parse_tree2.pretty().split('\n')

    result = unified_diff(parse_tree_list1, parse_tree_list2)
    return result

  def __replace_tab_with_spaces(self, value: str) -> str:
    return value.replace('\t', ' ' * 4)

  def __diff_output_title(self, snapshot_name: str) -> List[str]:
    output = []

    output.append(f"{bg(15)}\n")
    output.append(attr(0))

    output.append(f"{bg(15)}\n")
    output.append(f"{fg(1)}   FAIL")
    output.append(f"{fg(0)} Snapshot name: `{snapshot_name}`")
    output.append(attr(0))

    output.append(f"{bg(15)}\n")
    output.append(attr(0))

    return output

  def __diff_output_substract(self, value):
    diff_output = []

    diff_output.append(f"{bg(225)}\n")
    diff_output.append(f"{fg(89)}{value}")
    diff_output.append(f"{attr(0)}")

    return diff_output

  def __diff_output_add(self, value):
    diff_output = []

    diff_output.append(f"{bg(193)}\n")
    diff_output.append(f"{fg(29)}{value}")
    diff_output.append(f"{attr(0)}")

    return diff_output

  def __diff_output_unchanged(self, value):
    diff_output = []

    diff_output.append(f"{bg(15)}\n")
    diff_output.append(f"{fg(240)}{value}")
    diff_output.append(f"{attr(0)}")

    return diff_output
  
  def __diff_output(
    self,
    diff_list,
    snapshot_name,
    ignore_diff_result_lines = 3
  ) -> str:
    output = []
    output.extend(self.__diff_output_title(snapshot_name))

    for i, line in enumerate(diff_list):
      empty_line = len(line) == 0

      if (i < ignore_diff_result_lines) or empty_line:
        continue

      first_character = line[0]

      if first_character == '-':
        output_line = self.__replace_tab_with_spaces(line)
        output.extend(self.__diff_output_substract(output_line))
      elif first_character == '+':
        output_line = self.__replace_tab_with_spaces(line)
        output.extend(self.__diff_output_add(output_line))
      else:
        output.extend(self.__diff_output_unchanged(line))

    output.append(f"{attr(0)}\n")
    return output

  def assert_match_snapshot(self, value, name = ""):
    parser = generate_parser()

    parse_tree1 = parser.parse("E:49 + Z")
    parse_tree2 = parser.parse("E:49 | Z")

    diff_result = self.__diff_parse_trees(parse_tree1, parse_tree2)
    diff_list = list(diff_result)

    if len(diff_list) > 0:
      output = self.__diff_output(diff_list, "renders correctly 1")
      sys.stdout.writelines(output)

      self.fail("Snapshot test failed.")

class TestParser(SnapshotTestCase):
  def test_debug(self):
    parser = generate_parser()

    parse_tree = parser.parse("E:49 + Z")
    self.assert_match_snapshot(parse_tree)

    self.fail()