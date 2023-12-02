increase_fret_limit = 4  # The maximal distance between two note played on the same string.
decreasing_fret_limit = 4  # The maximal distance between the last note played on the string, and the fret on the next string


def scale2Pos(intervals, basePos):
    """A list of position, such that the 0-th position is basePos, and
    the interval between the i-th position's note and the basePos's
    note is intervals[i].

    """
    poss = [basePos]
    lastPos = basePos
    firstFret = basePos.fret
    for interval in intervals:
        pos = basePos.add(interval, min=max(lastPos.fret - decreasing_fret_limit, 1),
                          max=firstFret + increase_fret_limit)
        if pos is None:
            return False
        if pos.string != lastPos.string:
            firstFret = pos.fret
        poss.append(pos)
        lastPos = pos
    return poss
