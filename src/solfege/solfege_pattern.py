import unittest
from typing import List, Union


class SolfegePattern:
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    names: List[str]
    """Associate the class, then the name to the pattern"""
    class_to_name_to_pattern = dict()
    """associate to each class the list of all instances of this class"""
    class_to_patterns = dict()

    def __init__(self, names: Union[str, List[str]], record=True):
        """"""
        if isinstance(names, str):
            names = [names]
        self.names = names
        cls = self.__class__
        if cls not in self.class_to_name_to_pattern:
            self.class_to_name_to_pattern[cls] = dict()
            assert (cls not in self.class_to_patterns)
            self.class_to_patterns[cls] = []
        for name in names:
            self.class_to_name_to_pattern[cls][name] = self

        if record:
            self.class_to_patterns[cls].append(self)

    def get_the_first_of_the_name(self) -> str:
        """The first of all the names associated to this pattern. Hopefully the most canonical one"""
        return self.names[0]

    def get_names(self):
        """All the names associated to this pattern"""
        return self.names

    @classmethod
    def get_all_instances(cls):
        return cls.class_to_patterns.get(cls, [])

    @classmethod
    def get_from_name(cls, name: str):
        return cls.class_to_name_to_pattern.get(cls, dict()).get(name)


class TestSolfegePattern(unittest.TestCase):
    class PatternEmpty(SolfegePattern):
        pass

    class PatternDeux(SolfegePattern):
        pass

    instance_1 = PatternDeux(names=["1a", "1b"])
    instance_2 = PatternDeux(names=["2a"])

    def test_empty_set(self):
        self.assertEquals(self.PatternEmpty.get_all_instances(), [])
        self.assertIsNone(self.PatternEmpty.get_from_name("foo"))

    def test_pattern_deux_not_in_1(self):
        self.assertEquals(self.PatternEmpty.get_all_instances(), [])
        self.assertEquals(self.PatternEmpty.get_from_name("1a"), None)

    def test_pattern_deux(self):
        self.assertEquals(self.PatternDeux.get_all_instances(), [self.instance_1, self.instance_2])
        self.assertEquals(self.PatternDeux.get_from_name("1a"), self.instance_1)

    def test_name(self):
        self.assertEquals(self.instance_1.get_names(), ["1a", "1b"])
        self.assertEquals(self.instance_1.get_the_first_of_the_name(), "1a")
