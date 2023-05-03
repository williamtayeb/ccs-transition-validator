from typing import Tuple, List, Optional
from dataclasses import dataclass

import string
import random
import strgen

TAU_ACTION = '*'

# Refactor this shit
class BinaryOperations:
  SUM = '+'
  PARALLEL = '|'

class GeneratorOperations(BinaryOperations):
  RELABELLING = 'RELABELLING'
  RESTRICTION = 'RESTRICTION'

class Operations(GeneratorOperations):
  ACTION_PREFIX = 'ACTION_PREFIX'
  TRANSITION = 'TRANSITION'

@dataclass
class GeneratorOperation:
  operation_type: Operations

@dataclass
class BinaryOperation(GeneratorOperations):
  operation_type: BinaryOperations
  group: bool = False

@dataclass
class ActionPrefixOperation(GeneratorOperations):
  operation_type = Operations.ACTION_PREFIX

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

@dataclass
class GeneratorOperationConfig:
  operation: GeneratorOperation
  min_operations: int = 1,
  max_operations: int = 5

@dataclass
class OperationCounter:
  operation_type: Operations
  count: int = 0
  has_been_incremented: bool = False

class GeneratorCounter:
  def __init__(self):
    self.current_depth = 0
    self.operation_counters = [
      OperationCounter(Operations.ACTION_PREFIX),
      OperationCounter(Operations.SUM),
      OperationCounter(Operations.PARALLEL),
      OperationCounter(Operations.RELABELLING),
      OperationCounter(Operations.RESTRICTION),
      OperationCounter(Operations.TRANSITION),
    ]

  def increment(self, operation_type: Operations):
    operation_counter = self.get_operation_counter(operation_type)

    if (not operation_counter.has_been_incremented):
      operation_counter.count += 1
      operation_counter.has_been_incremented = True

  def get_operation_counter(self, operation_type: Operations) -> OperationCounter:
    for operation_counter in self.operation_counters:
      if operation_counter.operation_type == operation_type:
        return operation_counter

  def get_count(self, operation_type: Operations) -> int:
    return self.get_operation_counter(operation_type).count

  def next_expression(self):
    self.current_depth = 0

    for operation_counter in self.operation_counters:
      operation_counter.has_been_incremented = False
  
  def __str__(self):
    output = []
    output.append(f"Current depth: {self.current_depth}")

    for counter in self.operation_counters:
      output.append(f"({counter.operation_type}, {counter.count}, {counter.has_been_incremented})")
    
    return ", ".join(output[0:])

class GeneratorOptions:
  def __init__(
    self,
    declaration: bool = False,
    max_depth: int = 3,
    operation_configs: Optional[List[GeneratorOperationConfig]] = []
  ):
    self.declaration = declaration
    self.max_depth = max_depth
    self.operation_configs = operation_configs
  
  def __str__(self):
    title = f"Declaration: {self.declaration}, Max_Depth: {self.max_depth}"

    config_output = []
    for config in self.operation_configs:
      config_output.append(config.operation.operation_type)

    config_output_str = ", ".join(config_output)
    return f"{title}, " + f"({config_output_str})"

  def contains_operation_type(self, operation_type: Operations) -> bool:
    for operation_config in self.operation_configs:
      if (operation_config.operation.operation_type == operation_type):
        return True
    
    return False

  def get_operation_config(self, operation_type: Operations) -> GeneratorOperationConfig:
    for operation_config in self.operation_configs:
      if (operation_config.operation.operation_type == operation_type):
        return operation_config
    
    raise IndexError(f"Operation type '{operation_type}' not found.")

  def contains_binary_operations(self) -> bool:
    return (
      self.contains_operation_type(Operations.SUM) or
      self.contains_operation_type(Operations.PARALLEL)
    )

  def get_available_binary_operations(self, counter: GeneratorCounter):
    binary_operations = []

    for operation_config in self.operation_configs:
      operation_type = operation_config.operation.operation_type

      is_binary_operation = (
        (operation_type == Operations.SUM) or 
        (operation_type == Operations.PARALLEL)
      )

      if is_binary_operation:
        include_binary_operation = self.is_operation_available(
          operation_type,
          counter,
        )

        if include_binary_operation:
          binary_operations.append(operation_config.operation)
    
    return binary_operations

  def is_operation_available(
    self,
    operation_type: Operations,
    counter: GeneratorCounter,
    probability: float = 1.0
  ) -> bool:
    include_operation = False
    options_has_operation = self.contains_operation_type(operation_type)

    if options_has_operation:
      operation_config = self.get_operation_config(operation_type)

      num_operations = counter.get_count(operation_type)

      must_include_operation = self.must_include_operation(operation_config, num_operations)
      can_include_operation = self.can_include_operation(operation_config, num_operations)

      include_operation = can_include_operation and (probability >= random.random())

      if counter.current_depth == 0:
        include_operation = must_include_operation or include_operation

    return include_operation

  def must_include_operation(
    self,
    operation_config: GeneratorOperationConfig,
    num_operations: int
  ) -> bool:
    return operation_config.min_operations > num_operations

  def can_include_operation(
    self,
    operation_config: GeneratorOperationConfig,
    num_operations: int
  ) -> bool:
    return operation_config.max_operations > num_operations

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

