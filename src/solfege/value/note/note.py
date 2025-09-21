from __future__ import annotations

from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Optional, Self, Tuple, Type, Union

from lily.Lilyable.local_lilyable import LocalLilyable
from solfege.value.chromatic import Chromatic
from solfege.value.interval.alteration.alteration import Alteration
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import AbstractNote, AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput, low_and_high
from solfege.value.note.note_alteration import NoteAlteration
from solfege.value.pair import Pair
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note_alteration import alteration_symbols
from solfege.value.note.diatonic_note import DiatonicNote
from utils.easyness import ClassWithEasyness
from utils.frozenlist import FrozenList
from utils.util import assert_optional_typing, assert_typing


@dataclass(frozen=True, repr=False, eq=True)
class Note(AbstractNote[Interval], Pair[ChromaticNote, DiatonicNote, NoteAlteration], ClassWithEasyness[int], LocalLilyable):
    """A note of the scale, as an interval from middle C."""
    DiatonicClass: ClassVar[Type[DiatonicNote]] = DiatonicNote
    ChromaticClass: ClassVar[Type[ChromaticNote]] = ChromaticNote
    IntervalClass: ClassVar[Type[Pair]] = Interval
    AlterationClass: ClassVar[Type[Alteration]] = NoteAlteration

    def __post_init__(self):
        super().__post_init__()
        assert_typing(self.get_chromatic(), ChromaticNote)
        assert_typing(self._diatonic, DiatonicNote)

    @classmethod
    def _make_single_argument(cls, arg: Union[Tuple[int, int], str]) -> Self:
        if isinstance(arg, str):
            return cls.from_name(arg)
        return cls.make(*arg)

    @staticmethod
    def from_name(name: str):
        name = name.strip()
        diatonic_name = "".join(letter for letter in name if letter not in alteration_symbols)
        alteration_name = "".join(letter for letter in name if letter in alteration_symbols)
        diatonic = DiatonicNote.from_name(diatonic_name)
        alteration = NoteAlteration.from_name(alteration_name)
        chromatic = Note.from_diatonic(diatonic).get_chromatic() + alteration
        return Note(chromatic, diatonic)
    
    def __repr__(self):
        return f"Note.make({self.get_chromatic().value}, {self._diatonic.value})"

    def _sub_note(self, other: Note) -> Interval:
        diatonic = self._diatonic - other._diatonic
        chromatic = self.get_chromatic() - other.get_chromatic()

        return self.IntervalClass.make_instance_of_selfs_class(chromatic, diatonic)

    def correctAlteration(self):
        """Whether the note has a printable alteration."""
        return self.get_alteration().printable()

    def adjacent(self, other: Note):
        """Whether `other` is at most two half-tone away"""
        lower, higher = low_and_high(self, other)
        from solfege.value.interval.interval import Interval
        diff: Interval = higher - lower
        value = diff.get_chromatic().value
        assert value > 0
        if value <= 2:
            return True
        if value > 3:
            return False
        if higher.in_base_octave().get_chromatic().value in [0, 1, 2, 5, 6, 7]:  # C or F natural
            return False
        return True

    def simplest_enharmonic(self):
        """Enharmonic note, with 0 alteration if possible or one of the same alteration"""
        from solfege.value.interval.interval import Interval
        enharmonic = self
        while enharmonic.get_alteration().value >= 2:
            # double sharp at least, let's add a diatonic note
            enharmonic += Interval.make(_diatonic=1, _chromatic=0)
        while enharmonic.get_alteration().value <= -2:
            # double flat at least, let's remove a diatonic note
            enharmonic += Interval.make(_diatonic=-1, _chromatic=0)
        if enharmonic.get_alteration().value == 1:
            # It's a sharp note. Let's check if adding a diatonic note lead to a white key
            above = enharmonic + Interval.make(_diatonic=1, _chromatic=0)
            if above.is_white_key_on_piano():
                return above
        if enharmonic.get_alteration().value == -1:
            # It's a flat note. Let's check if removing a diatonic note lead to a white key
            below = enharmonic + Interval.make(_diatonic=-1, _chromatic=0)
            if below.is_white_key_on_piano():
                return below
        return enharmonic

    def canonize(self, for_sharp: bool):
        from solfege.value.interval.interval import Interval
        """Enharmonic note, with no alteration if possible or a single sharp"""
        enharmonic = self
        while enharmonic.get_alteration().value > (1 if for_sharp else 0):
            # too many sharp least, let's add a diatonic note
            enharmonic += Interval.make(_diatonic=1, _chromatic=0)
        while enharmonic.get_alteration().value < (0 if for_sharp else -1):
            # too many flat, let's remove a diatonic note
            enharmonic += Interval.make(_diatonic=-1, _chromatic=0)
        if enharmonic.get_alteration().value == 1:
            # It's a sharp note. Let's check if adding a diatonic note lead to a white key
            above = enharmonic + Interval.make(_diatonic=1, _chromatic=0)
            if above.is_white_key_on_piano():
                return above
        if enharmonic.get_alteration().value == -1:
            # It's a flat note. Let's check if removing a diatonic note lead to a white key
            below = enharmonic + Interval.make(_diatonic=-1, _chromatic=0)
            if below.is_white_key_on_piano():
                return below
        return enharmonic
    
    def lily_in_scale(self):
        """A string valid in a scale in lily"""
        return self.get_name_with_octave(alteration_output=AlterationOutput.LILY, note_output=NoteOutput.LILY, octave_notation=OctaveOutput.LILY, fixed_length=FixedLengthOutput.NO, )
    
    def lily_key(self):
        """A string valid as key indication for lily"""
        return self.get_name_up_to_octave(alteration_output=AlterationOutput.LILY, note_output=NoteOutput.LILY, fixed_length=FixedLengthOutput.NO)

    def is_natural(self):
        return self.get_alteration() == NATURAL

    def is_sharp(self):
        return self.get_alteration() == SHARP

    def is_flat(self):
        return self.get_alteration() == FLAT

    def is_double_sharp(self):
        return self.get_alteration() == DOUBLE_SHARP

    def is_double_flat(self):
        return self.get_alteration() == DOUBLE_FLAT
    
    def is_black_key_on_piano(self):
        return self.get_chromatic().is_black_key_on_piano()
    
    def is_white_key_on_piano(self):
        return self.get_chromatic().is_white_key_on_piano()
    
    def change_octave_to_be_enharmonic(self, chromatic_note: ChromaticNote) -> Optional[Self]:
        from solfege.value.interval.chromatic_interval import ChromaticInterval
        chromatic_distance: ChromaticInterval = chromatic_note - self.get_chromatic() 
        if chromatic_distance.value % Chromatic.number_of_interval_in_an_octave != 0:
            return None
        number_octave = chromatic_distance.value // Chromatic.number_of_interval_in_an_octave
        return self.add_octave(number_octave)
    
    #pragma mark - Abstract
    
    def __sub__(self, other: Union[Self, Interval]) -> Union[Self, Interval]:
        chromatic = self.get_chromatic() - other.get_chromatic()
        diatonic = self._diatonic - other._diatonic
        if self.__class__ == other.__class__:
            return Interval.make(chromatic, diatonic)
        else:
            assert other.__class__ == Interval
            return dataclasses.replace(self, _chromatic=chromatic, _diatonic=diatonic)
        
    #Pragma mark - AbstractNote

    def get_name_up_to_octave(self, alteration_output: AlterationOutput, note_output: NoteOutput, fixed_length: FixedLengthOutput):
        diatonic_note: DiatonicNote = self.get_diatonic()
        diatonic_name = diatonic_note.get_name_up_to_octave(note_output=note_output, fixed_length=fixed_length)
        alteration: NoteAlteration = self.get_alteration()
        alteration_name = alteration.get_name(alteration_output=alteration_output, fixed_length=fixed_length)
        return f"""{diatonic_name}{alteration_name}"""
 
    def __add__(self, other: Interval) -> Self:
        if isinstance(other, Interval):
            return dataclasses.replace(self, _chromatic=self.get_chromatic() + other.get_chromatic(), _diatonic=self._diatonic + other._diatonic)
        return NotImplemented

    def non_ambiguous_string_for_file_name(self):
        """Return the file name without extension nor folder"""
        return self.get_name_with_octave(
                    octave_notation=OctaveOutput.MIDDLE_IS_4,
                    alteration_output = AlterationOutput.ASCII, 
                    note_output = NoteOutput.LETTER, 
                    fixed_length = FixedLengthOutput.NO
                   )

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> int:
        return abs(self._get_alteration_value())
    
    #pragma mark - Pair

    def get_alteration_constructor(self):
        return NoteAlteration.make

ChromaticNote.PairClass = Note
DiatonicNote.PairClass = Note

ChromaticNote.DiatonicClass = DiatonicNote
DiatonicNote.ChromaticClass = ChromaticNote

class NoteFrozenList(FrozenList[Note]):
    type = Note


IntervalFrozenList.note_frozen_list_type = NoteFrozenList