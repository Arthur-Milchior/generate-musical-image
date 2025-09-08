from dataclasses import dataclass
from typing import Dict, FrozenSet, Generator, List
from guitar.position.guitar_position_with_fingers import GuitarPositionWithFingers
from guitar.position.set.set_of_guitar_positions import SetOfGuitarPositions
from guitar.position.string.string import String
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.util import assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class AnkiScaleWithStart(DataClassWithDefaultArgument):
    start_string: String
    number_of_octaves: int
    fingers: FrozenSet[int]
    scales: FrozenList[SetOfGuitarPositions]


    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "start_string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_octaves")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers", frozenset)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "scales", FrozenList)
        return args, kwargs

    def __post_init__(self):
        assert_typing(self.scales, FrozenList)
        assert_iterable_typing(self.scales, SetOfGuitarPositions)
        assert_typing(self.fingers, frozenset)
        assert_iterable_typing(self.fingers, int)
        assert_typing(self.start_string, String)
        assert_typing(self.number_of_octaves, int)
        assert_typing(self.number_of_octaves, int)
        assert 1 <= self.number_of_octaves <= 2

def _generate_scale(starting_note: GuitarPositionWithFingers, relative_intervals: FrozenList[ChromaticInterval]) -> Generator[FrozenList[GuitarPositionWithFingers]]:
    if not relative_intervals:
        yield FrozenList([starting_note])
        return
    relative_interval, remaining_relative_intervals = relative_intervals.head_tail()
    for fingers_for_current_note, next_note in starting_note.positions_for_interval(interval=relative_interval):
        starting_note_fingered = starting_note.restrict_fingers(fingers_for_current_note)
        for notes_for_remaining_intervals in _generate_scale(next_note, remaining_relative_intervals):
            yield FrozenList([starting_note_fingered, *notes_for_remaining_intervals])

def generate_scale(starting_note: GuitarPositionWithFingers, scale_pattern: ScalePattern, number_of_octaves: int):
    fingers_to_scales: Dict[FrozenSet[int], List[SetOfGuitarPositions]] = dict()
    for scale in _generate_scale(starting_note, scale_pattern.multiple_octaves(number_of_octaves).relative_chromatic()):
        first_pos, _ = scale.head_tail()
        first_fingers = first_pos.fingers
        if first_fingers not in fingers_to_scales:
            fingers_to_scales[first_fingers] = []
        fingers_to_scales[first_fingers].append(SetOfGuitarPositions.make(scale))

    anki_notes:List[AnkiScaleWithStart] = []
    for fingers, scales in fingers_to_scales.items():
        scales.sort()
        anki_notes.append(AnkiScaleWithStart.make(start_string=starting_note.string, fingers=fingers, number_of_octaves=number_of_octaves, scales = scales))
    return anki_notes
