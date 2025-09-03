from guitar.chord.guitar_chord import GuitarChord
from guitar.position.fret import Fret
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from guitar.position.strings import Strings, strings
from guitar.position.frets import Frets


def enumerate_frets(strings: Strings= strings, frets: Frets=Frets(min_fret=1, max_fret=5, allow_not_played=True, allow_open=True)):
    """Generate a maping from each string to one of the fret."""
    s_ss = strings.pop()
    if s_ss is None:
        yield SetOfGuitarPositions()
        return
    if frets.is_contradiction():
        return
    string, strings = s_ss
    for set_of_guitar_position in enumerate_frets(strings, frets):
        for fret in frets:
            guitar_position = GuitarPosition(string, fret)
            yield set_of_guitar_position.add(guitar_position)

def enumerate_guitar_chords():
    for frets in enumerate_frets():
        yield GuitarChord(frets.positions)
