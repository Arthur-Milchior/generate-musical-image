# Pattern system

A "pattern" is a shape (a scale, a chord, an interval, an inversion) that is not yet anchored to a
concrete note — e.g. "Major triad" as opposed to "C major triad". This folder is the shared base for
all of them; concrete subtrees are [chord/](chord/), [scale/](scale/), [inversion/](inversion/), and
[../value/interval/interval_pattern.py](../value/interval/interval_pattern.py) (single intervals).

See also [multi_octave_patterns.md](multi_octave_patterns.md) in this folder (why patterns are capped at one
octave) and [../../inheritance.md](../../inheritance.md) (base-class ordering convention used across the
codebase).

## Class hierarchy

`SolfegePattern` ([solfege_pattern.py](solfege_pattern.py)) is the common base, combining:
- `PatternWithName` ([pattern_with_name.py](pattern_with_name.py)): `names` (a `StrFrozenList` of aliases —
  the first is canonical), `notation`, and a per-subclass `name_to_pattern` dict / `all_patterns` list used
  by `get_from_name()` / `get_all_instances()`. Registering under a name that's already taken raises an
  assertion — this is what catches accidental duplicate imports.
- `PatternWithIntervalLists` ([pattern_with_interval_lists.py](pattern_with_interval_lists.py)): registers the
  pattern's interval list(s) into a `RecordKeeper` (see [../../utils/recording/README.md](../../utils/recording/README.md))
  so it can later be looked up *from* a set of intervals (e.g. "what chord is C-E-G?"). A pattern can expose
  more than one key (e.g. a chord with an optional fifth registers both the full and the fifth-omitted interval
  lists).
- `ClassWithEasyness[int]`: an `easy_key()` used to rank/sort patterns by how "easy" they are (their creation
  order here, via `_pattern_index`).
- `source: StrFrozenList` and `description: str`: added for documentation — a source is normally a Wikipedia
  URL (or a few); the constructor accepts a bare string too (it gets wrapped into a singleton list).
  `description` is free prose explaining what's notable about the pattern (name origin, construction, history).
  HTML is fine in `description` (`notation` already uses `<sup>`/entities elsewhere) — the convention used
  throughout [chord/chord_patterns.py](chord/chord_patterns.py)/[scale/scale_patterns.py](scale/scale_patterns.py)
  is to inline `<a href="...">` links at the natural mention of a concept: link the pattern's own name to its
  primary `source` URL, and link any other concept mentioned in the prose that has its own relevant Wikipedia
  article (a related pattern, a composer, a piece, a theory term) — reusing another pattern's exact `source`
  URL when cross-referencing it by name is an easy way to stay correct without re-verifying the link.

Concrete leaves: `ChordPattern` ([chord/](chord/)), `ScalePattern` ([scale/](scale/)),
`InversionPattern` ([inversion/](inversion/)), `IntervalPattern`
([../value/interval/interval_pattern.py](../value/interval/interval_pattern.py)).

## Construction: never call `__init__` directly

Every one of these classes is a frozen dataclass built through
[`DataClassWithDefaultArgument.make(...)`](../../utils/data_class_with_default_argument.py), not through the
generated `__init__` directly — `make()` is what applies default values and light type coercion (e.g. turning a
plain `[(4, 2), (7, 4)]` list into an `IntervalList`, or a bare string into a singleton `StrFrozenList`).
Definitions read like:

```python
major_triad = ChordPattern.make(names=["Major triad"], notation="M", _full_interval_list=[(4, 2), (7, 4)],
                                 interval_for_signature=nor_flat_nor_sharp, source="https://en.wikipedia.org/wiki/Major_chord",
                                 description="...")
```

Each class contributes to two classmethods that a subclass overrides and chains via `super()`:
- `_default_arguments_for_constructor(cls, args, kwargs)`: returns a dict of defaults.
- `_clean_arguments_for_constructor(cls, args, kwargs)`: coerces/validates values already passed in.

**Gotcha (bit us once, see git history around "interval notation"):** because these are real dataclasses,
Python still enforces "no field without a default may follow a field with one" across the *entire* MRO-flattened
field list — and a field declared without a default in a base class but given `= True`/`= False` in a
subclass counts as having a default at that field's *original* position. Concretely, do **not** write
`some_field: bool = True` directly on a dataclass field in a subclass of `SolfegePattern` unless you're sure
nothing declared later (in any subclass, anywhere) lacks a default. Instead give it a default through
`_default_arguments_for_constructor` like every other field. `_is_chord_pattern` used to violate this and broke
dataclass construction for the whole `solfege` package under Python 3.14.

## Interval spelling: `(chromatic, diatonic)` pairs

Intervals inside a pattern are `Interval.make(chromatic, diatonic)` pairs, written as plain tuples in pattern
definitions, e.g. `(4, 2)` = major third (4 semitones, 3rd scale degree, diatonic index 2 since it's 0-based).
A bare int (`2` instead of `(2, 1)`) is shorthand for "one diatonic scale-degree step of this many semitones" —
used for ordinary scale steps. Diatonic index *can* repeat within one pattern (e.g. a chromatic passing tone
uses the same diatonic index as its neighbour, diatonic delta 0) — that's fine for `ScalePattern`. It is
**not** safe for `ChordPattern`: two notes sharing a diatonic index can produce an invalid "diminished octave"
once `ChordPattern.inversion()` recomputes intervals relative to a different bass note (see
[chord/README.md](chord/README.md)).
