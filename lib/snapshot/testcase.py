import sys

from unittest import TestCase
from lib.snapshot.diff import SnapshotDiff
from lib.snapshot.snapshot import Snapshots

TEMP_SNAPSHOT_DATA_FILE = "test_parser.json"

class SnapshotTestCase(TestCase):
  def __init__(self, methodName="runTest"):
    self.snapshots = Snapshots(TEMP_SNAPSHOT_DATA_FILE)
    super(SnapshotTestCase, self).__init__(methodName)

  def setUp(self):
    try:
      self.snapshots.load()
    except:
      pass

  def assert_match_snapshot(self, value, name = ""):
    identifier = name

    if name == "":
      identifier = self.snapshots.generate_identifier(value)

    snapshot_exists = self.snapshots.entry_exists(identifier)

    if (not snapshot_exists):
      self.snapshots.add_entry(identifier, value)
      self.snapshots.persist()
      return

    snapshot_value = self.snapshots.get_value(identifier)

    diff = SnapshotDiff(identifier)
    diff.compare(snapshot_value, value)

    if len(diff.result) > 0:
      output = diff.output()
      sys.stdout.writelines(output)

      self.fail("Snapshot test failed.")