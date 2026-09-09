from instruments.fretted_instrument.chord.chord_on_fretted_instrument import *
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar

def _make(l):
    """Build an absolute `ChordOnFrettedInstrument` on Guitar from a list of fret values/`Fret`s (one per
    string), for use as a shared test fixture."""
    return ChordOnFrettedInstrument.make(Guitar, l, True)

def fret(value):
    """Build an absolute `Fret` from `value` (or the not-played fret when `value` is `None`)."""
    return Fret.make(value, absolute=True)

entirely_open_chord = _make([fret(0)] * 6)
ones = _make([fret(1)] * 6)
diag = _make([fret(i) for i in range(6)])
diag_two = _make([fret(i+2) for i in range(6)])
C4M_ = _make([None, 3, 2, 0, 1, None])
C4M = _make([None, 3, 2, 0, 1, 0])
F4M = _make([1, 3, 3, 2, 1, 1])
A4M_high_G = _make([None, 0, 2, 2, 2, 5]) 
A4Mt = _make([5, 4, 2, 2, 2, None])  