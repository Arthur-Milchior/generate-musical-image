from guitar.chord.guitar_chord import *
from guitar.position.fret.fret import OPEN_FRET


open = GuitarChord.make([OPEN_FRET] * 6)
ones = GuitarChord.make([Fret(1)] * 6)
diag = GuitarChord.make([Fret(i) for i in range(6)])
diag_two = GuitarChord.make([Fret(i+2) for i in range(6)])
C4M_ = GuitarChord.make([None, 3, 2, 0, 1, None])
C4M = GuitarChord.make([None, 3, 2, 0, 1, 0])
F4M = GuitarChord.make([1, 3, 3, 2, 1, 1])