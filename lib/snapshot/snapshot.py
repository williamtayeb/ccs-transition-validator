import hashlib
import json

from json import JSONEncoder
from typing import List

class SnapshotEntry:
  def __init__(self, identifier, value):
    self.identifier = identifier
    self.value = value

  @staticmethod
  def Decoder(entryDict):
    return SnapshotEntry(entryDict["identifier"], entryDict["value"])

class SnapshotEntryEncoder(JSONEncoder):
  def default(self, entryObject: SnapshotEntry):
    return entryObject.__dict__

class Snapshots:
  def __init__(self, file_path):
    self.snapshots: List[SnapshotEntry] = []
    self.file_path = file_path

  def load(self):
    with open(self.file_path, 'r') as file:
      snapshots_data = file.read()

    self.snapshots = json.loads(snapshots_data, object_hook=SnapshotEntry.Decoder)

  def persist(self):
    with open(self.file_path, 'w') as file:
      json.dump(self.snapshots, file, indent=2, cls=SnapshotEntryEncoder)
  
  def add_entry(self, identifier: str, value: str):
    entry = SnapshotEntry(identifier, value)
    self.snapshots.append(entry)

  def update_entry(self, identifier: str, value: str):
    for entry in self.snapshots:
      if entry.identifier == identifier:
        entry.value = value

  def get_value(self, identifier: str):
    for entry in self.snapshots:
      if entry.identifier == identifier:
        return entry.value
    
    raise IndexError(f"Invalid snapshot identifier '{identifier}'")

  def generate_identifier(self, value: str):
    identifier = hashlib.sha1(value.encode())
    return identifier.hexdigest()

  def entry_exists(self, identifier: str):
    for entry in self.snapshots:
      if entry.identifier == identifier:
        return True
    
    return False