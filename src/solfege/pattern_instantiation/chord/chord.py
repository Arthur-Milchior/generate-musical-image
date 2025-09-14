
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern_instantiation.chord.abstract_chord import AbstractChord
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.chord.chromatic_chord import ChromaticChord
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import  NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.util import assert_typing


class Chord(AbstractChord[Note, Interval, NoteFrozenList, IntervalFrozenList], AbstractPairInstantiation[ChordPattern]):
    
    chromatic_instantiation_type: ClassVar = ChromaticChord