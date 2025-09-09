from dataclasses import dataclass
from typing import ClassVar, Optional, Type
from solfege.value.interval.chromatic_interval import ChromaticIntervalFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.value.chromatic import Chromatic
from solfege.value.note.singleton_note import AbstractSingletonNote
from utils.frozenlist import FrozenList
from utils.util import img_tag


@dataclass(frozen=True, repr=False, eq=False)
class ChromaticNote(AbstractSingletonNote, Chromatic):
    AlterationClass: ClassVar[Type[Chromatic]]
    @staticmethod
    def from_name(name) -> "ChromaticNote":
        from solfege.value.note.note import Note
        return Note.from_name(name).get_chromatic()

    def get_color(self, color=True):
        """Color to print the note in lilypond"""
        return "black"

    def get_name_up_to_octave(self, alteration_output: AlterationOutput, note_output: NoteOutput, fixed_length: FixedLengthOutput):
        return self.get_note().get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

    def get_note(self, cls=None):
        """A solfège note. Diatonic note is guessed. The default class is
        Note. May return None if no diatonic note can be guessed. """
        diatonic = self.get_diatonic()
        if diatonic is None:
            return None
        if cls is None:
            from solfege.value.note.note import Note
            cls = Note
        diatonic = diatonic
        return cls(diatonic=diatonic, chromatic=self)

    def is_white_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        return not self.is_black_key_on_piano()

    def is_black_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().value % 12) in blacks
    
ChromaticNote.ChromaticClass = ChromaticNote

class ChromaticNoteFrozenList(FrozenList[ChromaticNote]):
    type = ChromaticNote

ChromaticIntervalFrozenList.note_frozen_list_type = ChromaticNoteFrozenList