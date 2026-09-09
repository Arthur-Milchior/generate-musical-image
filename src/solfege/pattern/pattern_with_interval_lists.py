from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import sys
from typing import ClassVar, Dict, Generic, List, Optional, Self, Type, TypeVar, Union

from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness, KeyType
from utils.recording.record_keeper import RecordKeeperType
from utils.recording.recordable import Recordable
from utils.util import assert_iterable_typing, assert_typing


@dataclass(frozen=True)
class PatternWithIntervalLists(Recordable[IntervalList, RecordKeeperType], ClassWithEasyness[KeyType], DataClassWithDefaultArgument, ABC, Generic[RecordKeeperType, KeyType]):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """Associate a interval list to its patterns"""

    """Whether to record this pattern in the list of patterns."""

    #Must be implemented by subtype

    @classmethod
    @abstractmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:
        """The `AbstractPairInstantiation` subclass used to anchor this pattern to a concrete note
        (e.g. `Chord` for `ChordPattern`, `Scale` for `ScalePattern`)."""
        ...

    def get_interval_lists(self) -> List[IntervalList]:
        """The interval list(s) this pattern registers itself under. Most patterns expose exactly one (via
        `get_interval_list()`); a subclass may override this to expose several (e.g. a chord with an optional
        fifth also registers its fifth-omitted interval list)."""
        il = self.get_interval_list()
        assert_typing(il, IntervalList)
        return [il]

    # public

    def chromatic_interval_lists(self) -> ChromaticIntervalListPattern:
        """`get_interval_lists()`, converted to their chromatic-only (no diatonic spelling) equivalents."""
        return [interval.get_chromatic_interval_list() for interval in self.get_interval_lists()]

    def get_chromatic_instantiation(self, lowest_chromatic_note: ChromaticNote) -> "AbstractChromaticInstantiation[Self]":
        """Anchor this pattern to a concrete chromatic (no diatonic spelling) lowest note."""
        return self._get_instantiation_type.related_chromatic_type(lowest_chromatic_note)

    def get_instantiation(self, lowest_note: Note) -> "AbstractPairInstantiation[Self]":
        """Anchor this pattern to a concrete lowest note, producing the instance/chord/scale it represents."""
        return self._get_instantiation_type(lowest_note)

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `record` to True (register into the record keeper on construction)."""
        defaut_dict = super()._default_arguments_for_constructor(args, kwargs)
        defaut_dict["record"] = True
        return defaut_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Pass `record` through positional-to-keyword normalization."""
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "record")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        """Validate `record`'s type, then, if True, register this pattern's interval list(s) into the
        record keeper (`_associate_keys_to_self()`)."""
        assert_typing(self.record, bool)
        super().__post_init__()
        if self.record:
            self._associate_keys_to_self()
    

PatternType = TypeVar("PatternType", bound=PatternWithIntervalLists)