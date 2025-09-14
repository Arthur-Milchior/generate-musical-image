from dataclasses import dataclass, field
from typing import Callable, Dict, FrozenSet, Generator, List, Optional, Set, Tuple
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position_with_fingers import FingersType, PositionOnFrettedInstrumentWithFingers, FrettedInstrumentPositionWithFingersFrozenList
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, SetOfPositionsOnFrettedInstrumentFrozenList
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import SetOfFrettedInstrumentPositionsWithFingers, SetOfFrettedInstrumentPositionsWithFingersFrozenList
from instruments.fretted_instrument.position.string.string import String
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.value.interval.chromatic_interval import ChromaticIntervalFrozenList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozendict import FrozenDict
from utils.frozenlist import FrozenList
from utils.util import assert_dict_typing, assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class AnkiScaleWithFingersAndString(DataClassWithDefaultArgument):
    instrument: FrettedInstrument
    start_string: String
    number_of_octaves: int
    fingers: FingersType
    pattern: ScalePattern
    scales: SetOfFrettedInstrumentPositionsWithFingersFrozenList

    def __len__(self):
        return len(self.scales)

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument", type=FrettedInstrument)
        instrument = kwargs["instrument"]
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "start_string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_octaves")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers", frozenset)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "pattern")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "scales", SetOfFrettedInstrumentPositionsWithFingersFrozenList)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.scales, SetOfFrettedInstrumentPositionsWithFingersFrozenList)
        assert_iterable_typing(self.scales, SetOfFrettedInstrumentPositionsWithFingers)
        assert_typing(self.instrument, FrettedInstrument)
        assert_typing(self.fingers, frozenset)
        # if we go to a higher fret we can't use 4, 
        # If we go to a lower fret we can't use 1.
        # However, if we start with two notes on the same fret, we can use either 4 or 1. 
        # No scale start by a fourth just, so this is not a concern if we start on a non-4 string.
        # Hirajōshi Burrows is the only scale starting with a third major. I expect this assertion to fail due to the actually hard to play 
        # scale with fourth followed by 1 on the same fret. If so, the code will need to be changed to forbid this.

        # Actually, the problem already exists with the major arpeggio.
        #assert 1 not in self.fingers or 4 not in self.fingers
        assert_iterable_typing(self.fingers, int)
        assert_typing(self.start_string, String)
        assert_typing(self.number_of_octaves, int)
        assert_typing(self.number_of_octaves, int)
        assert 1 <= self.number_of_octaves <= 2

@dataclass(frozen=True)
class AnkiScaleWithString(DataClassWithDefaultArgument):
    instrument: FrettedInstrument
    start_string: String
    number_of_octaves: int
    pattern: ScalePattern
    fingers_to_scales: FrozenDict[FingersType, AnkiScaleWithFingersAndString] = field(hash=False)

    def __len__(self):
        return sum (len(scales) for scales in self.fingers_to_scales.values())
    
    def all_scales(self) -> List[Tuple[FingersType, SetOfFrettedInstrumentPositionsWithFingers]]:
        l = [(aswfas.fingers, scale) for aswfas in self.fingers_to_scales.values() for scale in aswfas.scales]
        l.sort(key = lambda fingers_scale: fingers_scale[1].number_of_frets(allow_open=False))
        return l
    
    def scales_starting_with_finger(self, finger: int, excluded_fingers: Set[int]= frozenset()):
        """Return the scales, from easiest to hardest, containing `finger` and that can't be played with any of the `excluded_fingers`."""
        assert isinstance(excluded_fingers, set) or isinstance(excluded_fingers, frozenset) 
        l = []
        for fingers, scales in self.fingers_to_scales.items():
            if finger not in fingers:
                continue
            if fingers & excluded_fingers:
                # An excluded finger is found.
                continue
            l += scales.scales
        l.sort()
        return l
    
    def best_for_each_finger(self):
        """Return the best scale for the first finger, a middle finger and the last finger.
        For the middle finger, we select the best that is not with first or last."""
        best_first_fingers_scale: Optional[Tuple[FingersType, SetOfPositionOnFrettedInstrument]] = None
        best_middle_fingers_scale: Optional[Tuple[FingersType, SetOfPositionOnFrettedInstrument]] = None
        best_fourth_fingers_scale: Optional[Tuple[FingersType, SetOfPositionOnFrettedInstrument]] = None
        fingers_and_scale_list = self.all_scales()
        while (best_first_fingers_scale is None or best_middle_fingers_scale is None or best_fourth_fingers_scale is None) and fingers_and_scale_list:
            fingers, scale = fingers_and_scale_list.pop(0)
            if 1 in fingers and best_first_fingers_scale is None:
                best_first_fingers_scale = fingers, scale
                continue
            if 4 in fingers and best_fourth_fingers_scale is None:
                best_fourth_fingers_scale = fingers, scale
                continue
            if best_middle_fingers_scale is None:
                if {2, 3} & fingers:
                    best_middle_fingers_scale = fingers, scale
                    continue
                if 1 in fingers and ({2, 3}&best_first_fingers_scale[0]):
                    # moving the best from first to middle, so that we still have a good for first and the best at middle.
                    best_middle_fingers_scale = best_first_fingers_scale
                    best_first_fingers_scale = fingers, scale
                    continue
                if 4 in fingers and ({2, 3}&best_fourth_fingers_scale[0]):
                    # moving the best from fourth to middle, so that we still have a good for fourth and the best at middle.
                    best_middle_fingers_scale = best_fourth_fingers_scale
                    best_fourth_fingers_scale = fingers, scale
                    continue
        def pair_to_scale(pair: Optional[Tuple[FingersType, SetOfPositionOnFrettedInstrument]]):
            if pair is None:
                return None
            fingers, scale = pair
            return scale
        return (pair_to_scale(best_first_fingers_scale), pair_to_scale(best_middle_fingers_scale), pair_to_scale(best_fourth_fingers_scale))

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument", type=FrettedInstrument)
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


