from instruments.fretted_instrument.chord.chord_on_fretted_instrument import *
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar

def _make(l):
    return ChordOnFrettedInstrument.make(Guitar, l)

def fret(value):
    return Guitar.fret(value)

open = _make([fret(0)] * 6)
ones = _make([fret(1)] * 6)
diag = _make([fret(i) for i in range(6)])
diag_two = _make([fret(i+2) for i in range(6)])
C4M_ = _make([None, 3, 2, 0, 1, None])
C4M = _make([None, 3, 2, 0, 1, 0])
F4M = _make([1, 3, 3, 2, 1, 1])