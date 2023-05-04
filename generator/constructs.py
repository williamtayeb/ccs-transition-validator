from typing import List
from dataclasses import dataclass

from generator.options import GeneratorOptions
from generator.operations import ActionPrefixOperation, BinaryOperation, GeneratorOperationConfig, Operations, RelabellingOperation, RestrictionOperation, TransitionOperation

@dataclass
class Construct:
  options: GeneratorOptions
  operation_configs: List[GeneratorOperationConfig]

def get_option_list(constructs: List[Construct]):
  options_list = []

  for construct in constructs:
    options_list.append(
      GeneratorOptions(
        construct.options.declaration,
        construct.options.max_depth,
        construct.operation_configs
      )
    )

  return options_list

def get_possible_options() -> List[GeneratorOptions]:
  possible_options = [
    GeneratorOptions(declaration=False, max_depth=1),
    GeneratorOptions(declaration=True, max_depth=1),
    GeneratorOptions(declaration=False, max_depth=2),
    GeneratorOptions(declaration=True, max_depth=2)
  ]

  return possible_options

def get_possible_constructs(options: GeneratorOptions) -> List[Construct]:
  constructs = [
    Construct(options, [
      GeneratorOperationConfig(
        BinaryOperation(Operations.SUM),
        min_operations = 1,
        max_operations = 10
      ),
    ]),

    Construct(options, [
      GeneratorOperationConfig(
        BinaryOperation(Operations.PARALLEL),
        min_operations = 1,
        max_operations = 10
      ),
    ]),

    Construct(options, [
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
    ]),

    Construct(options, [
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
    ]),

    Construct(options, [
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
    ]),

    Construct(options, [
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
    ]),

    Construct(options, [
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
    ])
  ]

  return constructs