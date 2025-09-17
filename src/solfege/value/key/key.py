from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, List, Self

from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note
from solfege.value.note.abstract_note import OctaveOutput
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing


@dataclass(frozen=True)
class Key(DataClassWithDefaultArgument):
    """Represents a key for the partition. 
    
    Smaller key is the one with less alteration, or in case of equivalence the smallest note."""
    note: Note
    number_of_flats: int = 0
    number_of_sharps: int = 0

    """Maps note to its key"""
    _from_note: ClassVar[Dict[Note, "Key"]] = dict()

    """Map each note to the simplest enharmonic of this note."""
    _key_to_simplest_enharmonic: ClassVar[Dict[Note, Note]] = {}

    def simplest_enharmonic_major(self):
        return self.from_note(self._key_to_simplest_enharmonic[self.note.in_base_octave()])

    def simplest_enharmonic_minor(self):
        relative_interval = Interval.make(chromatic=3, diatonic=2)
        return self.from_note(
            self._key_to_simplest_enharmonic[(self.note + relative_interval).in_base_octave()] - relative_interval)

    @classmethod
    def add_enharmonic_set(cls, enharmonic_set: List[Key]):
        simplest = enharmonic_set[0]
        for key in enharmonic_set:
            cls._key_to_simplest_enharmonic[key.note.in_base_octave()] = simplest.note

    def _number_of_alterations(self):
        return self.number_of_flats + self.number_of_sharps

    @classmethod
    def from_note(cls, note: Note) -> Key:
        """Assume a key with this note was already added."""
        return cls._from_note[note.in_base_octave()]

    def __eq__(self, other):
        return self.note == other.note

    def __hash__(self):
        return hash(self.note)

    def __le__(self, other: Key):
        return (self._number_of_alterations(), self.note) <= (other._number_of_alterations(), other.note)

    def __lt__(self, other: Key):
        return (self._number_of_alterations(), self.note) < (other._number_of_alterations(), other.note)

    def __str__(self):
        return self.note.get_name_with_octave(octave_notation=OctaveOutput.OCTAVE_MIDDLE_PIANO_4, ascii=False) + (f" with {self.number_of_flats} ♭" if self.number_of_flats else "") + (
            f" with {self.number_of_sharps} #" if self.number_of_sharps else "")


    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["number_of_flats"] = 0
        default["number_of_sharps"] = 0
        return default
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_note(note: Note):
            return note.in_base_octave()
        cls.arg_to_kwargs(args, kwargs, "note", clean_note)
        cls._maybe_arg_to_kwargs(args, kwargs, "number_of_flats")
        cls._maybe_arg_to_kwargs(args, kwargs, "number_of_sharps")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.note, Note)
        assert_typing(self.number_of_flats, int)
        assert_typing(self.number_of_sharps, int)
        assert(self.note, self.note.in_base_octave())
        self._from_note[self.note.in_base_octave()] = self