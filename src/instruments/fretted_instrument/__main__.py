"""`python3 -m instruments.fretted_instrument` entry point.

Note: unlike `generate.py`'s `from ... import *` (which pulls in every generator, including chords and the
bass/ukulele scale generators), this only imports fret-position, note, note-pair, and guitar-scale generation --
each triggers its generation as an import-time side effect. Chord generation and the bass/ukulele scale
generators are not run here; use `generate.py` (or `python3 -m instruments.fretted_instrument.chord`/`.scale`)
for those.
"""

from instruments.fretted_instrument.position import generate
from instruments.fretted_instrument.note import generate_fretted_notes
from instruments.fretted_instrument.pair import generate_fretted_instrument_interval
from instruments.fretted_instrument.scale import generate_guitar