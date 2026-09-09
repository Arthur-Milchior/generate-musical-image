from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, List, Self

from solfege.value.interval.interval import Interval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing


@dataclass(frozen=True)
class Key(DataClassWithDefaultArgument):
    """Represents a key for the partition.

    Smaller key is the one with less alteration, or in case of equivalence the smallest note."""
    note: Note
    """The tonic note of this key, always normalized to the base octave."""
    number_of_flats: int = 0
    """Number of flats in this key's signature (0 if the key uses sharps or neither)."""
    number_of_sharps: int = 0
    """Number of sharps in this key's signature (0 if the key uses flats or neither)."""

    _from_note: ClassVar[Dict[Note, "Key"]] = dict()
    """Maps note to its key"""

    _key_to_simplest_enharmonic: ClassVar[Dict[Note, Note]] = {}
    """Map each note to the simplest enharmonic of this note."""

    def lily_key(self):
        """LilyPond key signature representation, delegating to `Note.lily_key()`."""
        return self.note.lily_key()

    def simplest_enharmonic_major(self):
        """Return the `Key` sharing this key's enharmonic set that has the fewest alterations (e.g.
        prefer C major over B# major)."""
        return self.from_note(self._key_to_simplest_enharmonic[self.note.in_base_octave()])

    def simplest_enharmonic_minor(self):
        """Like `simplest_enharmonic_major`, but treats this key as a minor key by first looking up
        its relative major (a minor third up) and converting the result back down."""
        relative_interval = Interval.make(_chromatic=3, _diatonic=2)
        return self.from_note(
            self._key_to_simplest_enharmonic[(self.note + relative_interval).in_base_octave()] - relative_interval)

    @classmethod
    def add_enharmonic_set(cls, enharmonic_set: List[Key]):
        """Register `enharmonic_set` (a list of enharmonically-equivalent keys, e.g. C/B#/Dbb) so that
        every key in it maps to the first (simplest) one via `_key_to_simplest_enharmonic`."""
        simplest = enharmonic_set[0]
        for key in enharmonic_set:
            cls._key_to_simplest_enharmonic[key.note.in_base_octave()] = simplest.note

    def _number_of_alterations(self):
        """Total alteration count (flats + sharps), used to rank keys by simplicity."""
        return self.number_of_flats + self.number_of_sharps

    @classmethod
    def from_note(cls, note: Note) -> Key:
        """Assume a key with this note was already added."""
        if isinstance(note, ChromaticNote):
            note = Note.from_chromatic(note)
        return cls._from_note[note.in_base_octave()]

    def __eq__(self, other):
        """Equal iff the tonic note is equal (signature counts are not part of equality)."""
        return self.note == other.note

    def __hash__(self):
        """Hash by the tonic note."""
        return hash(self.note)

    def __le__(self, other: Key):
        """Ordered by (number of alterations, note): fewer alterations first, then by note."""
        return (self._number_of_alterations(), self.note) <= (other._number_of_alterations(), other.note)

    def __lt__(self, other: Key):
        """Ordered by (number of alterations, note): fewer alterations first, then by note."""
        return (self._number_of_alterations(), self.note) < (other._number_of_alterations(), other.note)

    def __str__(self):
        """The tonic note's plain letter name, plus " with N ♭"/" with N #" if this key's signature
        has any alterations."""
        return self.note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.ASCII, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO) + (f" with {self.number_of_flats} ♭" if self.number_of_flats else "") + (
            f" with {self.number_of_sharps} #" if self.number_of_sharps else "")


    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default both `number_of_flats` and `number_of_sharps` to 0."""
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["number_of_flats"] = 0
        default["number_of_sharps"] = 0
        return default

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Normalize `note` to its base octave before construction."""
        def clean_note(note: Note):
            """Fold `note` into the base octave."""
            return note.in_base_octave()
        cls.arg_to_kwargs(args, kwargs, "note", clean_note)
        cls._maybe_arg_to_kwargs(args, kwargs, "number_of_flats")
        cls._maybe_arg_to_kwargs(args, kwargs, "number_of_sharps")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        """Validate field types and that `note` is already in the base octave, then register this
        key into `_from_note` so `Key.from_note` can look it up later."""
        assert_typing(self.note, Note)
        assert_typing(self.number_of_flats, int)
        assert_typing(self.number_of_sharps, int)
        assert(self.note, self.note.in_base_octave())
        self._from_note[self.note.in_base_octave()] = self