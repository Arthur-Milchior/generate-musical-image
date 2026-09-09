"""Package marker for `solfege.pattern`; imports the `chord` and `scale` subpackages so that their base
pattern classes (`ChordPattern`, `ScalePattern`) are importable via `solfege.pattern.chord`/`solfege.pattern.scale`.
Note this does not by itself populate the chord/scale catalogs -- that only happens once
`solfege.pattern.chord.chord_patterns`/`solfege.pattern.scale.scale_patterns` are imported (directly, or
transitively through code that uses the catalogs, e.g. under `instruments/`)."""

import solfege.pattern.chord
import solfege.pattern.scale