from typing import List, Optional
from guitar.position.guitar_position import GuitarPosition
from solfege.value.interval.chromatic_interval import ChromaticInterval


increase_fret_limit = 4  # The maximal distance between two note played on the same string.
decreasing_fret_limit = 4  # The maximal distance between the last note played on the string, and the fret on the next string


def scale2Pos(intervals: List[ChromaticInterval], lowest_note_position: GuitarPosition) -> Optional[List[GuitarPosition]]:
    """A list of position, such that the 0-th position is lowest_note_position, and
    the interval between the i-th position's note and the lowest_note_position's
    note is intervals[i].

    Return None if a scale can't be generated.

    """
    poss = [lowest_note_position]
    lastPos = lowest_note_position
    firstFret = lowest_note_position.fret
    for interval in intervals:
        pos = lowest_note_position.positions_for_interval_with_restrictions(interval, fret_min=max(lastPos.fret - decreasing_fret_limit, 1),
                          fret_max=firstFret + increase_fret_limit)
        if pos is None:
            return None
        if pos.string != lastPos.string:
            firstFret = pos.fret
        poss.append(pos)
        lastPos = pos
    return poss
