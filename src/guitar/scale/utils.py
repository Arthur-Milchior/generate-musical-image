from typing import List
from src.guitar.position.guitar_position import GuitarPosition
from src.solfege.interval.chromatic import ChromaticInterval


increase_fret_limit = 4  # The maximal distance between two note played on the same string.
decreasing_fret_limit = 4  # The maximal distance between the last note played on the string, and the fret on the next string


def scale2Pos(intervals: List[ChromaticInterval], lowest_note_position: GuitarPosition):
    """A list of position, such that the 0-th position is lowest_note_position, and
    the interval between the i-th position's note and the lowest_note_position's
    note is intervals[i].

    """
    poss = [lowest_note_position]
    lastPos = lowest_note_position
    firstFret = lowest_note_position.fret
    for interval in intervals:
        pos = lowest_note_position.add(interval, min=max(lastPos.fret - decreasing_fret_limit, 1),
                          max=firstFret + increase_fret_limit)
        if pos is None:
            return False
        if pos.string != lastPos.string:
            firstFret = pos.fret
        poss.append(pos)
        lastPos = pos
    return poss
