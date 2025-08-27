from dataclasses import dataclass
import unittest

from solfege.solfege_pattern import SolfegePattern

class TestSolfegePattern(unittest.TestCase):
    @dataclass(frozen=True)
    class PatternEmpty(SolfegePattern):
        pass

    @dataclass(frozen=True)
    class PatternDeux(SolfegePattern):
        pass

    instance_1 = PatternDeux.make_relative([], ["1a", "1b"])
    instance_2 = PatternDeux.make_relative([], ["2a"])

    def test_empty_set(self):
        self.assertEqual(self.PatternEmpty.get_all_instances(), [])
        self.assertIsNone(self.PatternEmpty.get_from_name("foo"))

    def test_pattern_deux_not_in_1(self):
        self.assertEqual(self.PatternEmpty.get_all_instances(), [])
        self.assertEqual(self.PatternEmpty.get_from_name("1a"), None)

    def test_pattern_deux(self):
        self.assertEqual(self.PatternDeux.get_all_instances(), [self.instance_1, self.instance_2])
        self.assertEqual(self.PatternDeux.get_from_name("1a"), self.instance_1)

    def test_name(self):
        self.assertEqual(self.instance_1.get_names(), ["1a", "1b"])
        self.assertEqual(self.instance_1.first_of_the_names(), "1a")
