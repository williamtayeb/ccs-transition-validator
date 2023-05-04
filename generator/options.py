import random
from typing import List, Optional

from generator.operations import Operations, GeneratorOperationConfig
from generator.counters import GeneratorCounter

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

      must_include_operation = self.__must_include_operation(operation_config, num_operations)
      can_include_operation = self.__can_include_operation(operation_config, num_operations)

      include_operation = can_include_operation and (probability >= random.random())

      if counter.current_depth == 0:
        include_operation = must_include_operation or include_operation

    return include_operation

  def __must_include_operation(
    self,
    operation_config: GeneratorOperationConfig,
    num_operations: int
  ) -> bool:
    return operation_config.min_operations > num_operations

  def __can_include_operation(
    self,
    operation_config: GeneratorOperationConfig,
    num_operations: int
  ) -> bool:
    return operation_config.max_operations > num_operations
