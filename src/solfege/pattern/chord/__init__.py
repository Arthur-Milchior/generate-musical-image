"""Package marker for `solfege.pattern.chord`; imports `chord_pattern` so `ChordPattern` is importable via
`solfege.pattern.chord.chord_pattern`. The actual chord catalog lives in `chord_patterns.py` and is not
imported here -- import that module directly to populate it."""

import solfege.pattern.chord.chord_pattern