def generate_relabels(min_len=1, max_len=10):
  relabels = {}
  length = random.randint(min_len, max_len)

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
  identifier_is_constant = (random.random() < 0.5)

  if identifier_is_constant:
    identifier = generate_constant()
  else:
    identifier = generate_process_name()
  
  return declaration(identifier, expression)

def generate_ccs_expressions(
  options: GeneratorOptions = GeneratorOptions(),
  counter: GeneratorCounter = GeneratorCounter()
):
  include_transition = options.is_operation_available(
    Operations.TRANSITION,
    counter,
    probability = 0.5
  )

  expression = generate_expression(options, counter)

  if include_transition:
    right = generate_expression(options, counter)
    action = generate_action()

    transition_config = options.get_operation_config(Operations.TRANSITION).operation

    if transition_config.tau_action_only:
      action = TAU_ACTION

    expression = transition(expression, action, right)
    counter.increment(Operations.TRANSITION)
  else:
    include_declaration = options.declaration and (random.random() < 0.5)

    if include_declaration:
      expression = generate_declaration(expression)
      # counter.increment(Operations.DECLARATION)

  return expression

def generate_expression(options: GeneratorOptions, counter: GeneratorCounter):
  include_action_prefix = options.is_operation_available(
    Operations.ACTION_PREFIX,
    counter,
    probability = 0.10
  )

  include_binary_operation = (
    options.is_operation_available(Operations.SUM, counter) or
    options.is_operation_available(
      Operations.PARALLEL,
      counter
    )
  )

  include_relabelling = options.is_operation_available(
    Operations.RELABELLING,
    counter,
    probability = 0.10
  )

  include_restriction = options.is_operation_available(
    Operations.RESTRICTION,
    counter,
    probability = 0.10
  )

  if counter.current_depth >= options.max_depth:
    include_binary_operation = False

  expression = generate_process_name()

  if include_action_prefix:
    if include_binary_operation:
      expression = generate_binary_operation(options, counter, group=True)

    labels = generate_labels(max_len=3)

    actions = map(decorate_with_output_actions, enumerate(labels))
    actions_output = ".".join(actions)

    expression = f"{actions_output}.{expression}"

    counter.increment(Operations.ACTION_PREFIX)
  else:
    if include_binary_operation:
      group = random_boolean()

      if include_relabelling or include_restriction:
        group = True

      expression = generate_binary_operation(options, counter, group)

  if include_relabelling:
    operation = options.get_operation_config(Operations.RELABELLING).operation

    relabels = generate_relabels(operation.min_labels, operation.max_labels)
    expression = relabelling(expression, relabels)

    counter.increment(Operations.RELABELLING)

  if include_restriction:
    operation = options.get_operation_config(Operations.RESTRICTION).operation

    actions = generate_labels(min_len=operation.min_actions, max_len=operation.max_actions)
    expression = restriction(expression, actions)

    counter.increment(Operations.RESTRICTION)

  return expression

