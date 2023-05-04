from operations import BinaryOperations

def declaration(left, right):
  return f"{left} ::= {right}"

def action_prefix(action, expr): 
  return f"{action}.{expr}"

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

def transition(left, action, right):
  return f"{left} ->({ action }) {right}"