from typing import Iterable, Tuple
import unittest

from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalListFrozenList
from utils.frozenlist import FrozenList

from solfege.pattern.interval_list_to_pattern import *

second_major = IntervalList.make_relative([(2, 1)])
tone = ChromaticIntervalListPattern.make_relative([2])

@dataclass(frozen=True, eq = True)
class FakePattern(PatternWithIntervalLists["FakeIntervalListToFakePatterns", int]):
    """Test fixture: a minimal `PatternWithIntervalLists` implementation, holding just a relative interval
    list, used to exercise `IntervalListToPattern`/`ChromaticIntervalListToPatterns` registration/lookup."""
    #pragma mark - Recordable
    _key_type: ClassVar[Type] = IntervalList
    """Same as KeyType."""
    #???
    _relative_intervals: IntervalListFrozenList
    """The relative (step-to-step) intervals defining this test pattern's shape."""

    @classmethod
    def _new_record_keeper(cls) -> "FakeIntervalListToFakePatterns":
        """Build this class's `FakeIntervalListToFakePatterns`."""
        return FakeIntervalListToFakePatterns.make()

    def get_interval_list(self) -> IntervalList:
        """`_relative_intervals` turned into an absolute `IntervalList`."""
        return IntervalList.make_relative(self._relative_intervals)

    @classmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:
        """Not needed by these tests; left unimplemented."""
        ...

    #pragma mark - ClassWithEasyness
    def easy_key(self) -> int:
        """Constant: ordering doesn't matter for these tests."""
        return 0

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Coerce `_relative_intervals` into an `IntervalFrozenList` of `Interval`s."""
        def clean_intervals(intervals: Iterable) -> IntervalFrozenList:
            """Coerce each element of `intervals` into an `Interval`, then wrap them in an `IntervalFrozenList`."""
            return IntervalFrozenList([Interval.make_single_argument(interval) for interval in intervals])

        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_relative_intervals", clean_intervals)
        return super()._clean_arguments_for_constructor(args, kwargs)
class FakeChromaticIntervalListToFakePatterns(ChromaticIntervalListToPatterns[FakePattern]):
    """Test fixture: the chromatic-only record keeper companion to `FakeIntervalListToFakePatterns`."""

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = FakePattern
    """Same as RecordedType"""
    _recorded_container_type: ClassVar[Type] = list
    """Same as RecordedContainerType."""

    def is_key_valid(self, key: ChromaticIntervalListPattern) -> bool:
        """Any key is accepted."""
        return True

    @classmethod
    def _new_container(self, key: IntervalList) -> List[FakePattern]:
        """A fresh, empty container for `key`."""
        return list()

class FakeIntervalListToFakePatterns(IntervalListToPattern[FakePattern]):
    """Test fixture: the record keeper backing `FakePattern`, pairing exact and chromatic-only interval keys."""

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = FakePattern
    """Same as RecordedType"""
    _recorded_container_type: ClassVar[Type] = list
    """Same as RecordedContainerType."""
    _chromatic_recorded_container_type: ClassVar[Type] = list
    """The container type used by the chromatic-only companion record keeper (see `make_chromatic_record_keeper`)."""

    def is_key_valid(self, key: ChromaticIntervalListPattern) -> bool:
        """Any key is accepted."""
        return True

    @classmethod
    def _new_container(self, key: IntervalList) -> List[FakePattern]:
        """A fresh, empty container for `key`."""
        return list()

    #pragma mark - IntervalListToPatterns

    @classmethod
    def make_chromatic_record_keeper(self) -> FakeChromaticIntervalListToFakePatterns:
        """Build the companion `FakeChromaticIntervalListToFakePatterns`."""
        return FakeChromaticIntervalListToFakePatterns.make()


fake_pattern_second_major = FakePattern.make([(2,1)])
fake_pattern_third_major = FakePattern.make([(4,2)])

class TestIntervalToPattern(unittest.TestCase):
    def test_add_retrieve(self) -> None:
        """Registering a pattern under an interval list makes it retrievable by exact interval list, by
        chromatic-only interval list, and via the "easiest pattern for this chromatic shape" lookup."""
        itp = FakeIntervalListToFakePatterns.make()
        itp.register(second_major, fake_pattern_second_major)
        self.assertEqual([fake_pattern_second_major], itp.get_from_chromatic_interval_list(tone))
        self.assertEqual([fake_pattern_second_major], itp.get_from_interval_list(second_major))
        self.assertEqual(fake_pattern_second_major, itp.get_easiest_pattern_from_chromatic_interval(tone))
