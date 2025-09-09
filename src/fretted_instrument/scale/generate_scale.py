from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Generator, List
from fretted_instrument.position.guitar_position import GuitarPosition
from fretted_instrument.position.guitar_position_with_fingers import FingersType, GuitarPositionWithFingers, GuitarPositionWithFingersFrozenList
from fretted_instrument.position.set.set_of_guitar_positions import SetOfGuitarPositions, SetOfGuitarPositionsFrozenList
from fretted_instrument.position.set.set_of_guitar_positions_with_fingers import SetOfGuitarPositionsWithFingers, SetOfGuitarPositionsWithFingersFrozenList
from fretted_instrument.position.string.string import String
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.value.interval.chromatic_interval import ChromaticIntervalFrozenList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozendict import FrozenDict
from utils.util import assert_dict_typing, assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class AnkiScaleWithFingersAndString(DataClassWithDefaultArgument):
    start_string: String
    number_of_octaves: int
    fingers: FingersType
    pattern: ScalePattern
    scales: SetOfGuitarPositionsWithFingersFrozenList

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "start_string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_octaves")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers", frozenset)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "scales", SetOfGuitarPositionsWithFingersFrozenList)
        return args, kwargs

    def __post_init__(self):
        assert_typing(self.scales, SetOfGuitarPositionsWithFingersFrozenList)
        assert_iterable_typing(self.scales, SetOfGuitarPositionsWithFingers)
        assert_typing(self.fingers, frozenset)
        assert_iterable_typing(self.fingers, int)
        assert_typing(self.start_string, String)
        assert_typing(self.number_of_octaves, int)
        assert_typing(self.number_of_octaves, int)
        assert 1 <= self.number_of_octaves <= 2

    def __len__(self):
        return len(self.scales)

@dataclass(frozen=True)
class AnkiScaleWithString(DataClassWithDefaultArgument):
    start_string: String
    number_of_octaves: int
    pattern: ScalePattern
    fingers_to_scales: FrozenDict[FingersType, AnkiScaleWithFingersAndString] = field(hash=False)

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "start_string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_octaves")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "pattern")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers_to_scales", FrozenDict)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        all_fingers = set()
        # To find case where the same finger occurs in multiple places.
        assert_typing(self.fingers_to_scales, FrozenDict)
        assert_dict_typing(self.fingers_to_scales, frozenset, AnkiScaleWithFingersAndString)
        for new_fingers, scales in self.fingers_to_scales.items():
            # for new_finger in new_fingers:
            #     assert new_finger not in all_fingers
            assert scales.start_string == self.start_string
            assert scales.number_of_octaves == self.number_of_octaves
            assert new_fingers == scales.fingers
            assert self.pattern == scales.pattern
            all_fingers = all_fingers | new_fingers
        super().__post_init__()

    def __len__(self):
        return sum (len(scales) for scales in self.fingers_to_scales.values())
    
    def all_scales(self):
        l = [scale for aswfas in self.fingers_to_scales.values() for scale in aswfas.scales]
        l.sort(key = lambda scale: scale.number_of_frets(include_open=False))
        return l
    

def _generate_scale(starting_note: GuitarPositionWithFingers, relative_intervals: ChromaticIntervalFrozenList) -> Generator[List[GuitarPositionWithFingers]]:
    assert_typing(starting_note, GuitarPositionWithFingers)
    if not relative_intervals:
        yield [starting_note]
        return
    relative_interval, remaining_relative_intervals = relative_intervals.head_tail()
    for fingers_for_current_note, next_note in starting_note.positions_for_interval(interval=relative_interval):
        starting_note_fingered = starting_note.restrict_fingers(fingers_for_current_note)
        for notes_for_remaining_intervals in _generate_scale(next_note, remaining_relative_intervals):
            assert_iterable_typing(notes_for_remaining_intervals, GuitarPositionWithFingers)
            yield [starting_note_fingered, *notes_for_remaining_intervals]

def generate_scale(starting_note: GuitarPosition, scale_pattern: ScalePattern, number_of_octaves: int):
    fingers_to_scales: Dict[FingersType, List[SetOfGuitarPositions]] = dict()
    starting_note = GuitarPositionWithFingers.from_guitar_position(starting_note)
    assert_typing(scale_pattern, ScalePattern)
    for scale in _generate_scale(starting_note, scale_pattern.multiple_octaves(number_of_octaves).get_chromatic_interval_list().relative_intervals()):
        first_pos = scale[0]
        first_fingers = first_pos.fingers
        if first_fingers not in fingers_to_scales:
            fingers_to_scales[first_fingers] = []
        fingers_to_scales[first_fingers].append(SetOfGuitarPositions.make(scale))

    finger_to_anki_scale_with_fingers_and_strings: Dict[FingersType, AnkiScaleWithFingersAndString] = dict()
    for fingers, scales in fingers_to_scales.items():
        scales.sort()
        finger_to_anki_scale_with_fingers_and_strings[fingers] = AnkiScaleWithFingersAndString.make(start_string = starting_note.string, number_of_octaves=number_of_octaves, fingers=fingers, pattern=scale_pattern, scales=scales)
    return AnkiScaleWithString.make(start_string =starting_note.string, number_of_octaves = number_of_octaves, pattern=scale_pattern, fingers_to_scales=finger_to_anki_scale_with_fingers_and_strings)
