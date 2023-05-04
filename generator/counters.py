from typing import List

from dataclasses import dataclass
from operations import Operations

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