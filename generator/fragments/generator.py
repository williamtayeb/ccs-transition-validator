import string, random, strgen
from typing import Tuple

def generate_constant():
  NUM_PARTS = 2
  constant_part = strgen.StringGenerator(r"[a-z]{3}").render_list(NUM_PARTS, unique=True)

  first = constant_part[0].capitalize()
  second = constant_part[1].capitalize()

  include_second = (random.random < 0.5)

  if include_second:
    return f"{first}{second}"

  return first

def generate_process_name():
  char = random.sample(string.ascii_uppercase, 1)[0]
  number = random.randint(0, 100)

  include_number = (random.random < 0.5)

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

def decorate_with_output_actions(element: Tuple[int, str]) -> str:
  """
  Map function for a list of label strings.

  arguments:
    element -- a tuple value that consists of an index value and
    an associated label string.
  """
  index, label = element

  transform_even_index = (random.random() < 0.25)
  is_output_action = index % 2 == 0 if transform_even_index else index % 2 != 0

  return f"&{label}" if is_output_action else label