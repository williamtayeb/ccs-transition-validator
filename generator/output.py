from typing import List

from generator import constructs as gc
from generator.counters import GeneratorCounter
from generator.options import GeneratorOptions
from generator.expressions import generate_ccs_statement

def output_statements(options: GeneratorOptions, len_per_option: int = 10):
  counters = (GeneratorCounter(), GeneratorCounter())

  for x in range(len_per_option):
    print(generate_ccs_statement(options, counters))
    [counter.next_expression() for counter in counters]

  print("\n")

  left_expr_counter, right_expr_counter = counters
  print(f"Left: {left_expr_counter}\n")
  print(f"Right: {right_expr_counter}")

def output_possible_constructs():
  possible_options = gc.get_possible_options()

  options_list = []
  for i, possible_option in enumerate(possible_options):
    possible_constructs = gc.get_possible_constructs(possible_option)
    options_list = gc.get_option_list(possible_constructs)

    output_possible_option_headline(i, len(possible_options), possible_option)

    for j, options in enumerate(options_list):
      output_construct_headline(j, len(options_list), options)
      output_statements(options)

      print("\n\n")

def output_construct_headline(current_index: int, total_constructs: int, options: List[GeneratorOptions]):
  current_construct_num = current_index + 1

  print(f"\t -> [{current_construct_num}/{total_constructs}] Generating...")
  print(options)
  print("\n")

def output_possible_option_headline(
  current_index: int,
  total_options: int,
  option: GeneratorOptions
):
  COLOR_CYAN = '\033[96m'

  current_option_num = current_index + 1
  print_color(COLOR_CYAN, f"[{current_option_num}/{total_options}] Current Options: (Declaration: {option.declaration}, Max Depth: {option.max_depth})")

  print("\n\n")

def print_color(color: str, text: str):
  COLOR_RESET = '\033[0m'

  print(color)
  print(text)
  print(COLOR_RESET)
