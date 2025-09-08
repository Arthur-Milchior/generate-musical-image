from typing import Optional
from guitar.chord.guitar_chord import GuitarChord
from guitar.position.fret.fret import Fret
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set.set_of_guitar_positions import SetOfGuitarPositions
from guitar.position.string.strings import ALL_STRINGS, Strings, strings
from guitar.position.fret.frets import Frets
from utils.util import assert_typing


def enumerate_frets(strings: Strings= ALL_STRINGS, frets: Optional[Frets]=None):
    """Generate a maping from each string to one of the fret."""
    assert_typing(strings, Strings)
    frets = frets if frets else Frets.make(closed_fret_interval=(1, 5), allow_not_played=True, allow_open=True) 
    s_ss = strings.pop()
    if s_ss is None:
        """There is no string to play at all. End case of the recursion."""
        yield SetOfGuitarPositions()
        return
    if frets.is_contradiction():
        return
    string, strings = s_ss
    for set_of_guitar_position in enumerate_frets(strings, frets):
        for fret in frets:
            guitar_position = GuitarPosition(string, fret)
            yield set_of_guitar_position.add(guitar_position)

def enumerate_guitar_chords(frets: Optional[Frets] = None):
    for frets in enumerate_frets(frets = frets):
        yield GuitarChord(frets.positions)
