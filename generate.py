from enum import Enum
from typing import Tuple

import string
import random
import strgen

TAU_ACTION = '*'

class BinaryOperations(Enum):
  SUM = '+'
  PARALLEL_COMPOSITION = '|'

def generate_constant():
  constant_part = strgen.StringGenerator("[a-z]{1,5}").render()

  first = constant_part.example().capitalize()
  second = constant_part.example().capitalize()

  include_second = random_boolean()

  if include_second:
    return f"{first}{second}"

  return first

def generate_process_name():
  char = random.sample(string.ascii_uppercase, 1)[0]
  number = random.randint(0, 100)

  include_number = random_boolean()

  if include_number:
    return f"{char}:{number}"

  return char

def generate_action():
  action = random.choice(string.ascii_lowercase + '*')
  return action

def generate_labels(min_len=1, max_len=5):
  length = random.randint(min_len, max_len)
  actions = random.sample(string.ascii_lowercase, k=length)

  return actions

def generate_relabels():
  relabels = {}
  length = random.randint(1, 10)

  previous_actions = random.sample(string.ascii_lowercase, k=length)
  new_actions = random.sample(string.ascii_lowercase, k=length)

  for i, new_action in enumerate(new_actions):
    relabels[new_action] = previous_actions[i]

  return relabels

def random_boolean():
  return random.choice([True, False])

def definition(left, right):
  return f"{left} ::= {right}"

def binary_operator(operation: BinaryOperations, left, right, group=False):
  expression = f"{left} {operation.value} {right}"

  if group:
    return f"({expression})"

  return expression

def relabelling(expr, relabels: dict):
  relabel_expressions = [f"{key}/{relabels[key]}" for key in relabels]
  relabel_expressions_str = ", ".join(relabel_expressions)

  return f"{expr}[{relabel_expressions_str}]"

def restriction(expr, actions: list):
  actions_str = ", ".join(actions)
  return expr + "\{" + actions_str + "}"

def action_prefix(action, expr): 
  return f"{action}.{expr}"

def transition(left, action, right):
  return f"{left} ->({ action }) {right}"

def decorate_with_output_actions(element: Tuple[int, str]) -> str:
  """
  Map function for a list of label strings.

  arguments:
    element -- a tuple value that consists of an index value and
    an associated label string.
  """
  index, label = element

  transform_even_index = random.random() < 0.25
  is_output_action = index % 2 == 0 if transform_even_index else index % 2 != 0

  return f"&{label}" if is_output_action else label

def generate_definition(expression):
  identifier_is_constant = random_boolean()

  if identifier_is_constant:
    identifier = generate_constant()
  else:
    identifier = generate_process_name()
  
  return definition(identifier, expression)

def generate_ccs_expressions():
  include_transition = random_boolean()
  expression = generate_expression()

  if include_transition:
    right = generate_expression()
    action = generate_action()
    expression = transition(expression, action, right)
  else:
    include_definition = random_boolean()

    if include_definition:
      expression = generate_definition(expression)

  return expression

def generate_expression(current_depth=0, max_depth=1):
  include_action_prefix = random_boolean()
  include_binary_operation = (not include_action_prefix) or random_boolean()

  include_relabelling = random.random() < 0.25
  include_restriction = random.random() < 0.25

  if current_depth >= max_depth:
    include_binary_operation = False

  expression = generate_process_name()

  if include_action_prefix:
    if include_binary_operation:
      expression = generate_binary_operation(current_depth, max_depth, group=True)

    labels = generate_labels(max_len=3)

    actions = map(decorate_with_output_actions, enumerate(labels))
    actions_output = ".".join(actions)

    expression = f"{actions_output}.{expression}"
  else:
    if include_binary_operation:
      group = random_boolean()

      if include_relabelling or include_restriction:
        group = True

      expression = generate_binary_operation(current_depth, max_depth, group)

  if include_relabelling:
    relabels = generate_relabels()
    expression = relabelling(expression, relabels)

  if include_restriction:
    actions = generate_labels()
    expression = restriction(expression, actions)

  return expression

def generate_binary_operation(current_depth, max_depth, group=False):
  current_depth += 1
  operation = random.choice([BinaryOperations.SUM, BinaryOperations.PARALLEL_COMPOSITION])

  left = generate_expression(current_depth=current_depth, max_depth=max_depth)
  right = generate_expression(current_depth=current_depth, max_depth=max_depth)

  return binary_operator(operation, left, right, group)

for x in range(20):
  print(generate_ccs_expressions())