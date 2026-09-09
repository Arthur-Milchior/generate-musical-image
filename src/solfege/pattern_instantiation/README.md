# Pattern instantiation

Where [`solfege/pattern/`](../pattern/README.md) defines note-less *shapes* (a `ChordPattern`, `ScalePattern`,
`InversionPattern` -- "Major triad", not "C major triad"), this package anchors one of those shapes to a
concrete lowest note, producing the actual playable object: a chord, a scale, or a specific inversion starting
on a specific note. Concrete subtrees are [chord/](chord/), [scale/](scale/), [inversion/](inversion/); there is
no `interval/` counterpart here because a bare `IntervalPattern` doesn't need its own instantiation type.

## Class hierarchy

[`pattern_instantiation.py`](pattern_instantiation.py)'s `AbstractPatternInstantiation` is the common base: a
frozen dataclass holding just `pattern` (the note-less pattern) and `lowest_note` (the concrete note it starts
on), plus a handful of `ClassVar`s each concrete subtree fixes (`pattern_type`, `note_type`, `interval_type`,
`interval_list_type`, `note_list_type`) so `__post_init__` can type-check `pattern`/`lowest_note` and
`get_notes()` knows which frozen-list class to build. `lowest_note` must sit in the base octave; call
`add_octave(n)` afterwards to shift the whole thing.

Two abstract subclasses split what "note" and "interval" mean, orthogonally to *which* pattern is being
instantiated:
- [`abstract_pair_instantiation.py`](abstract_pair_instantiation.py)'s `AbstractPairInstantiation`: notes and
  intervals carry both diatonic and chromatic information (`Note`/`Interval`) -- this is the "normal" case,
  e.g. `Chord`, `Scale`, `InversionInstantiation`.
- [`abstract_chromatic_instantiation.py`](abstract_chromatic_instantiation.py)'s `AbstractChromaticInstantiation`:
  notes and intervals are chromatic-only (`ChromaticNote`/`ChromaticInterval`), with no diatonic spelling --
  e.g. `ChromaticChord`, `ChromaticScale`, `ChromaticInversionInstantiation`. Every diatonic+chromatic class
  exposes `get_chromatic_instantiation()`, which builds its chromatic-only counterpart (named via
  `chromatic_instantiation_type`) anchored on `lowest_note.get_chromatic()`.

Each concrete subtree then crosses these two splits with its own pattern type:
- [chord/](chord/README.md): `AbstractChord` (pattern type `ChordPattern`) -> `Chord` / `ChromaticChord`.
- [scale/](scale/README.md): `AbstractScale` (pattern type `ScalePattern`) -> `Scale` / `ChromaticScale`.
- [inversion/](inversion/README.md): `AbstractInversionInstantiation` (pattern type `InversionPattern`) ->
  `InversionInstantiation` / `ChromaticInversionInstantiation`.

## Getting from a pattern to its instantiation

`PatternWithIntervalLists.get_instantiation(lowest_note)` / `get_chromatic_instantiation(lowest_chromatic_note)`
(see [`../pattern/pattern_with_interval_lists.py`](../pattern/pattern_with_interval_lists.py)) are the normal
entry points: they look up the right instantiation class via `_get_instantiation_type()`, which every concrete
pattern class (`ChordPattern`, `ScalePattern`, `InversionPattern`) implements. This is also usable the other
way around: constructing a `Chord`/`Scale`/`InversionInstantiation` directly (`Chord.make(pattern, lowest_note)`)
is how e.g. [`instruments/`](../../instruments/) code turns "this pattern, on this note" into notes to draw.

## `get_notes()`

`AbstractPatternInstantiation.get_notes()` walks `get_absolute_intervals()` (from-the-root intervals) and adds
each to `lowest_note`, producing a strictly increasing note list. [scale/](scale/README.md) overrides this
(`AbstractScale.get_notes()`) to instead walk the pattern's *relative* steps, since a scale can span several
octaves and/or run in either direction -- something a single pass over one absolute interval list can't express.
