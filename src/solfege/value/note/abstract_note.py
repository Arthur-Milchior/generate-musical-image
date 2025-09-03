from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type, Union, TypeVar, Tuple, assert_never
from enum import Enum

from solfege.value.interval.abstract_interval import AbstractInterval
from solfege.value.abstract import Abstract
from solfege.value.singleton import Singleton
from utils.util import assert_typing

class AlterationOutput(Enum):
    ASCII = "ASCII"
    SYMBOL = "SYMBOL"
    LILY = "LILY"

class NoteOutput(Enum):
    LETTER = "LETTER" # C, D, ..., B
    NUMBER = "NUMBER" # 1, ..., 7
    FRENCH = "FRENCH" # do, ..., si
    LILY = "LILY" #c, ..., b

class OctaveOutput(Enum):
    MIDDLE_IS_0 = "0"
    MIDDLE_IS_4 = "4"
    LILY = "LILY"

class FixedLengthOutput(Enum):
    SPACE_DOUBLE = "SPACE_DOUBLE"  # if we must consider double sharp and double flat
    SPACE_SIMPLE = "SPACE_SIMPLE" # If we only deal with at moste one alteration
    UNDERSCORE_DOUBLE = "DOUBLE"  # if we must consider double sharp and double flat
    UNDERSCORE_SIMPLE = "SIMPLE" # If we only deal with at moste one alteration
    NO = "NO"

@dataclass(frozen=True)
class AbstractNote(Abstract):
    make_instance_of_selfs_class: ClassVar[Type["AbstractNote"]]
    """A note. Similar to an interval.

    -To a note may be added or subtracted an interval, but not to a note
    -Two note may be subtracted, leading to an interval.

    """

    def is_note(self):
        return True

    def __neg__(self):
        raise Exception("Trying to negate a note makes no sens.")

    def __neg__(self):
        raise Exception("Trying to multiply a note makes no sens.")

    def __sub__(self, other: Union[AbstractInterval, AbstractNote]) -> Abstract:
        if isinstance(other, AbstractNote):
            return self._sub_note(other)
        else:
            return self._sub_interval(other)

    def _sub_interval(self, other: AbstractInterval):
        return self + (-other)

    def _sub_note(self, other: AbstractNote):
        return NotImplemented

    def __radd__(self, other: AbstractInterval):
        # called as other + self
        return self + other

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

    def get_name_up_to_octave(self,
                              **kwargs
                               # potential argument. alteration_output: AlterationOutput, note_output: NoteOutput, fixed_length: FixedLengthOutput = FixedLengthOutput.NOT_FIXED_LENGTH
                              ) -> str:
        return NotImplemented

    def get_name_with_octave(self, octave_notation: OctaveOutput, **kwargs):
        return f"{self.get_name_up_to_octave(**kwargs)}{str(self.get_octave_name(octave_notation=octave_notation))}"


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
