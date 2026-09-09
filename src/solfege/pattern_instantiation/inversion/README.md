# Inversion instantiation

Anchors an [`InversionPattern`](../../pattern/inversion/README.md) -- one inversion of a `ChordPattern` -- to a
concrete lowest note (the note that becomes the new bass). See [../README.md](../README.md) for the shared
`AbstractPatternInstantiation` mechanics and the diatonic+chromatic vs. chromatic-only split this folder plugs
into.

- [`abstract_inversion.py`](abstract_inversion.py)'s `AbstractInversionInstantiation`: fixes
  `pattern_type = InversionPattern`; shared by both concrete classes below.
- [`inversion_instantiation.py`](inversion_instantiation.py)'s `InversionInstantiation`: an `InversionPattern`
  anchored on a concrete (diatonic+chromatic) `Note` bass -- e.g. "C major triad, first inversion (E in the
  bass)". `get_tonic()` recovers the underlying chord's tonic (not this inversion's bass note) via
  `pattern.tonic_minus_lowest_note`; `_get_chord()` builds the corresponding root-position `Chord` (see
  [../chord/README.md](../chord/README.md)) from that tonic, which `names()`/`notation()` then delegate to,
  appending `"over <bass note>"` / `"/<bass note>"` for any inversion other than root position.
- [`chromatic_inversion_instantiation.py`](chromatic_inversion_instantiation.py)'s
  `ChromaticInversionInstantiation`: the same, anchored on a chromatic-only bass note. `_get_inversion()` picks
  a concrete diatonic spelling for `lowest_note` (`best_enharmonic_starting_note`, re-normalized into the base
  octave since respelling can push it back out -- e.g. `ChromaticNote(11)` can respell to `Note(11, 7)`) and
  delegates to `InversionInstantiation`.

This is also the class that a fretted-instrument voicing check reads from: `InversionPattern.
voicing_respects_extensions()` (see [../../pattern/chord/README.md](../../pattern/chord/README.md)'s
`extension_intervals` section) is called against the pattern these instantiations wrap, not against the
instantiation itself.
