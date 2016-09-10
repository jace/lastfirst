import unittest
from lastfirst.parsers import tokenize

sample_data = [
    ("First Last", [('t', "First"), ('s', " "), ('t', "Last")]),
    ("F.L.", [('t', "F"), ('s', "."), ('t', "L"), ('s', ".")]),
    ("I.First Last", [('t', "I"), ('s', "."), ('t', "First"), ('s', " "), ('t', "Last")]),
    ("I. First Last", [('t', "I"), ('s', "."), ('s', " "), ('t', "First"), ('s', " "), ('t', "Last")]),
    ("First..Last", [('t', "First"), ('s', "."), ('t', "Last")]),  # Second period is dropped
    ]


class TestParsersTokenizer(unittest.TestCase):
    def test_tokenize(self):
        for input, output in sample_data:
            self.assertEqual(tokenize(input), output)
