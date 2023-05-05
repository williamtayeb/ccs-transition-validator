# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['TestParser::test_debug 1'] = GenericRepr("Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'process_expression'), [Tree(Token('RULE', 'process_expression_element'), [Tree(Token('RULE', 'sum'), [Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'process_expression'), [Tree(Token('RULE', 'process_expression_element'), [Tree(Token('RULE', 'identifier'), [Token('PROCESS_NAME', 'E:49')])])])]), Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'process_expression'), [Tree(Token('RULE', 'process_expression_element'), [Tree(Token('RULE', 'identifier'), [Token('PROCESS_NAME', 'Z')])])])])])])])])])")
