from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Generator, List
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from fretted_instrument.position.fretted_instrument_position_with_fingers import FingersType, PositionOnFrettedInstrumentWithFingers, FrettedInstrumentPositionWithFingersFrozenList
from fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, SetOfPositionsOnFrettedInstrumentFrozenList
from fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import SetOfFrettedInstrumentPositionsWithFingers, SetOfFrettedInstrumentPositionsWithFingersFrozenList
from fretted_instrument.position.string.string import String
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.value.interval.chromatic_interval import ChromaticIntervalFrozenList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozendict import FrozenDict
from utils.util import assert_dict_typing, assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class AnkiScaleWithFingersAndString(DataClassWithDefaultArgument):
    instrument: FrettedInstrument
    start_string: String
    number_of_octaves: int
    fingers: FingersType
    pattern: ScalePattern
    scales: SetOfFrettedInstrumentPositionsWithFingersFrozenList

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_scales(scales):
            return SetOfFrettedInstrumentPositionsWithFingersFrozenList(
                (instrument, scale) for scale in scales
            )
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        instrument = kwargs["instrument"]
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "start_string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_octaves")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers", frozenset)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "pattern")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "scales", clean_scales)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.scales, SetOfFrettedInstrumentPositionsWithFingersFrozenList)
        assert_iterable_typing(self.scales, SetOfFrettedInstrumentPositionsWithFingers)
        assert_typing(self.instrument, FrettedInstrument)
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
    instrument: FrettedInstrument
    start_string: String
    number_of_octaves: int
    pattern: ScalePattern
    fingers_to_scales: FrozenDict[FingersType, AnkiScaleWithFingersAndString] = field(hash=False)

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "start_string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_octaves")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "pattern")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers_to_scales", FrozenDict)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        all_fingers = set()
        # To find case where the same finger occurs in multiple places.
        assert_typing(self.fingers_to_scales, FrozenDict)
        assert_typing(self.instrument, FrettedInstrument)
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
        l.sort(key = lambda scale: scale.number_of_frets(allow_open=False))
        return l
    

def _generate_scale(starting_note: PositionOnFrettedInstrumentWithFingers, relative_intervals: ChromaticIntervalFrozenList) -> Generator[List[PositionOnFrettedInstrumentWithFingers]]:
    assert_typing(starting_note, PositionOnFrettedInstrumentWithFingers)
    if not relative_intervals:
        yield [starting_note]
        return
    relative_interval, remaining_relative_intervals = relative_intervals.head_tail()
    for fingers_for_current_note, next_note in starting_note.positions_for_interval(interval=relative_interval):
        starting_note_fingered = starting_note.restrict_fingers(fingers_for_current_note)
        for notes_for_remaining_intervals in _generate_scale(next_note, remaining_relative_intervals):
            assert_iterable_typing(notes_for_remaining_intervals, PositionOnFrettedInstrumentWithFingers)
            yield [starting_note_fingered, *notes_for_remaining_intervals]

def generate_scale(starting_note: PositionOnFrettedInstrument, scale_pattern: ScalePattern, number_of_octaves: int):
    instrument = starting_note.instrument
    fingers_to_scales: Dict[FingersType, List[SetOfPositionOnFrettedInstrument]] = dict()
    starting_note = PositionOnFrettedInstrumentWithFingers.from_fretted_instrument_position(starting_note)
    assert_typing(scale_pattern, ScalePattern)
    for scale in _generate_scale(starting_note, scale_pattern.multiple_octaves(number_of_octaves).get_chromatic_interval_list().relative_intervals()):
        first_pos = scale[0]
        first_fingers = first_pos.fingers
        if first_fingers not in fingers_to_scales:
            fingers_to_scales[first_fingers] = []
        fingers_to_scales[first_fingers].append(SetOfPositionOnFrettedInstrument.make(instrument=instrument, positions=scale))

    finger_to_anki_scale_with_fingers_and_strings: Dict[FingersType, AnkiScaleWithFingersAndString] = dict()
    for fingers, scales in fingers_to_scales.items():
        scales.sort()
        finger_to_anki_scale_with_fingers_and_strings[fingers] = AnkiScaleWithFingersAndString.make(instrument=instrument, start_string = starting_note.string, number_of_octaves=number_of_octaves, fingers=fingers, pattern=scale_pattern, scales=scales)
    return AnkiScaleWithString.make(instrument=instrument, start_string =starting_note.string, number_of_octaves = number_of_octaves, pattern=scale_pattern, fingers_to_scales=finger_to_anki_scale_with_fingers_and_strings)
