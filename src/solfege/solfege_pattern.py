from dataclasses import dataclass
import sys
from typing import ClassVar, Dict, List, Optional, Self, Tuple, Union

from solfege.interval.interval import Interval, octave
from solfege.interval.set.list import IntervalList
from utils.util import assert_typing
from solfege.key.key import nor_flat_nor_sharp


@dataclass(frozen=True)
class SolfegePattern(IntervalList):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """Associate the class, then the name to the pattern"""
    class_to_name_to_pattern: ClassVar[Dict[type, Dict[str, "SolfegePattern"]]] = dict()
    """associate to each class the list of all instances of this class"""
    class_to_patterns: ClassVar[Dict[type, List['SolfegePattern']]] = dict()

    names: List[str]
    notation: Optional[str] = None
    """Whether to record this pattern in the list of patterns."""
    record: bool=True

    """The interval between the signature for this scale and the signature for the major scale with the same key.
    E.g. for minor, use three_flats"""
    interval_for_signature: Interval = nor_flat_nor_sharp

    def __post_init__(self):
        assert isinstance(self.interval_for_signature, Interval)
        super().__post_init__()
        if not self.record:
            return
        cls = self.__class__
        if cls not in self.class_to_patterns:
            self.class_to_patterns[cls] = list()
        self.class_to_patterns[cls].append(self)
        
        if cls not in self.class_to_name_to_pattern:
            self.class_to_name_to_pattern[cls] = dict()
        for name in self.names:
            assert name not in self.class_to_name_to_pattern[cls], f"{name} added twice."
            self.class_to_name_to_pattern[cls][name] = self

    def first_of_the_names(self, for_file= False) -> str:
        """The first of all the names associated to this pattern. Hopefully the most canonical one"""
        name = self.names[0] 
        if for_file:
            return name.replace(" ", "_")
        return name

    def get_names(self):
        """All the names associated to this pattern"""
        return self.names

    @classmethod
    def get_all_instances(cls):
        return cls.class_to_patterns.get(cls, [])

    @classmethod
    def get_from_name(cls, name: str):
        return cls.class_to_name_to_pattern.get(cls, dict()).get(name)


