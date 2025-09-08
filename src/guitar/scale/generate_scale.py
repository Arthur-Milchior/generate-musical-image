from typing import List
from guitar.position.guitar_position_with_fingers import GuitarPositionWithFingers
from guitar.position.set.set_of_guitar_positions import SetOfGuitarPositions
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.frozenlist import FrozenList


def _generate_scale(starting_note: GuitarPositionWithFingers, relative_intervals: FrozenList[ChromaticInterval]):
    if not relative_intervals:
        yield FrozenList([starting_note])
        return
    relative_interval, remaining_relative_intervals = relative_intervals.head_tail()
    for next_note in starting_note.positions_for_interval(interval=relative_interval):
        for notes_for_remaining_intervals in _generate_scale(next_note, remaining_relative_intervals):
            yield FrozenList([starting_note, *notes_for_remaining_intervals])

def generate_scale(starting_note: GuitarPositionWithFingers, relative_intervals: FrozenList[ChromaticInterval]):
    poss = _generate_scale(starting_note, relative_intervals)
    return SetOfGuitarPositions.make(positions = poss)