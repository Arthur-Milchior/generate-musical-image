from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Set

from guitar.finger_to_fret_delta import finger_to_fret_delta
from guitar.position.guitar_position import GuitarPosition
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.util import assert_typing


@dataclass(frozen=True)
class GuitarPositionWithFingers(GuitarPosition):
    fingers: FrozenSet[int]

    def __post_init__(self):
        assert_typing(self.fingers, frozenset)
        for finger in self.fingers:
            assert 1 <= finger <= 4
        super().__post_init__()

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_fingers(fingers):
            if isinstance(fingers, int):
                fingers = {fingers}
            return frozenset(fingers)
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fingers", clean_fingers)
        return args, kwargs

    def positions_for_interval(self, interval: ChromaticInterval):
        pos_to_fingers: Dict[GuitarPosition, Set[int]] = dict()
        for current_finger in self.fingers:
            for new_finger in range(1, 5):
                if new_finger== current_finger:
                    continue
                fret_delta = finger_to_fret_delta[current_finger][new_finger]
                for pos in self.positions_for_interval_with_restrictions(interval=interval, frets=fret_delta):
                    if pos not in pos_to_fingers:
                        pos_to_fingers[pos] = set()
                    pos_to_fingers[pos].add(new_finger)
        return [GuitarPositionWithFingers.make(string=pos.string, fret=pos.fret, fingers=fingers) for pos, fingers in pos_to_fingers.items()]
    
    def __repr__(self):
        return f"""GuitarPositionWithFingers.make({self.string.value}, {self.fret.value}, {set(self.fingers)})"""