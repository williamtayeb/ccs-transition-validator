from json import JSONEncoder

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
