# Inversion patterns

`InversionPattern` ([inversion_pattern.py](inversion_pattern.py)) represents one inversion of a `ChordPattern`
(see [../chord/README.md](../chord/README.md)) — the same set of notes with a different one as the bass. You
normally don't construct these directly: `ChordPattern.__post_init__` creates and registers one per note
automatically whenever a chord is `.make()`'d with `record=True` (the default), via `ChordPattern.inversions()` /
`ChordPattern.inversion(n)` → `interval_list_of_inversion(n)`.

## Why this is the class that actually enforces "one octave"

`InversionPattern.__post_init__` asserts, for every note of every inversion's interval list:

```python
assert interval.is_in_base_octave(accepting_octave=False)
```

i.e. strictly under 12 semitones from *that inversion's* bass note. This is stricter than the record keeper
check on the chord's root position alone, and it's the actual mechanism that makes it impossible to register a
`ChordPattern` with a compound interval (9th, 11th, 13th...) even in principle — some inversion of it will
always push a note to or past the octave. See [../multi_octave_patterns.md](../multi_octave_patterns.md) for the
reduction rule used instead, and [../chord/README.md](../chord/README.md) for the related "no two notes may
share a diatonic index" pitfall (which manifests as a failure *here*, inside `interval_list_of_inversion`, not
at the point where the chord itself is declared).

## Fields

- `inversion`: 0 = root position, 1 = first inversion, etc.
- `base`: the `ChordPattern` this is an inversion of.
- `fifth_omitted`: whether this specific inversion has the fifth dropped (only meaningful when
  `base.optional_fifth`).
- `tonic_minus_lowest_note`: lets you recover the original tonic from a concrete lowest note
  (`get_tonic(lowest_note)`), since the "root" of an inversion isn't its lowest sounding note.
