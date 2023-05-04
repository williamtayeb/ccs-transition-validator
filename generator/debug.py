from generator import output

from generator.operations import ActionPrefixOperation, BinaryOperation, GeneratorOperationConfig, Operations, RelabellingOperation, RestrictionOperation, TransitionOperation
from generator.options import GeneratorOptions

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

  output(generator_options)

