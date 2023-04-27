from hypothesis import strategies as st

import string
import random

def generate_constant():
  constant_part = st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=5)

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

def generate_actions():
  length = random.randint(1, 10)
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

def sum_operator(left, right):
  return f"{left} + {right}"

def parallel_composition(left, right):
  return f"{left} | {right}"

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

constant = generate_constant()
process_name = generate_process_name()

expression = definition(constant, sum_operator(process_name, process_name))

relabelling = relabelling(expression, generate_relabels())
restriction = restriction(relabelling, generate_actions())

transition = transition(relabelling, '*', restriction)
print(transition)

print(constant)
print(process_name)

print(expression)
print(restriction)
