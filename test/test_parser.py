from lib.snapshot.testcase import SnapshotTestCase
from validator.parser import generate_parser

class TestParser(SnapshotTestCase):
  def test_debug(self):
    parser = generate_parser()

    parse_tree = parser.parse("E:49 + Z").pretty()
    self.assert_match_snapshot(parse_tree, "test_debug")