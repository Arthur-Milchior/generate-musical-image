

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, Generic, Iterable, List, Tuple, Type, TypeVar
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.pattern_with_interval_lists import PatternWithIntervalLists
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import IntervalList
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness
from utils.util import assert_iterable_typing, assert_optional_typing, assert_typing

class InversionPatternsGetter(ClassWithEasyness, ABC):
    """A protocol simply offeritng to access a IdenticalInversionPattern."""
    @abstractmethod
    def get_inversion_pattern(self) -> "InversionPatterns":
        """The `InversionPattern` (or equivalent grouping) associated with this object."""
        ...

InversionPatternsGetterType = TypeVar("IdenticalInversionPatternGetterType", bound=InversionPatternsGetter)

@dataclass(frozen=True)
class InversionPattern(PatternWithIntervalLists["IntervalListToInversionPattern", Tuple[int, int]],
                       DataClassWithDefaultArgument):
    """A chord voiced starting from a note other than its root: the same set of pitch classes as a `ChordPattern`
    (`base`), but recomputed relative to whichever note becomes the new lowest note. Built and registered
    automatically by `ChordPattern.inversions()`; not normally constructed directly."""

    #pragma mark - Recordable
    _key_type: ClassVar[Type] = IntervalList
    """Same as KeyType."""

    # public
    """Order is considering not inversion first. Then with fifth. Then base."""

    inversion: int
    """0 if the pattern is in base position, 1 for first inversion and so on"""
    base: ChordPattern
    """The pattern without inversion. Equal to self if `inversion` is 0."""
    fifth_omitted: bool
    """Whether the fifth is omitted in this pattern."""

    tonic_minus_lowest_note: Interval
    """For a scale whose lowest note is n, you get the position of the tonic with n+tonic_minus_lowest_note."""

    def get_tonic_minus_lowest_note(self):
        """For a scale whose lowest note is n, you get the position of the tonic with n+tonic_minus_lowest_note."""
        return self.tonic_minus_lowest_note

    def get_tonic(self, lowest_note: Note):
        """Returns the tonic assuming that the pattern start with this `lowest_note`."""
        assert_typing(lowest_note, Note)
        return lowest_note - self.tonic_minus_lowest_note

    def get_chromatic_tonic(self, lowest_note: ChromaticNote) -> ChromaticNote:
        """Same as `get_tonic`, but working purely in chromatic terms (e.g. for a fretted-instrument voicing,
        which has no diatonic identity of its own)."""
        assert_typing(lowest_note, ChromaticNote)
        return lowest_note - self.tonic_minus_lowest_note.get_chromatic()

    def voicing_respects_extensions(self, tonic: ChromaticNote, physical_notes: Iterable[ChromaticNote]) -> bool:
        """Whether a concrete, physical voicing of this inversion -- `physical_notes`, distinct real notes with
        `tonic` as this chord's real root (see `get_chromatic_tonic`) -- respects `base.extension_intervals`
        (see ChordPattern.extension_intervals and multi_octave_patterns.md): every note playing an extension
        tone must sound above every note playing a non-extension tone. True (no constraint to check) if `base`
        has no marked extension, or if `physical_notes` doesn't actually contain both kinds."""
        assert_typing(tonic, ChromaticNote)
        assert_iterable_typing(physical_notes, ChromaticNote)
        extension_classes = self.base.extension_chromatic_values()
        if not extension_classes:
            return True
        extension_physical = []
        base_physical = []
        for note in physical_notes:
            pitch_class = (note - tonic).in_base_octave().value
            if pitch_class in extension_classes:
                extension_physical.append(note)
            else:
                base_physical.append(note)
        if not extension_physical or not base_physical:
            return True
        return max(base_physical) < min(extension_physical)

    @classmethod
    def _new_record_keeper(cls):
        """Build this class's `IntervalListToInversionPattern` record keeper."""
        from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
        return IntervalListToInversionPattern.make()

    def names(self):
        """`base`'s names, each suffixed with this inversion's ordinal (e.g. " first inversion"), or left
        unsuffixed for root position (inversion 0)."""
        names = []
        for chord_name in self.base.names:
            if self.inversion == 0:
                suffix = ""
            elif self.inversion == 1:
                suffix = " first inversion"
            elif self.inversion == 2:
                suffix = " second inversion"
            elif self.inversion == 3:
                suffix = " third inversion"
            else:
                assert self.inversion < 10
                suffix = f" {self.inversion}th inversion"
            names.append(f"""{chord_name}{suffix}""")
        return names

    def notation(self):
        """`base`'s notation, suffixed with "/<inversion>" (e.g. "/1") unless this is root position."""
        suffix = "" if self.inversion == 0 else f"/{self.inversion}"
        return f"""{self.base.notation}{suffix}"""

    def __lt__(self, other: "InversionPattern"):
        """Order by inversion number first, then chords with the fifth before those without it, then by `base`."""
        return (self.inversion, not self.fifth_omitted, self.base) < (other.inversion, not other.fifth_omitted, other.base)

    def intervals_with_all_notes(self):
        """`base`'s full interval list (fifth included), recomputed relative to this inversion's bass note."""
        return self.base.interval_list_of_inversion(self.inversion)

    def intervals_without_fifth(self):
        """Same as `intervals_with_all_notes()` but with the fifth dropped, or None if `base.optional_fifth`
        is False (the fifth can't be omitted) or this inversion's bass note is itself the fifth."""
        if self.base.optional_fifth is False:
            return None
        return self.base.interval_list_of_inversion(self.inversion, omit_fifth=True)

    @classmethod
    def _get_instantiation_type(cls) -> Type["Inversion"]:
        """`InversionInstantiation` is the `AbstractPairInstantiation` used to anchor an `InversionPattern` to
        a concrete note."""
        from solfege.pattern_instantiation.inversion.inversion_instantiation import InversionInstantiation
        return InversionInstantiation

    #pragma mark - PatternWithIntervalLists
    def get_interval_lists(self) -> List[IntervalList]:
        """The interval list(s) this inversion registers under: the full-notes list, plus (if the fifth can be
        omitted here) the fifth-omitted variant."""
        iv = self.intervals_with_all_notes()
        assert_typing(iv, IntervalList)
        iv_without_5 = self.intervals_without_fifth()
        assert_optional_typing(iv_without_5, IntervalList)
        return [iv] if iv_without_5 is None else [iv, iv_without_5]

    #pragma mark - ClassWithEasyness
    def easy_key(self) -> Tuple[int, int]:
        """No inversion is easier. If two patterns have the same inversion, the easiest one have the easiest pattern. ."""
        return (self.inversion, self.base.easy_key())

    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        """Validate that `inversion` is a valid index into `base`'s notes, and that every interval list this
        inversion registers under starts at unison and stays within one octave, then chain to the rest of
        construction."""
        assert self.inversion < len(self.base._full_interval_list)
        for il in self.get_interval_lists():
            absolute_intervals = il.absolute_intervals()
            assert absolute_intervals[0] == Interval.make(0, 0)
            for interval in absolute_intervals:
                assert interval.is_in_base_octave(accepting_octave=False)
        super().__post_init__()

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `fifth_omitted` to False (the fifth is part of the voicing)."""
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["fifth_omitted"] = False
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Pass `inversion`/`base` through positional-to-keyword normalization."""
        cls.arg_to_kwargs(args, kwargs, "inversion")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "base")
        return super()._clean_arguments_for_constructor(args, kwargs)