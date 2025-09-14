
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.chord.abstract_inversion import AbstractInversion
from solfege.pattern_instantiation.chord.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.frozenlist import FrozenList
from utils.util import assert_typing


class Inversion(AbstractInversion[Note, Interval, NoteFrozenList, IntervalFrozenList], AbstractPairInstantiation[InversionPattern]):
    pass