def generate_binary_operation(
  options: GeneratorOptions,
  counter: GeneratorCounter,
  group=False
):
  counter.current_depth += 1

  binary_operations: List[BinaryOperation] = options.get_available_binary_operations(counter)
  operation = random.choice(binary_operations)

  if operation.operation_type == Operations.SUM:
    counter.increment(Operations.SUM)

  if operation.operation_type == Operations.PARALLEL:
    counter.increment(Operations.PARALLEL)

  left = generate_expression(options, counter)
  right = generate_expression(options, counter)

  return binary_operator(
    operation.operation_type,
    left,
    right,
    group = (operation.group or group)
  )


def debug():
  operation_configs = [
    GeneratorOperationConfig(
      BinaryOperation(Operations.SUM),
      min_operations = 5,
      max_operations = 10
    ),

    GeneratorOperationConfig(
      BinaryOperation(Operations.PARALLEL),
      min_operations = 5,
      max_operations = 10
    ),

    GeneratorOperationConfig(
      ActionPrefixOperation(),
      min_operations = 5,
      max_operations = 10
    ),

    GeneratorOperationConfig(
      RelabellingOperation(),
      min_operations = 5,
      max_operations = 10
    ),

    GeneratorOperationConfig(
      RestrictionOperation(),
      min_operations = 5,
      max_operations = 10
    ),

    GeneratorOperationConfig(
      TransitionOperation(),
      min_operations = 5,
      max_operations = 10
    ),
  ]

  generator_options = GeneratorOptions(
    declaration=False,
    max_depth=1,
    operation_configs=operation_configs
  )

  counter = GeneratorCounter()
  len_per_option = 10

  for x in range(len_per_option):
    print(generate_ccs_expressions(generator_options, counter))
    counter.next_expression()


def generate(constructs: List[List[GeneratorOperationConfig]], len_per_option = 10):
  possible_generator_options = [
    GeneratorOptions(declaration=False, max_depth=1),
    GeneratorOptions(declaration=True, max_depth=1),
    GeneratorOptions(declaration=False, max_depth=2),
    GeneratorOptions(declaration=True, max_depth=2),
  ]

  for i, possible_option in enumerate(possible_generator_options):
    options_list = []

    for construct in constructs:
      options_list.append(
        GeneratorOptions(
          possible_option.declaration,
          possible_option.max_depth,
          operation_configs=construct
        )
      )

    print(f"\033[96m[{i+1}/{len(possible_generator_options)}] Construct: (Declaration: {possible_option.declaration}, Max Depth: {possible_option.max_depth})\033[0m")
    print("\n\n")

    for j, options in enumerate(options_list):
      print(f"\t -> [{j+1}/{len(options_list)}] Generating...")
      print(options)
      print("\n")

      counter = GeneratorCounter()

      for x in range(len_per_option):
        print(generate_ccs_expressions(options, counter))
        counter.next_expression()
      
      print("\n")
      print(counter)

      print("\n\n")

def get_possible_generator_operations_constructs():
  operation_constructs = [
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 1,
        max_operations = 10
      ),
    ],
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 1,
        max_operations = 10
      ),
    ],
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 1,
        max_operations = 5
      ),
    ],
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        ActionPrefixOperation(),
        min_operations = 1,
        max_operations = 5
      ),
    ],
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        ActionPrefixOperation(),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        RelabellingOperation(),
        min_operations = 1,
        max_operations = 5
      ),
    ],
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        ActionPrefixOperation(),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        RelabellingOperation(),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        RestrictionOperation(),
        min_operations = 1,
        max_operations = 5
      ),
    ],
    [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 5,
        max_operations = 10
      ),

      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 5,
        max_operations = 10
      ),

      GeneratorOperationConfig(
        ActionPrefixOperation(),
        min_operations = 1,
        max_operations = 5
      ),

      GeneratorOperationConfig(
        RelabellingOperation(),
        min_operations = 10,
        max_operations = 20
      ),

      GeneratorOperationConfig(
        RestrictionOperation(),
        min_operations = 10,
        max_operations = 20
      ),

      GeneratorOperationConfig(
        TransitionOperation(),
        min_operations = 10,
        max_operations = 20
      ),
    ]
  ]

  return operation_constructs

options_list = []

possible_constructs = get_possible_generator_operations_constructs()
constructs_len = len(possible_constructs)

#generate(options_list[0:constructs_len])
generate(possible_constructs)
# debug()