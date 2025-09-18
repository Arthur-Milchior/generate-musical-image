
from dataclasses import dataclass
from typing import Callable, ClassVar, Dict, Generic, List, Optional, Self, Type

from lily.lily import chord
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import AbstractIntervalListPattern, IntervalListPattern
from solfege.value.note.abstract_note import AbstractNote, AlterationOutput, FixedLengthOutput, NoteOutput, NoteType, OctaveOutput
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note, NoteFrozenList
from solfege.value.note.set.abstract_note_list import AbstractNoteList
from utils.easyness import ClassWithEasyness
from utils.frozenlist import FrozenList
from utils.util import assert_iterable_typing, assert_typing, indent
from .chromatic_note_list import ChromaticNoteList


class NoteList(AbstractNoteList[Note, Interval, IntervalListPattern], ClassWithEasyness[int]):
    interval_list_type: ClassVar[Type[AbstractIntervalListPattern]] = IntervalListPattern
    _frozen_list_type: ClassVar[Type[FrozenList[AbstractNote]]] = NoteFrozenList

    note_type: ClassVar[Type[AbstractNote]] = Note

    def find_note_from_list_up_to_octave(self, chromatic_note: ChromaticNote):
        """Return a note that is enharmonic to `chromatic_note` and equal - up to octave - to a note of `self`.
        In case of ambiguity, assert.
        """
        found = None
        for note in self:
            changed = note.change_octave_to_be_enharmonic(chromatic_note)
            if changed is not None:
                if found is not None:
                    assert found == changed, f"{found} and {changed} are two possible notes. Meaning that, up two octave, this list has enharmonic notes."
                found = changed
        return found
    
    def lily_chord(self):
        """Lily code for this chord."""
        return f"""<{" ".join(note.lily_in_scale() for note in self)}>"""
    
    def lily_file_with_only_chord(self, clef: Clef):
        """Lily code for a file containing just this as a chord"""
        return f"""\\version "2.20.0"
\\score{{
  \\new Staff{{
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef {str(clef)}
{indent(self.lily_chord(), 6)}
  }}
}}"""
    
    def lily_file_name(self, clef: Clef):
        """Return a name for the file containing those notes, without extension"""
        notes = list(self)
        notes.sort()
        notes_str = "_".join(note.get_name_with_octave(
            alteration_output=AlterationOutput.ASCII,
            note_output=NoteOutput.LETTER, 
            fixed_length=FixedLengthOutput.UNDERSCORE_DOUBLE,
            octave_notation=OctaveOutput.MIDDLE_IS_4
            ) for note in self)
        return f"chord_{str(clef)}_{notes_str}"
    
    def chromatic(self):
        return ChromaticNoteList.make(note.chromatic for note in self)
        
    def change_octave_to_be_enharmonic(self, chromatic_note_list: ChromaticNoteList) -> Optional[Self]:
        """Return a list of note, enharmonic to `chromatic_note_list`, containing notes equals to note of the current list, up to octave.
        Return None if some note can't be found.
        """
        notes = []
        for chromatic_note in chromatic_note_list:
            note = self.find_note_from_list_up_to_octave(chromatic_note)
            if note is None:
                return None
            notes.append(note)
        return self.__class__.make(notes)

    def __repr__(self):
        return f"""NoteList.make([{", ".join(f"({note.chromatic.value}, {note.diatonic.value})" for note in self)}])"""
    
    def easy_key(self) -> int:
        return sum(note.easy_key() for note in self)