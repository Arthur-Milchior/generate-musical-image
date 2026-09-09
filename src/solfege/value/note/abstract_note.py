from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, Optional, Self, Type, Union, TypeVar, Tuple, assert_never, overload
from enum import Enum

from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.abstract import Abstract
from solfege.value.note.clef import Clef
from solfege.value.singleton import Singleton
from utils.util import assert_optional_typing, assert_typing, img_tag

class AlterationOutput(Enum):
    """How to render a note's alteration (sharp/flat) as text."""
    ASCII = "ASCII"
    """Plain ASCII, e.g. "sharp"/"flat"."""
    SYMBOL = "SYMBOL"
    """Musical symbols, e.g. "#"/"♭"."""
    LILY = "LILY"
    """LilyPond syntax, e.g. "is"/"es"."""

class NoteOutput(Enum):
    """How to render a note's diatonic letter as text."""
    LETTER = "LETTER" # C, D, ..., B
    """Letter names: C, D, ..., B."""
    NUMBER = "NUMBER" # 1, ..., 7
    """Scale-degree numbers: 1, ..., 7."""
    FRENCH = "FRENCH" # do, ..., si
    """French solfège syllables: do, ..., si."""
    LILY = "LILY" #c, ..., b
    """LilyPond syntax: c, ..., b."""

class OctaveOutput(Enum):
    """How to render a note's octave as text."""
    MIDDLE_IS_0 = "0"
    """Octave numbering where middle C is octave 0."""
    MIDDLE_IS_4 = "4"
    """Scientific-pitch-notation-style numbering where middle C is octave 4."""
    LILY = "LILY"
    """LilyPond syntax (repeated `'`/`,` relative to the LilyPond default octave)."""

class FixedLengthOutput(Enum):
    """Whether/how an alteration's text rendering should be padded to a fixed width, so tables of
    note names line up."""
    SPACE_DOUBLE = "SPACE_DOUBLE"  # if we must consider double sharp and double flat
    """Fixed-width, padded with spaces, wide enough for double sharp/flat."""
    SPACE_SIMPLE = "SPACE_SIMPLE" # If we only deal with at moste one alteration
    """Fixed-width, padded with spaces, wide enough for a single sharp/flat only."""
    UNDERSCORE_DOUBLE = "DOUBLE"  # if we must consider double sharp and double flat
    """Fixed-width, padded with underscores, wide enough for double sharp/flat."""
    UNDERSCORE_SIMPLE = "SIMPLE" # If we only deal with at moste one alteration
    """Fixed-width, padded with underscores, wide enough for a single sharp/flat only."""
    NO = "NO"
    """Not padded: just the alteration text, however long it is."""

@dataclass(frozen=True)
class AbstractNote(Abstract, ABC, Generic[IntervalType]):
    """A note. Similar to an interval.

    -To a note may be added or subtracted an interval, but not to a note
    -Two note may be subtracted, leading to an interval.

    """
    make_instance_of_selfs_class: ClassVar[Type["AbstractNote"]]
    """Constructor used to build a new instance of this exact class (see `Singleton`/`Pair`)."""

    def __radd__(self, other: IntervalType) -> Self:
        """Support `interval + note` by delegating to `note + interval`, since addition here is
        commutative."""
        return self + other

    @overload
    def __sub__(self, other: IntervalType) -> Self:
        """Subtracting an interval from a note yields a note."""
        ...

    @overload
    def __sub__(self, other: Self) -> IntervalType:
        """Subtracting a note from a note yields an interval."""
        ...

    def get_octave_name(self, octave_notation: OctaveOutput) -> str:
        """The octave.  By default, starting at middle c. If scientific_notation, starting at C0"""
        if octave_notation == OctaveOutput.MIDDLE_IS_4:
            return str(self.octave() + 4)
        elif octave_notation == OctaveOutput.MIDDLE_IS_0:
            return str(self.octave())
        elif octave_notation == OctaveOutput.LILY:
            if self.octave() >= 0:
                return "'" * (self.octave() + 1)
            return "," * (-self.octave() - 1)
        raise assert_never(octave_notation)

    def file_name_for_lily_with_a_single_note(self, clef: Optional[Clef]):
        """Return the file for a lily partition of this note only in this clef."""
        assert_optional_typing(clef, Clef)
        from solfege.value.note.chromatic_note import Chromatic
        if clef is None:
            clef = Clef.TREBLE if self.octave() >= 0 else Clef.BASS
        # adding _ at start so that it's not deleted by anki.
        return f"_{str(clef)}_{self.non_ambiguous_string_for_file_name()}"

    def get_name_with_octave(self, octave_notation: OctaveOutput, **kwargs):
        """Return the note's full name (`get_name_up_to_octave`) followed by its octave marker
        (`get_octave_name`). `kwargs` are forwarded to `get_name_up_to_octave`."""
        return f"{self.get_name_up_to_octave(**kwargs)}{str(self.get_octave_name(octave_notation=octave_notation))}"

    # Must be implemented by subclasses

    @abstractmethod
    def __add__(self, other: IntervalType) -> Self:
        """Add an interval to this note, returning a note of the same class."""
        ...

    @abstractmethod
    def get_name_up_to_octave(self,
                              **kwargs
                               # potential argument. alteration_output: AlterationOutput, note_output: NoteOutput, fixed_length: FixedLengthOutput = FixedLengthOutput.NOT_FIXED_LENGTH
                              ) -> str:
        """Return the note's name without any octave information (e.g. "C#"), formatted
        according to `kwargs` (alteration/letter/padding output options, subclass-dependent)."""
        ...
    @abstractmethod
    def non_ambiguous_string_for_file_name(self) -> str:
        """Return a string uniquely identifying this note, safe to use as part of a generated
        file name."""
        ...


NoteType = TypeVar('NoteType', bound=AbstractNote)


def low_and_high(note_1: NoteType, note_2: NoteType) -> Tuple[NoteType, NoteType]:
    """Return the lowest and highest note of the inputs"""
    return min(note_1, note_2), max(note_1, note_2)


def pinky_and_thumb_side(note_1: NoteType, note_2: NoteType, for_right_hand: bool) -> Tuple[NoteType, NoteType]:
    """Return the note on pinky side and thumb side of the hand"""
    low, high = low_and_high(note_1, note_2)
    if for_right_hand:
        return high, low
    else:
        return low, high
