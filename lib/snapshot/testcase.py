import sys

from colored import fg, bg, attr
from unittest import TestCase
from difflib import unified_diff
from typing import List

from lib.snapshot.snapshot import Snapshots

TEMP_SNAPSHOT_DATA_FILE = "test_parser.json"

class SnapshotTestCase(TestCase):
  def __init__(self, methodName="runTest"):
    self.snapshots = Snapshots(TEMP_SNAPSHOT_DATA_FILE)
    super(SnapshotTestCase, self).__init__(methodName)

  def setUp(self):
    try:
      self.snapshots.load()
    except:
      pass

  def __diff(self, a, b) -> List[str]:
    a_lines = a.split('\n')
    b_lines = b.split('\n')

    result = unified_diff(a_lines, b_lines)
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
    identifier = name

    if name == "":
      identifier = self.snapshots.generate_identifier(value)

    snapshot_exists = self.snapshots.entry_exists(identifier)

    if (not snapshot_exists):
      self.snapshots.add_entry(identifier, value)
      self.snapshots.persist()
      return

    snapshot_value = self.snapshots.get_value(identifier)

    diff_result = self.__diff(snapshot_value, value)
    diff_list = list(diff_result)

    if len(diff_list) > 0:
      output = self.__diff_output(diff_list, name)
      sys.stdout.writelines(output)

      self.fail("Snapshot test failed.")