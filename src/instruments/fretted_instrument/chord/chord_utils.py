"""Brute-force enumeration of chord fingerings: every combination of one fret (from a given `Frets` range, or
not-played) per string of an instrument."""

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


def enumerate_frets(instrument: FrettedInstrument, frets: Frets, strings: Optional[Strings]= None) -> Generator[SetOfPositionOnFrettedInstrument]:
    """Recursively generate every mapping from each of `strings` (defaulting to all of `instrument`'s strings) to
    one of the frets allowed by `frets` -- i.e. the cartesian product of `frets` across `strings`, each
    combination returned as a `SetOfPositionOnFrettedInstrument`. Yields nothing if `frets.is_contradiction()`."""
    assert_typing(instrument, FrettedInstrument)
    assert_typing(frets, Frets)
    if strings is None:
        strings = instrument.strings()
    assert_typing(strings, Strings)
    s_ss = strings.pop()
    if s_ss is None:
        """There is no string to play at all. End case of the recursion."""
        yield empty_set_of_position(instrument, absolute=frets.absolute)
        return
    if frets.is_contradiction():
        return
    string, strings = s_ss
    for set_of_fretted_instrument_position in enumerate_frets(instrument, strings=strings, frets=frets):
        for fret in frets:
            fretted_instrument_position = PositionOnFrettedInstrument(string, fret)
            yield set_of_fretted_instrument_position.add(fretted_instrument_position)

def enumerate_fretted_instrument_chords(instrument: FrettedInstrument, frets: Optional[Frets] = None) ->Generator[ChordOnFrettedInstrument]:
    """Wrap `enumerate_frets` to yield every fingering as a `ChordOnFrettedInstrument` rather than a generic
    `SetOfPositionOnFrettedInstrument`, using `frets.absolute` for the chord's absolute/transposable-ness."""
    assert_typing(instrument, FrettedInstrument)
    for fret in enumerate_frets(instrument, frets = frets):
        yield ChordOnFrettedInstrument(fret.positions, absolute=frets.absolute)
