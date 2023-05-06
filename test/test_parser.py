import sys
import hashlib
import json

from colored import fg, bg, attr
from unittest import TestCase
from difflib import unified_diff
from typing import List

from validator.parser import generate_parser

TEMP_SNAPSHOT_DATA_FILE = "test_parser.json"

class SnapshotTestCase(TestCase):
  def __init__(self, methodName="runTest"):
    self.snapshots = []
    super(SnapshotTestCase, self).__init__(methodName)

  def setUp(self):
    self.__load_snapshots()

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

  def __persist_snapshots(self):
    file = open(TEMP_SNAPSHOT_DATA_FILE, 'w')
    json.dump(self.snapshots, file, indent=2)

    file.close()

  def __load_snapshots(self):
    try:
      file = open(TEMP_SNAPSHOT_DATA_FILE, 'r')
      snapshots_data = file.read()

      self.snapshots = json.loads(snapshots_data)
      file.close()
    except:
      pass

  def __snapshot_exists(self, identifier: str):
    for snapshot in self.snapshots:
      if snapshot["identifier"] == identifier:
        return True

    return False

  def generate_identifier(self, value: str):
    identifier = hashlib.sha1(value.encode())
    return identifier.hexdigest()

  def get_snapshot_data(self, identifier: str):
    for snapshot in self.snapshots:
      if snapshot["identifier"] == identifier:
        return snapshot["data"]

  def update_snapshot_data(self, identifier: str, data: str):
    for snapshot in self.snapshots:
      if snapshot["identifier"] == identifier:
        snapshot["data"] = data

  def append_snapshot_data(self, identifier: str, data: str):
    self.snapshots.append({
      "identifier": identifier,
      "data": data
    })

  def assert_match_snapshot(self, value, name = ""):
    identifier = name

    if name == "":
      identifier = self.generate_identifier(value)

    if (not self.__snapshot_exists(identifier)):
      self.append_snapshot_data(identifier, value)
      self.__persist_snapshots()
      return

    snapshot = self.get_snapshot_data(identifier)

    diff_result = self.__diff(snapshot, value)
    diff_list = list(diff_result)

    if len(diff_list) > 0:
      output = self.__diff_output(diff_list, name)
      sys.stdout.writelines(output)

      self.fail("Snapshot test failed.")

class TestParser(SnapshotTestCase):
  def test_debug(self):
    parser = generate_parser()

    parse_tree = parser.parse("E:49 | Z").pretty()
    self.assert_match_snapshot(parse_tree, "test_debug")