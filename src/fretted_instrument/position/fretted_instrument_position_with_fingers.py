from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Self, Set, Tuple

from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.frozenlist import FrozenList, MakeableWithSingleArgument
from utils.util import assert_typing

FingersType = FrozenSet[int]
ALL_FINGERS = frozenset(range(1,5))

@dataclass(frozen=True)
class PositionOnFrettedInstrumentWithFingers(PositionOnFrettedInstrument, MakeableWithSingleArgument):
    fingers: FingersType

    @classmethod
    def _make_single_argument(cls, arg) -> Self:
        (string, fret, fingers) = arg
        return cls.make(string=string, fret=fret, fingers=fingers)

    def repr_single_argument(self) -> str:
        return f"""{(self.string.value, self.fret.value, set(self.fingers))}"""

    def restrict_fingers(self, fingers: FingersType):
        assert fingers <= self.fingers
        return PositionOnFrettedInstrumentWithFingers.make(instrument=self.instrument, fingers=fingers, string=self.string, fret=self.fret)

    def __post_init__(self):
        assert_typing(self.fingers, frozenset)
        for finger in self.fingers:
            assert 1 <= finger <= 4
        super().__post_init__()

    @staticmethod
    def from_fretted_instrument_position(pos: PositionOnFrettedInstrument, fingers: FingersType = ALL_FINGERS):
        return PositionOnFrettedInstrumentWithFingers.make(instrument = pos.instrument, fingers=fingers, string=pos.string, fret=pos.fret)

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_fingers(fingers):
            if isinstance(fingers, int):
                fingers = {fingers}
            return frozenset(fingers)
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers", clean_fingers)
        return args, kwargs

    def positions_for_interval(self, interval: ChromaticInterval) -> List[Tuple[FingersType, "PositionOnFrettedInstrumentWithFingers"]]:
        """Returns the set of next note to play this interval, and the fingers that could be used to reach it on current note."""
        # Associate to each position the fingers for the current and the next note.
        pos_to_fingers: Dict[PositionOnFrettedInstrument, Tuple[Set[int], Set[int]]] = dict()
        for current_finger in self.fingers:
            for new_finger in range(1, 5):
                if new_finger== current_finger:
                    continue
                fret_delta = self.instrument.finger_to_fret_delta[current_finger][new_finger]
                for pos in self.positions_for_interval_with_restrictions(interval=interval, frets=fret_delta):
                    if pos not in pos_to_fingers:
                        pos_to_fingers[pos] = (set(), set())
                    fingers_for_current_note, fingers_for_next_note = pos_to_fingers[pos]
                    fingers_for_current_note.add(current_finger)
                    fingers_for_next_note.add(new_finger)
        return [
            (frozenset(fingers_for_current_pos), 
             PositionOnFrettedInstrumentWithFingers.make(self.instrument, string=next_pos.string, fret=next_pos.fret, fingers=fingers_for_next_pos)
             ) for next_pos, (fingers_for_current_pos, fingers_for_next_pos) in pos_to_fingers.items()]
    
    def __repr__(self):
        return f"""FrettedInstrumentPositionWithFingers.make({self.string.value}, {self.fret.value}, {set(self.fingers)})"""
    
class FrettedInstrumentPositionWithFingersFrozenList(FrozenList[PositionOnFrettedInstrumentWithFingers]):
    type = PositionOnFrettedInstrumentWithFingers