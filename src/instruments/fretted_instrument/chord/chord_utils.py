from typing import Generator, Optional
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument
from instruments.fretted_instrument.position.string.strings import Strings
from instruments.fretted_instrument.position.fret.frets import Frets
from utils.util import assert_typing
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import empty_set_of_position


def enumerate_frets(instrument: FrettedInstrument, strings: Optional[Strings]= None, frets: Optional[Frets]=None) -> Generator[SetOfPositionOnFrettedInstrument]:
    """Generate a maping from each string to one of the fret."""
    assert_typing(instrument, FrettedInstrument)
    if strings is None:
        strings = instrument.strings()
    assert_typing(strings, Strings)
    frets = frets if frets else Frets.make(closed_fret_interval=(1, 5), allow_not_played=True, allow_open=True) 
    s_ss = strings.pop()
    if s_ss is None:
        """There is no string to play at all. End case of the recursion."""
        yield empty_set_of_position(instrument)
        return
    if frets.is_contradiction():
        return
    string, strings = s_ss
    for set_of_fretted_instrument_position in enumerate_frets(instrument, strings, frets):
        for fret in frets:
            fretted_instrument_position = PositionOnFrettedInstrument(string, fret)
            yield set_of_fretted_instrument_position.add(fretted_instrument_position)

def enumerate_fretted_instrument_chords(instrument: FrettedInstrument, frets: Optional[Frets] = None) ->Generator[ChordOnFrettedInstrument]:
    assert_typing(instrument, FrettedInstrument)
    for fret in enumerate_frets(instrument, frets = frets):
        yield ChordOnFrettedInstrument(fret.positions)
