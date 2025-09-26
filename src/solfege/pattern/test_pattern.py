from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type
import unittest

from solfege.pattern.solfege_pattern import SolfegePattern
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from utils.frozenlist import FrozenList, StrFrozenList
from utils.recordable import RecordKeeper


@dataclass(frozen=True, unsafe_hash=True)
class PatternEmpty(SolfegePattern):
    """See SoflegePattern"""
    name_to_pattern: ClassVar[Dict[str, "PatternEmpty"]] = dict()
    all_patterns: ClassVar[List['PatternEmpty']] = list()

    @classmethod
    def _new_record_keeper(cls):
        return RecordKeeperForPatternEmpty.make()

    @classmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:...
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        kwargs["record"] = False
        return super()._clean_arguments_for_constructor(args, kwargs)

class RecordKeeperForPatternEmpty(RecordKeeper[IntervalListPattern, PatternEmpty, List[PatternEmpty]]):
    #pragma mark - RecordKeeper

    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = PatternEmpty
    """Same as KeyType"""
    _key_type: ClassVar[Type] = IntervalListPattern
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = List

    def is_key_valid(self, key: IntervalListPattern):
        return True
    
    def _new_container(self, key: IntervalListPattern) -> List[IntervalListPattern]:
        return list()

PatternEmpty._record_keeper_type = RecordKeeperForPatternEmpty

@dataclass(frozen=True, unsafe_hash=True)
class PatternDeux(SolfegePattern):
    """See SoflegePattern"""
    name_to_pattern: ClassVar[Dict[str, "PatternDeux"]] = dict()
    all_patterns: ClassVar[List['PatternDeux']] = list()


    @classmethod
    def _new_record_keeper(cls):
        return RecordKeeperForPatternDeux.make()

    @classmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:...
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        return super()._clean_arguments_for_constructor(args, kwargs)

class RecordKeeperForPatternDeux(RecordKeeper[IntervalListPattern, PatternDeux, List[PatternDeux]]):

    #pragma mark - RecordKeeper
    
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = PatternDeux
    """Same as KeyType"""
    _key_type: ClassVar[Type] = IntervalListPattern
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = List


    def is_key_valid(self, key: IntervalListPattern):
        return True
    
    def _new_container(self, key: IntervalListPattern) -> List[IntervalListPattern]:
        return list()

PatternDeux._record_keeper_type = RecordKeeperForPatternDeux

class TestSolfegePattern(unittest.TestCase):

    instance_1 = PatternDeux.make_relative([], names=["1a", "1b"])
    instance_2 = PatternDeux.make_relative([], names=["2a"])

    def test_empty_set(self):
        self.assertEqual(PatternEmpty.get_all_instances(), [])
        self.assertIsNone(PatternEmpty.get_from_name("foo"))

    def test_pattern_deux_not_in_1(self):
        self.assertEqual(PatternEmpty.get_all_instances(), [])
        self.assertEqual(PatternEmpty.get_from_name("1a"), None)

    def test_pattern_deux(self):
        self.assertEqual(PatternDeux.get_all_instances(), [self.instance_1, self.instance_2])
        self.assertEqual(PatternDeux.get_from_name("1a"), self.instance_1)

    def test_name(self):
        self.assertEqual(self.instance_1.get_names(), StrFrozenList(["1a", "1b"]))
        self.assertEqual(self.instance_1.first_of_the_names(), "1a")
