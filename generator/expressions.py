import random
from typing import Tuple, List

from fragments import generator as fg
from fragments import output

from constants import TAU_ACTION

from options import GeneratorOptions
from counters import GeneratorCounter
from operations import Operations, BinaryOperation

def generate_ccs_statement(
  options: GeneratorOptions = GeneratorOptions(),
  counters: Tuple[GeneratorCounter] = (GeneratorCounter(), GeneratorCounter())
):
  """
  arguments:
    counters -- a tuple of generator counters for left and right expressions
    respectively.
  """
  left_expr_counter, right_expr_counter = counters

  include_transition = options.is_operation_available(
    Operations.TRANSITION,
    left_expr_counter,
    probability = 0.5
  )

  expression = generate_expression(options, left_expr_counter)

  if include_transition:
    right = generate_expression(options, right_expr_counter)
    action = fg.generate_action()

    transition_config = options.get_operation_config(Operations.TRANSITION).operation

    if transition_config.tau_action_only:
      action = TAU_ACTION

    expression = output.transition(expression, action, right)
    left_expr_counter.increment(Operations.TRANSITION)
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

  expression = fg.generate_process_name()

  if include_action_prefix:
    if include_binary_operation:
      expression = generate_binary_operation(options, counter, group=True)

    labels = fg.generate_labels(max_len=3)

    actions = map(fg.decorate_with_output_actions, enumerate(labels))
    actions_output = ".".join(actions)

    expression = f"{actions_output}.{expression}"

    counter.increment(Operations.ACTION_PREFIX)
  else:
    if include_binary_operation:
      group = (random.random() < 0.5)

      if include_relabelling or include_restriction:
        group = True

      expression = generate_binary_operation(options, counter, group)

  if include_relabelling:
    operation = options.get_operation_config(Operations.RELABELLING).operation

    relabels = fg.generate_relabels(operation.min_labels, operation.max_labels)
    expression = output.relabelling(expression, relabels)

    counter.increment(Operations.RELABELLING)

  if include_restriction:
    operation = options.get_operation_config(Operations.RESTRICTION).operation

    actions = fg.generate_labels(min_len=operation.min_actions, max_len=operation.max_actions)
    expression = output.restriction(expression, actions)

    counter.increment(Operations.RESTRICTION)

  return expression

def generate_binary_operation(
  options: GeneratorOptions,
  counter: GeneratorCounter,
  group = False
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

  return output.binary_operator(
    operation.operation_type,
    left,
    right,
    group = (operation.group or group)
  )

def generate_declaration(expression):
  identifier_is_constant = (random.random() < 0.5)

  if identifier_is_constant:
    identifier = fg.generate_constant()
  else:
    identifier = ()
  
  return output.declaration(identifier, expression)
