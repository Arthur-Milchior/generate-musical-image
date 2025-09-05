

from guitar.chord.guitar_chord import *


open = GuitarChord.make([OPEN_FRET] * 6)
ones = GuitarChord.make([Fret(1)] * 6)
diag = GuitarChord.make([Fret(i) for i in range(6)])
diag_two = GuitarChord.make([Fret(i+2) for i in range(6)])
C = GuitarChord.make([None, 3, 0, 2, 1, 0])
F = GuitarChord.make([1, 3, 3, 2, 1, 1])