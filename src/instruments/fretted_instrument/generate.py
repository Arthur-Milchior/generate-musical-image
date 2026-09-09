"""Entry point that runs every fretted-instrument generator (notes, note pairs, fret positions, scales, chords).

Each imported module runs its generation as a side effect of being imported (they call their `generate_*()`/
`generate_instruments()` function, or run generation code, at module scope), so importing `*` from all of them
here is enough to regenerate every fretted-instrument Anki asset. Imported by `instruments/generate.py` (the
cross-instrument generation entry point) -- note this is distinct from, and more complete than, this package's
own `__main__.py`, which only wires up a subset of these generators (see its docstring).
"""

from instruments.fretted_instrument.note.generate_fretted_notes import *
from instruments.fretted_instrument.pair.generate_fretted_instrument_interval import *
from instruments.fretted_instrument.position.generate import *
from instruments.fretted_instrument.scale.generate_scales import *
from instruments.fretted_instrument.chord.generate_chords import *
