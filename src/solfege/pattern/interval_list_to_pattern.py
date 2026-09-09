
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns, PatternType
from solfege.pattern.pattern_with_interval_lists import PatternWithIntervalLists
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.recording.record_keeper import RecordKeeper
from utils.recording.recorded_container import ChromaticRecordedContainerType, RecordedContainerType
from utils.recording.singleton_container import SingletonContainer
from utils.util import assert_dict_typing, assert_optional_typing, assert_typing, assert_iterable_typing


@dataclass(frozen=True)
class IntervalListToPattern(RecordKeeper[IntervalList, PatternType, SingletonContainer[PatternType]], ABC, Generic[PatternType]):
    """Associate a Interval list to a list of PatternType stored in RecordedContainerType.

    Registering in this record keeper also register to the associated record keeper with interval keys.
    """


    chromatic: ChromaticIntervalListToPatterns[PatternType]
    """Same but for chromatic interval as key"""

    #Must be implemented by subclasses
    _key_type: ClassVar[Type] = IntervalList
    """Same as KeyType"""
    _recorded_type: ClassVar[Type]
    """Same as RecordedType"""

    _recorded_container_type: ClassVar[Type] = SingletonContainer
    """Same as RecordedContainerType."""

    @classmethod
    @abstractmethod
    def make_chromatic_record_keeper(self) -> ChromaticIntervalListToPatterns[PatternType]:
        """Build the `ChromaticIntervalListToPatterns` companion record keeper used for `chromatic`."""
        ...
    #public

    def get_easiest_pattern_from_chromatic_interval(self, chromatic_interval_list: ChromaticIntervalListPattern):
        """The single pattern registered under `chromatic_interval_list`'s chromatic-only key, or None."""
        return self.chromatic.get_pattern_from_chromatic_interval(chromatic_interval_list)

    def register(self, key: IntervalList, recorded: PatternType):
        """Register `recorded` under `key` here, and also under `key`'s chromatic-only equivalent in
        `self.chromatic`, keeping both record keepers in sync."""
        super().register(key, recorded)
        self.chromatic.register(key.get_chromatic_interval_list(), recorded)

    def get_from_interval_list(self, key: IntervalList) -> Optional[RecordedContainerType]:
        """The container of pattern(s) registered under the exact interval list `key`, or None."""
        container = self.get_recorded_container(key)
        assert_optional_typing(container, self._recorded_container_type)
        return container

    def get_from_chromatic_interval_list(self, key: ChromaticIntervalListPattern) -> Optional[ChromaticRecordedContainerType]:
        """The container of pattern(s) registered under the chromatic-only interval list `key`, or None."""
        assert_typing(key, ChromaticIntervalListPattern)
        container = self.chromatic.get_recorded_container(key)
        assert_optional_typing(container, SingletonContainer)
        return container

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `chromatic` to a freshly built companion record keeper (`make_chromatic_record_keeper()`)."""
        default = super()._default_arguments_for_constructor(args, kwargs)
        chromatic = cls.make_chromatic_record_keeper()
        assert_typing(chromatic, ChromaticIntervalListToPatterns)
        default["chromatic"] = chromatic
        return default

    def __post_init__(self):
        """Validate `chromatic`'s type before chaining to the rest of construction."""
        assert_typing(self.chromatic, ChromaticIntervalListToPatterns)
        super().__post_init__()


PatternWithIntervalLists._record_keeper_type = IntervalListToPattern