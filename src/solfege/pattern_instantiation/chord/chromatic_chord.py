
from typing import ClassVar
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern_instantiation.chord.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.chord.chord import AbstractChord
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.interval import Interval
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from solfege.value.note.note import Note
from utils.frozenlist import FrozenList


class ChromaticChord(AbstractChord[Note, Interval, ChromaticNoteFrozenList, ChromaticIntervalFrozenList], AbstractChromaticInstantiation[ChordPattern]):
    pass