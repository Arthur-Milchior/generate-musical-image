"""`python3 -m instruments.fretted_instrument.chord` entry point.

Currently broken/stale: `chord.transposable.generate_transposable` no longer exists (the chord-generation code
was reorganized into `generate_chords.py`, which triggers generation as an import-time side effect on its own).
Use `python3 -c "import instruments.fretted_instrument.chord.generate_chords"` or run the whole package via
`generate.py`/the repo-wide entry points instead.
"""

from instruments.fretted_instrument.chord.transposable import generate_transposable