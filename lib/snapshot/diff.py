from difflib import unified_diff
from typing import List
from colored import attr, fg, bg

class SnapshotDiff:
  def __init__(self, identifier: str):
    self.identifier = identifier
    self.result = []

  def compare(self, a, b) -> List[str]:
    a_lines = a.split('\n')
    b_lines = b.split('\n')

    diff_result = unified_diff(a_lines, b_lines)
    self.result = list(diff_result)

    return self.result
  
  def output(
    self,
    ignore_diff_result_lines = 3
  ) -> str:
    output = []
    output.extend(self.__output_title(self.identifier))

    for i, line in enumerate(self.result):
      empty_line = len(line) == 0

      if (i < ignore_diff_result_lines) or empty_line:
        continue

      first_character = line[0]

      if first_character == '-':
        output_line = self.__replace_tab_with_spaces(line)
        output.extend(self.__output_substract(output_line))
      elif first_character == '+':
        output_line = self.__replace_tab_with_spaces(line)
        output.extend(self.__output_add(output_line))
      else:
        output.extend(self.__output_unchanged(line))

    output.append(self.__reset_output_colors())
    return output

  def __output_title(self, name: str) -> List[str]:
    output = []

    output.append(f"{bg(15)}\n")
    output.append(attr(0))

    output.append(f"{bg(15)}\n")
    output.append(f"{fg(1)}   FAIL")
    output.append(f"{fg(0)} Snapshot name: `{name}`")
    output.append(attr(0))

    output.append(f"{bg(15)}\n")
    output.append(attr(0))

    return output

  def __output_substract(self, value: str):
    diff_output = []

    diff_output.append(f"{bg(225)}\n")
    diff_output.append(f"{fg(89)}{value}")
    diff_output.append(f"{attr(0)}")

    return diff_output

  def __output_add(self, value: str):
    diff_output = []

    diff_output.append(f"{bg(193)}\n")
    diff_output.append(f"{fg(29)}{value}")
    diff_output.append(f"{attr(0)}")

    return diff_output

  def __output_unchanged(self, value: str):
    diff_output = []

    diff_output.append(f"{bg(15)}\n")
    diff_output.append(f"{fg(240)}{value}")
    diff_output.append(f"{attr(0)}")

    return diff_output

  def __replace_tab_with_spaces(self, value: str) -> str:
    return value.replace('\t', ' ' * 4)
  
  def __reset_output_colors(self):
    return f"{attr(0)}\n"