def _generate_scale(instrument: FrettedInstrument, starting_note: PositionOnFrettedInstrumentWithFingers, relative_intervals: ChromaticIntervalFrozenList) -> Generator[List[PositionOnFrettedInstrumentWithFingers]]:
    assert_typing(starting_note, PositionOnFrettedInstrumentWithFingers)
    if not relative_intervals:
        yield [starting_note]
        return
    relative_interval, remaining_relative_intervals = relative_intervals.head_tail()
    for fingers_for_current_note, next_note in starting_note.positions_for_interval(instrument, interval=relative_interval):
        starting_note_fingered = starting_note.restrict_fingers(fingers_for_current_note)
        for notes_for_remaining_intervals in _generate_scale(instrument, next_note, remaining_relative_intervals):
            assert_iterable_typing(notes_for_remaining_intervals, PositionOnFrettedInstrumentWithFingers)
            yield [starting_note_fingered, *notes_for_remaining_intervals]

def generate_scale(instrument: FrettedInstrument, 
                starting_note: PositionOnFrettedInstrument,
                scale_pattern: ScalePattern,
            number_of_octaves: int,
            filter: Callable[[SetOfFrettedInstrumentPositionsWithFingers], bool] = lambda x: True,
        pattern_to_avoid_list: List[SetOfFrettedInstrumentPositionsWithFingers] = []) -> AnkiScaleWithString:
    """
    patter_to_avoid - don't return any position that is a subset of this one.
    filter: keep only the value for which the answer is true."""
    assert_iterable_typing(pattern_to_avoid_list, SetOfFrettedInstrumentPositionsWithFingers)
    fingers_to_scales: Dict[FingersType, List[SetOfFrettedInstrumentPositionsWithFingers]] = dict()
    starting_note = PositionOnFrettedInstrumentWithFingers.from_fretted_instrument_position(starting_note)
    assert_typing(scale_pattern, ScalePattern)
    for scale in _generate_scale(instrument, starting_note, scale_pattern.multiple_octaves(number_of_octaves).get_chromatic_interval_list().relative_intervals()):
        first_pos = scale[0]
        first_fingers = first_pos.fingers
        if first_fingers not in fingers_to_scales:
            fingers_to_scales[first_fingers] = []
        set_of_pos = SetOfFrettedInstrumentPositionsWithFingers.make(positions=scale)
        if not filter(set_of_pos):
            continue
        must_be_avoided = False
        for pattern_to_avoid in pattern_to_avoid_list:
            if set_of_pos <= pattern_to_avoid:
                must_be_avoided = True
                break
        if must_be_avoided:
            continue
        fingers_to_scales[first_fingers].append(set_of_pos)

    finger_to_anki_scale_with_fingers_and_strings: Dict[FingersType, AnkiScaleWithFingersAndString] = dict()
    for fingers, scales in fingers_to_scales.items():
        scales.sort()
        finger_to_anki_scale_with_fingers_and_strings[fingers] = AnkiScaleWithFingersAndString.make(instrument=instrument, start_string = starting_note.string, number_of_octaves=number_of_octaves, fingers=fingers, pattern=scale_pattern, scales=scales)
    return AnkiScaleWithString.make(instrument=instrument, start_string =starting_note.string, number_of_octaves = number_of_octaves, pattern=scale_pattern, fingers_to_scales=finger_to_anki_scale_with_fingers_and_strings)
