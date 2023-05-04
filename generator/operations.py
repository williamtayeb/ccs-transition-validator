from dataclasses import dataclass

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