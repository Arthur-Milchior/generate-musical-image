from dataclasses import dataclass, field
from itertools import pairwise
from typing import Callable, ClassVar, Dict, FrozenSet, List, Optional, Tuple, Type, Union

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.interval_list import IntervalList
from solfege.pattern.solfege_pattern import SolfegePattern
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_all_same_class, assert_iterable_typing, assert_typing

def chord_to_arpeggio_name(name: str) -> str:
    """Turn a chord's name into the name of its arpeggio: replaces a trailing "chord"/"triad" with "arpeggio",
    or appends " arpeggio" if neither word is present. Used by `ChordPattern.to_arpeggio_pattern()`."""
    if "chord" in name:
        return name.replace("chord", "arpeggio")
    if "triad" in name:
        return name.replace("triad", "arpeggio")
    else:
        return f"{name} arpeggio"

@dataclass(frozen=True, unsafe_hash=True)
class ChordPattern(SolfegePattern, DataClassWithDefaultArgument):
    """A pattern describing a chord.
    
    Ordered according to the name."""

    """See SolfegePattern"""
    name_to_pattern: ClassVar[Dict[str, "ChordPattern"]] = dict()
    """Maps each registered name to its `ChordPattern` instance (see `PatternWithName.name_to_pattern`)."""
    all_patterns: ClassVar[List['ChordPattern']] = list()
    """Every registered `ChordPattern` instance, in creation order (see `PatternWithName.all_patterns`)."""

    _record_keeper: ClassVar[List]
    """This class's lazily-created `RecordKeeper` (see `Recordable._record_keeper`); redeclared here only for
    the `ClassVar` type annotation."""

    _full_interval_list: IntervalList
    """The absolute intervals (from the root/tonic) of every note of this chord, root position, e.g.
    `[(4, 2), (7, 4)]` for a major triad. Unison (the root itself) is implicit and not included."""

    optional_fifth: bool
    """Whether the 5th is optional"""

    extension_intervals: IntervalFrozenList
    """Which of `_full_interval_list`'s intervals represent a compound extension (a 9th/11th/13th stored
    octave-reduced, see multi_octave_patterns.md) that must sound above every non-extension tone once this
    pattern is turned into a real, physical voicing (e.g. on a fretted instrument). Empty for chords that have
    no such extension -- most chords. See extension_chromatic_values()."""


    @classmethod
    def _new_record_keeper(cls) -> "IntervalListToChordPattern":
        """Build this class's `IntervalListToChordPattern` record keeper."""
        from solfege.pattern.chord.interval_list_to_chord_pattern import IntervalListToChordPattern
        return IntervalListToChordPattern.make()

    def _index_of_fifth(self) -> int:
        """The index, within `_full_interval_list`, of the note at diatonic index 4 (the fifth). Requires
        `optional_fifth`, and asserts there is exactly one such note."""
        index = None
        for i in range(len(self._full_interval_list)):
            if self._full_interval_list.absolute_intervals()[i]._diatonic.value == 4:
                assert index is None
                index = i
        assert index is not None
        return index

    def intervals_with_all_notes(self) -> IntervalList:
        """This chord's full interval list, i.e. `_full_interval_list` (the fifth always included, even if
        `optional_fifth`)."""
        return self._full_interval_list

    def extension_chromatic_values(self) -> FrozenSet[int]:
        """The base-octave chromatic pitch classes (0-11, relative to the tonic) of this chord's extension
        tones -- see `extension_intervals`. Empty if this chord has none."""
        return frozenset(interval.get_chromatic().in_base_octave().value for interval in self.extension_intervals)

    def intervals_without_fifth(self) -> IntervalList:
        """`_full_interval_list` with the fifth (diatonic index 4) dropped. Requires `optional_fifth`."""
        assert self.optional_fifth
        index_of_fifth = self._index_of_fifth()
        full_intervals = self.intervals_with_all_notes().absolute_intervals()
        absolute_without_fifth = full_intervals[:index_of_fifth] + full_intervals[index_of_fifth+1:]
        return IntervalList.make_absolute(absolute_intervals=absolute_without_fifth)

    def to_arpeggio_pattern(self) -> "ScalePattern":
        """This chord played as a one-octave ascending scale (arpeggio) instead of stacked simultaneously:
        a `ScalePattern` built from the same absolute intervals plus a closing octave, carrying over this
        chord's names (via `chord_to_arpeggio_name`), notation, signature interval, source and description."""
        from solfege.pattern.scale.scale_pattern import ScalePattern
        absolute_intervals = self._full_interval_list.absolute_intervals() + [Interval.one_octave()]
        return ScalePattern.make(_absolute_intervals=absolute_intervals,
                            names=[chord_to_arpeggio_name(name) for name in self.names],
                            notation = self.notation,
                            interval_for_signature=self.interval_for_signature, record=True, increasing=True, _is_chord_pattern=True,
                            source=self.source,
                            description=f"The {self.first_of_the_names()} chord ({self.description}) played as a "
                                         "one-octave scale (arpeggio) instead of stacked simultaneously.")

    def interval_list_of_inversion(self, inversion_number: int, omit_fifth:bool=False) -> Optional[IntervalList]:
        """The absolute interval list of this chord's `inversion_number`-th inversion (0 = root position),
        i.e. the same notes recomputed relative to the note that becomes the new bass, wrapped increasing.
        If `omit_fifth` (requires `optional_fifth`), also drops the fifth from that inversion -- returning
        None if the fifth would end up as the new bass note itself (it can't be dropped from an inversion
        where it *is* the lowest note)."""
        assert 0<= inversion_number<len(self._full_interval_list)
        new_lower: Interval = self._full_interval_list.absolute_intervals()[inversion_number]
        absolute_intervals = [(interval - new_lower).add_octave(1 if index < inversion_number else 0) for index, interval in enumerate(self._full_interval_list.absolute_intervals())]
        absolute_intervals = absolute_intervals[inversion_number:] + absolute_intervals[:inversion_number]
        if omit_fifth:
            assert self.optional_fifth
            new_index_of_fifth = (self._index_of_fifth() - inversion_number) % len(absolute_intervals)
            if new_index_of_fifth == 0: # don't remove the lowest note of the inversion
                return None
            absolute_intervals.pop(new_index_of_fifth)
        inversion_interval_list = IntervalList.make_absolute(absolute_intervals, increasing=True)
        return inversion_interval_list

    def inversion(self, inversion_number: int, record: bool = False) -> "InversionPattern":
        """Build (and, if `record`, register) the `InversionPattern` for this chord's `inversion_number`-th
        inversion."""
        from solfege.pattern.inversion.inversion_pattern import InversionPattern
        new_lower: Interval = self._full_interval_list.absolute_intervals()[inversion_number]
        return InversionPattern.make(inversion=inversion_number, base=self, record=record, tonic_minus_lowest_note=new_lower)

    def inversions(self, record: bool = False) -> List["InversionPattern"]:
        """Every `InversionPattern` of this chord (one per note as potential bass), in inversion-number order.
        Called automatically from `__post_init__` with `record=self.record`."""
        l = []
        for inversion_number in range(len(self._full_interval_list.absolute_intervals())):
            l.append(self.inversion(inversion_number, record=record))
        return l

    def __lt__(self, other: "ChordPattern") -> bool:
        """Order chords alphabetically by their canonical (first) name."""
        return self.first_of_the_names() < other.first_of_the_names()

    def get_interval_lists(self) -> List[IntervalList]:
        """The interval list(s) this chord registers under: the full interval list, plus (if `optional_fifth`)
        the fifth-omitted variant."""
        il = self.intervals_with_all_notes()
        assert_typing(il, IntervalList)
        l = [il]
        if self.optional_fifth:
            il = self.intervals_without_fifth()
            assert_typing(il, IntervalList)
            l.append(il)
        return l
    
    # pragma mark - PatternWithIntervalLists
    
    @classmethod
    def _get_instantiation_type(cls) -> Type["Chord"]:
        """`Chord` is the `AbstractPairInstantiation` used to anchor a `ChordPattern` to a concrete note."""
        from solfege.pattern_instantiation.chord.chord import Chord
        return Chord


    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Dict:
        """Default `optional_fifth` to False, `_is_chord_pattern` to True, and `extension_intervals` to empty."""
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["optional_fifth"] = False
        default_dict["_is_chord_pattern"] = True
        default_dict["extension_intervals"] = IntervalFrozenList()
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Coerce `_full_interval_list` into an `IntervalList` (via `IntervalList.make_absolute` if it isn't
        one already) and `extension_intervals` into an `IntervalFrozenList`; pass `optional_fifth` through
        positional-to-keyword normalization."""
        def clean_full_interval_list(l: Union[IntervalList, List]) -> IntervalList:
            """Pass through an existing `IntervalList` unchanged, else build one via `IntervalList.make_absolute`."""
            if isinstance(l, IntervalList):
                return l
            else:
                return IntervalList.make_absolute(l)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_full_interval_list", clean_full_interval_list)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "optional_fifth")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "extension_intervals", IntervalFrozenList)
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self) -> None:
        """Validate `_full_interval_list`/`extension_intervals`'s types and that every `extension_intervals`
        entry is actually one of `_full_interval_list`'s intervals, then chain to the rest of construction and,
        if `record`, build and register every inversion of this chord (see `inversions()`)."""
        assert_typing(self._full_interval_list, IntervalList)
        assert_typing(self.extension_intervals, IntervalFrozenList)
        assert_iterable_typing(self.extension_intervals, Interval)
        for extension_interval in self.extension_intervals:
            assert extension_interval in self._full_interval_list.absolute_intervals(), \
                f"{extension_interval} marked as an extension of {self.names} but not in its _full_interval_list"
        super().__post_init__()
        if not self.record:
            return

        self.inversions(record=self.record)