# Chord instantiation

Anchors a [`ChordPattern`](../../pattern/chord/README.md) to a concrete lowest note. See
[../README.md](../README.md) for the shared `AbstractPatternInstantiation` mechanics and the
diatonic+chromatic vs. chromatic-only split this folder plugs into.

- [`abstract_chord.py`](abstract_chord.py)'s `AbstractChord`: fixes `pattern_type = ChordPattern`; shared by
  both concrete classes below.
- [`chord.py`](chord.py)'s `Chord`: a `ChordPattern` anchored on a concrete (diatonic+chromatic) `Note` root --
  e.g. "C major triad". `names()`/`notation()` prefix the note's spelled name/notation onto the pattern's own
  (e.g. "C" + "Major triad", "C" + "M").
- [`chromatic_chord.py`](chromatic_chord.py)'s `ChromaticChord`: the same, anchored on a chromatic-only root.
  It has no diatonic spelling of its own, so `names()`/`notation()` pick one (`_get_chord()`, via
  `Note.from_chromatic`) and delegate to `Chord`.

Note: `Chord.names()` builds each note's spelled name as a one-element Python `set` before interpolating it
into the returned string -- a pre-existing bug that leaves the set's braces/quoting in the output (e.g.
`"{'C'} Major triad"` instead of `"C Major triad"`); not fixed here.

Since a `ChordPattern` registers an `InversionPattern` for every one of its notes as potential bass (see
[../../pattern/chord/README.md](../../pattern/chord/README.md)), instantiating a specific inversion on a note
goes through [../inversion/](../inversion/README.md) instead of this folder -- `Chord` only ever represents
root position.
