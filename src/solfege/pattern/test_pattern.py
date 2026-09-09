from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type
import unittest

from solfege.pattern.solfege_pattern import SolfegePattern
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.frozenlist import FrozenList, StrFrozenList
from utils.recording.record_keeper import RecordKeeper
from utils.recording.singleton_container import SingletonContainer


@dataclass(frozen=True, unsafe_hash=True)
class PatternEmpty(SolfegePattern):
    """Test fixture: a `SolfegePattern` subclass whose instances are never actually recorded
    (`_clean_arguments_for_constructor` forces `record=False`), used to check the "no instances" case."""
    name_to_pattern: ClassVar[Dict[str, "PatternEmpty"]] = dict()
    """Maps each registered name to its `PatternEmpty` instance (see `PatternWithName.name_to_pattern`)."""
    all_patterns: ClassVar[List['PatternEmpty']] = list()
    """Every registered `PatternEmpty` instance, in creation order (see `PatternWithName.all_patterns`)."""

    @classmethod
    def _new_record_keeper(cls):
        """Build this class's `RecordKeeperForPatternEmpty`."""
        return RecordKeeperForPatternEmpty.make()

    @classmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:
        """Not needed by these tests; left unimplemented."""
        ...
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Force `record=False` so `PatternEmpty` instances are never registered."""
        kwargs["record"] = False
        return super()._clean_arguments_for_constructor(args, kwargs)

class RecordKeeperForPatternEmpty(RecordKeeper[IntervalList, PatternEmpty, SingletonContainer[PatternEmpty]]):
    """Test fixture: the record keeper backing `PatternEmpty`."""
    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = PatternEmpty
    """Same as RecordedType"""
    _key_type: ClassVar[Type] = IntervalList
    """Same as KeyType"""
    _recorded_container_type: ClassVar[Type] = List
    """Same as RecordedContainerType"""

    def is_key_valid(self, key: IntervalList):
        """Any key is accepted."""
        return True

    def _new_container(self, key: IntervalList) -> List[IntervalList]:
        """A fresh, empty container for `key`."""
        return list()

PatternEmpty._record_keeper_type = RecordKeeperForPatternEmpty

@dataclass(frozen=True, unsafe_hash=True)
class PatternDeux(SolfegePattern):
    """Test fixture: a `SolfegePattern` subclass that does get recorded (unlike `PatternEmpty`), used to check
    name-based lookup and registration."""
    name_to_pattern: ClassVar[Dict[str, "PatternDeux"]] = dict()
    """Maps each registered name to its `PatternDeux` instance (see `PatternWithName.name_to_pattern`)."""
    all_patterns: ClassVar[List['PatternDeux']] = list()
    """Every registered `PatternDeux` instance, in creation order (see `PatternWithName.all_patterns`)."""
    il: IntervalList
    """The interval list this test pattern exposes via `get_interval_list()`."""


    @classmethod
    def _new_record_keeper(cls):
        """Build this class's `RecordKeeperForPatternDeux`."""
        return RecordKeeperForPatternDeux.make()

    def get_interval_list(self):
        """This test pattern's interval list, i.e. `il`."""
        return self.il

    @classmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:
        """Not needed by these tests; left unimplemented."""
        ...
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Coerce `il` into an `IntervalList` via `IntervalList.make`."""
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "il", IntervalList.make)
        return super()._clean_arguments_for_constructor(args, kwargs)

class RecordKeeperForPatternDeux(RecordKeeper[IntervalList, PatternDeux, SingletonContainer[PatternDeux]]):
    """Test fixture: the record keeper backing `PatternDeux`."""

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = PatternDeux
    """Same as RecordedType"""
    _key_type: ClassVar[Type] = IntervalList
    """Same as KeyType"""
    _recorded_container_type: ClassVar[Type] = List
    """Same as RecordedContainerType"""


    def is_key_valid(self, key: IntervalList):
        """Any key is accepted."""
        return True

    def _new_container(self, key: IntervalList) -> List[IntervalList]:
        """A fresh, empty container for `key`."""
        return list()

PatternDeux._record_keeper_type = RecordKeeperForPatternDeux

class TestSolfegePattern(unittest.TestCase):

    instance_1 = PatternDeux.make(il=[(0,0)], names=["1a", "1b"])
    instance_2 = PatternDeux.make(il=[(0, 0)], names=["2a"])

    def test_empty_set(self):
        """A `PatternEmpty` instance (record=False) never gets registered: no instances, no name lookup."""
        self.assertEqual(PatternEmpty.get_all_instances(), [])
        self.assertIsNone(PatternEmpty.get_from_name("foo"))

    def test_pattern_deux_not_in_1(self):
        """Registration is per-class: a name registered on `PatternDeux` is not visible from `PatternEmpty`."""
        self.assertEqual(PatternEmpty.get_all_instances(), [])
        self.assertEqual(PatternEmpty.get_from_name("1a"), None)

    def test_pattern_deux(self):
        """`PatternDeux` instances are recorded in creation order and retrievable by any of their names."""
        self.assertEqual(PatternDeux.get_all_instances(), [self.instance_1, self.instance_2])
        self.assertEqual(PatternDeux.get_from_name("1a"), self.instance_1)

    def test_name(self):
        """`get_names()` returns every alias; `first_of_the_names()` returns the canonical (first) one."""
        self.assertEqual(self.instance_1.get_names(), StrFrozenList(["1a", "1b"]))
        self.assertEqual(self.instance_1.first_of_the_names(), "1a")
