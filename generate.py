from enum import StrEnum, auto
from typing import Tuple, List, Optional
from dataclasses import dataclass

import string
import random
import strgen

TAU_ACTION = '*'

class BinaryOperations:
  SUM = '+'
  PARALLEL = '|'

class GeneratorOperations(BinaryOperations):
  RELABELLING = 'RELABELLING'
  RESTRICTION = 'RESTRICTION'

class Operations(GeneratorOperations):
  TRANSITION = 'TRANSITION'

class GeneratorOperation:
  operation_type: Operations

@dataclass
class BinaryOperation(GeneratorOperations):
  operation_type: BinaryOperations
  group: bool

@dataclass
class RelabellingOperation(GeneratorOperations):
  operation_type = GeneratorOperations.RELABELLING
  min_labels: int = 1
  max_labels: int = 3

@dataclass
class RestrictionOperation(GeneratorOperations):
  operation_type = GeneratorOperations.RESTRICTION
  min_actions: int = 1
  max_actions: int = 3

@dataclass
class TransitionOperation(GeneratorOperations):
  operation_type: Operations = Operations.TRANSITION
  tau_action_only: bool = False

class GeneratorOptions:
  def __init__(
    self,
    process_only: bool = False,
    declaration: bool = False,
    max_depth: int = 3,
    operations: Optional[List[GeneratorOperations | TransitionOperation]] = []
  ):
    self.process_only = process_only
    self.declaration = declaration
    self.max_depth = max_depth
    self.operations = operations

    if operations is None or len(operations) == 0:
      self.operations = [
        BinaryOperation(BinaryOperations.SUM, group=False),
        BinaryOperation(BinaryOperations.PARALLEL, group=False),
        RelabellingOperation(),
        RestrictionOperation(),
        TransitionOperation(tau_action_only=False)
      ]

  def contains_operation(self, operation_type: Operations) -> bool:
    for current_operation in self.operations:
      if (current_operation.operation_type == operation_type):
        return True
    
    return False

  def get_operation(self, operation_type: Operations) -> (
    GeneratorOperation |
    BinaryOperation |
    RelabellingOperation |
    RestrictionOperation |
    TransitionOperation
  ):
    for current_operation in self.operations:
      if (current_operation.operation_type == operation_type):
        return current_operation
    
    raise IndexError(f"Operation type '{operation_type}' not found.")
    

def generate_constant():
  constant_part = strgen.StringGenerator(r"[a-z]{3}").render_list(2, unique=True)

  first = constant_part[0].capitalize()
  second = constant_part[1].capitalize()

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

def declaration(left, right):
  return f"{left} ::= {right}"

def binary_operator(operation: BinaryOperations, left, right, group=False):
  expression = f"{left} {operation} {right}"

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

def generate_declaration(expression):
  identifier_is_constant = random_boolean()

  if identifier_is_constant:
    identifier = generate_constant()
  else:
    identifier = generate_process_name()
  
  return declaration(identifier, expression)

def generate_ccs_expressions(options: GeneratorOptions = GeneratorOptions()):
  include_transition = options.contains_operation(Operations.TRANSITION) and random_boolean()
  expression = generate_expression(options)

  if include_transition:
    right = generate_expression(options)
    action = generate_action()

    if options.get_operation(Operations.TRANSITION).tau_action_only:
      action = TAU_ACTION

    expression = transition(expression, action, right)
  else:
    include_declaration = options.declaration and random_boolean()

    if include_declaration:
      expression = generate_declaration(expression)

  return expression

def generate_expression(options: GeneratorOptions, current_depth=0):
  include_action_prefix = random_boolean()
  include_binary_operation = (not include_action_prefix) or random_boolean()

  include_relabelling = options.contains_operation(Operations.RELABELLING) and (random.random() < 0.25)
  include_restriction = options.contains_operation(Operations.RESTRICTION) and (random.random() < 0.25)

  if current_depth >= options.max_depth:
    include_binary_operation = False

  expression = generate_process_name()

  if include_action_prefix:
    if include_binary_operation:
      expression = generate_binary_operation(options, current_depth, group=True)

    labels = generate_labels(max_len=3)

    actions = map(decorate_with_output_actions, enumerate(labels))
    actions_output = ".".join(actions)

    expression = f"{actions_output}.{expression}"
  else:
    if include_binary_operation:
      group = random_boolean()

      if include_relabelling or include_restriction:
        group = True

      expression = generate_binary_operation(options, current_depth, group)

  if include_relabelling:
    relabels = generate_relabels()
    expression = relabelling(expression, relabels)

  if include_restriction:
    actions = generate_labels()
    expression = restriction(expression, actions)

  return expression

def generate_binary_operation(options: GeneratorOptions, current_depth, group=False):
  current_depth += 1
  operation = random.choice([BinaryOperations.SUM, BinaryOperations.PARALLEL])

  left = generate_expression(options, current_depth)
  right = generate_expression(options, current_depth)

  return binary_operator(operation, left, right, group)


generator_options = GeneratorOptions(max_depth=1)

for x in range(20):
  print(generate_ccs_expressions(generator_options))