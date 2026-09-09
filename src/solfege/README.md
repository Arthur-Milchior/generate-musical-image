# solfege

The music-theory model: notes, intervals, keys, and the chord/scale/inversion *patterns* built from them.
Nothing here draws anything or knows about any particular instrument — that's [`../instruments/`](../instruments/README.md);
this package only knows about music theory.

## Layout

- [`value/`](value/README.md) — the base values everything else is built from: notes (`value/note/`),
  intervals (`value/interval/`), and key signatures (`value/key/`), each in chromatic-only, diatonic-only, or
  chromatic+diatonic-pair flavors.
- [`pattern/`](pattern/README.md) — note-less *shapes* (a `ChordPattern`, `ScalePattern`, `InversionPattern`,
  or single-`IntervalPattern`), e.g. "Major triad" as opposed to "C major triad". See
  [`pattern/multi_octave_patterns.md`](pattern/multi_octave_patterns.md) for why patterns are capped at one
  octave.
- [`pattern_instantiation/`](pattern_instantiation/README.md) — anchors a `pattern/` shape to a concrete
  lowest note, producing the actual playable object (a `Chord`, `Scale`, or `InversionInstantiation`, and
  their chromatic-only counterparts).
- [`list_order.py`](list_order.py) — the `ListOrder` enum (`INCREASING`/`DECREASING`/`NOT`) used by
  `value/note/set/`'s note lists and `pattern_instantiation/` to track/enforce how a list of notes is sorted.

`__main__.py` and `tests.py` at the top level are empty/stale (an empty file, and a file of commented-out
imports referencing module names from before the current `value`/`pattern`/`pattern_instantiation` layout),
and `generate.py~` is a leftover editor backup — none of the three are part of the current module structure.
See [`../README.md`](../README.md) for the repo's actual generator/test entry points.

## Dependencies

`pattern_instantiation` depends on `pattern`, which depends on `value` (specifically `value/note` and
`value/interval`; `value/key` is not used by patterns). Within `value`, `key` depends on `note`, which depends
on `interval` — see [`value/README.md`](value/README.md#dependencies). Where the reverse direction is needed,
the import is deferred to inside a function body to avoid a cycle.
