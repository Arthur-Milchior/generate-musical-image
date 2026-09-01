# Design: chords whose real-world span exceeds one octave

Many chords documented on Wikipedia are conventionally described with tones
that reach beyond an octave from the root: a 9th is a compound 2nd (14
semitones), an 11th a compound 4th (17 semitones), a 13th a compound 6th (21
semitones). Some famous individual chords (the Mystic chord, the Psalms
chord, the Petrushka chord...) were voiced by their composers across two or
more octaves, sometimes with specific notes doubled. This document explains
why the current engine cannot store any of that literally, and what we do
instead.

## The constraint is architectural, not cosmetic

`ChordPattern` and `ScalePattern` are not free-form containers: every
instance is registered into a singleton `RecordKeeper` keyed by its interval
content, and that registration enforces "everything fits in one octave":

- `IntervalListToChordPattern.is_key_valid` and
  `ChromaticIntervalListToChordPattern.is_key_valid` both require
  `key.is_in_base_octave()`
  ([chord/interval_list_to_chord_pattern.py:17-18](chord/interval_list_to_chord_pattern.py#L17-L18),
  [chord/chromatic_interval_list_to_chord_pattern.py:17-18](chord/chromatic_interval_list_to_chord_pattern.py#L17-L18)).
- `RecordKeeper.register` / `_get_or_create_recorded_container` /
  `get_recorded_container` all `assert self.is_key_valid(key)`
  ([utils/recording/record_keeper.py](../../utils/recording/record_keeper.py),
  lines 43, 49, 61).
- Every `ChordPattern` records itself **and all of its inversions** at
  construction time, since `record` defaults to `True`
  ([pattern_with_interval_lists.py:52](pattern_with_interval_lists.py#L52)) and
  `ChordPattern.__post_init__` calls `self.inversions(record=self.record)`
  ([chord/chord_pattern.py](chord/chord_pattern.py)).
- `InversionPattern.__post_init__` goes further and asserts, for *every*
  note of *every* inversion, that `interval.is_in_base_octave(accepting_octave=False)`
  ([inversion/inversion_pattern.py](inversion/inversion_pattern.py)) — i.e. strictly under
  12 semitones from that inversion's new lowest note.
- `ScalePattern` is not exempt either:
  `IntervalListToScalePattern.is_key_valid` /
  `ChromaticIntervalListToScalePattern.is_key_valid` require
  `key.is_in_base_octave(accepting_octave=True)`
  ([scale/interval_list_to_scale_pattern.py](scale/interval_list_to_scale_pattern.py),
  [scale/chromatic_interval_list_to_scale_pattern.py](scale/chromatic_interval_list_to_scale_pattern.py)) —
  every note strictly under the octave, except the very last note of the
  scale, which may land *exactly* on the octave.
- On the rendering side, matching a fretted-instrument voicing back to a
  chord pattern explicitly folds notes into one octave first
  (`intervals_frow_lowest_note_in_base_octave()` in
  [instruments/fretted_instrument/position/set/abstract_set_of_fretted_instrument_positions.py:183-189](../../instruments/fretted_instrument/position/set/abstract_set_of_fretted_instrument_positions.py#L183-L189)),
  so even if a >1-octave `ChordPattern` could be constructed, guitar-chord
  lookup would not be able to find it back from a fingering.

So: **any pattern whose highest interval reaches or exceeds one octave from
its lowest note cannot be registered today**, and this is checked well
before any image gets rendered — it fails at pattern-definition time in
[chord/chord_patterns.py](chord/chord_patterns.py)/[scale/scale_patterns.py](scale/scale_patterns.py).

## What we do about it: pitch-class reduction (the default)

For the overwhelming majority of "extended" chords, the thing that actually
matters harmonically is the *set of pitch classes*, not the specific octave
each one happens to sit in. A 6/9 chord voiced "9th above the root" and the
same 6/9 chord voiced with the 9th dropped to a plain 2nd below the 6th are
the same chord in every meaningful sense — the second is just its closest
voicing. So the rule applied throughout [chord/chord_patterns.py](chord/chord_patterns.py) and
[scale/scale_patterns.py](scale/scale_patterns.py) (and already used, before this change, for e.g. the
"Prometheus"/"Mystic chord" scale) is:

> Store every pattern using its **closest-position, octave-reduced**
> intervals (each compound interval brought down by whole octaves — a
> 9th becomes a 2nd, an 11th a 4th, a 13th a 6th — both chromatically and
> diatonically via `Interval.in_base_octave()`), and keep the traditional
> compound-degree name only in `notation` (free text) and `description`
> (prose). Never put a compound interval in `_full_interval_list` /
> `_absolute_intervals`.

Concretely, for the new chords added alongside this document:

- A **6/9 chord** (`1-3-5-6-9`) is stored as `(2,1),(4,2),(7,4),(9,5)` — i.e.
  `1-2-3-5-6` — because the 9th and the 2nd are the same pitch class.
- A **dominant/major/minor 13th chord** is stored with its 13th reduced to a
  6th, e.g. dominant 13th is `(4,2),(7,4),(9,5),(10,6)` (`1-3-5-6-b7`, the
  6th standing in for the 13th). The jazz-specific alterations listed on
  [Thirteenth (interval) § Gallery](https://en.wikipedia.org/wiki/Thirteenth_(interval)#Gallery)
  (♭9, ♯11, ♭5, sus, "add13" vs "13") mostly collapse onto the *same*
  octave-reduced pitch classes once the 9th/11th are omitted (which they
  commonly are in practice — the gallery article itself notes "root, third,
  seventh, and thirteenth are most often included"); rather than invent one
  `ChordPattern` per jazz alteration label, only the three canonical forms
  (dominant/major/minor 13th) are added, and the omitted alterations are
  called out in their `description`.
- This reduction can reveal that a "new" chord is not a new *shape* at all.
  Once collapsed to pitch classes, the **Tristan chord** (traditionally
  described as a bass note plus an augmented 4th, augmented 6th and
  augmented 9th — see [Tristan chord](https://en.wikipedia.org/wiki/Tristan_chord))
  is enharmonically identical to the existing
  `half_diminished_seventh_chord` shape — Wikipedia's own article says as
  much. Likewise the **Psalms chord** (see [Psalms chord](https://en.wikipedia.org/wiki/Psalms_chord))
  collapses to a plain `minor_triad`,
  and the shape used for the **Neapolitan chord** (see [Neapolitan chord](https://en.wikipedia.org/wiki/Neapolitan_chord))
  is a plain `major_triad`
  on a specific (context-dependent, not shape-dependent) scale degree. In
  these cases we do *not* create a duplicate `ChordPattern` with identical
  interval content — we add the extra Wikipedia source and a description
  note to the existing pattern instead. Creating a second `ChordPattern`
  with the exact same shape is technically possible (chords are recorded in
  a plain `list`, not a `SingletonContainer`, so the record keeper would not
  reject it — see `ChordPattern._new_record_keeper` in
  [chord/chord_pattern.py](chord/chord_pattern.py)) but would be pure
  duplication with no behavioural difference, so it is avoided.
- Collections that are genuinely wider than 4 notes once reduced (the
  **Petrushka chord**, see [Petrushka chord](https://en.wikipedia.org/wiki/Petrushka_chord);
  the **Elektra chord**, see [Elektra chord](https://en.wikipedia.org/wiki/Elektra_chord))
  are added as `ScalePattern`s
  instead of `ChordPattern`s, matching the precedent already set by
  "Prometheus"/"Mystic chord", "Whole tone" and "Augmented": in this
  codebase, a harmonic collection wider than a triad-plus-extension is
  modelled as a scale, not a chord, and does not go through
  `ChordPattern.inversions()` at all.

## What we deliberately do *not* try to model

Some of what's actually notable about a specific historical chord is not a
pitch-class set at all — it's the composer's choice of *register and
doubling*. The [Psalms chord](https://en.wikipedia.org/wiki/Psalms_chord)'s real claim to fame is that Stravinsky doubled
the middle note across four octaves and pushed the root and fifth to the
extreme registers, leaving a wide gap in the middle; reduced to pitch
classes it is just E minor. No `_full_interval_list` can represent "this
note doubled four octaves up" — `ChordPattern`/`ScalePattern` have no
concept of doubling or of a note's absolute register at all. For chords like
this, the historically interesting fact is recorded purely as prose in
`description`, on the closest existing pattern (or, if there is no
suitable proxy at all, not modelled in code and left as a comment/aside in
the relevant description instead).

We also deliberately do **not** relax the one-octave constraint at the
architecture level (e.g. by teaching `InversionPattern` to accept wider
spans, or replacing the `RecordKeeper`'s per-note octave check with a
whole-pattern check). Reasons:

1. **No settled musical vocabulary to generate.** Standard chord theory has
   a clear, small, useful notion of "inversions of a triad or seventh
   chord" (bass note moves through the stack). There is no equally settled
   notion of "the second inversion of a spread 13-chord voiced across two
   octaves" — real voicings of extended/wide chords are described by
   register and doubling choices ("drop 2", "drop 3", specific voicings),
   not by a small enumerable set of inversions. Relaxing the constraint
   would mostly generate a combinatorial explosion of inversions nobody
   asks for, for a few rare chords, at real engineering cost (every place
   listed above would need reworking, including the guitar-fingering
   lookup path).
2. **No current consumer needs it.** Every current renderer
   ([instruments/piano](../../instruments/piano/), [instruments/fretted_instrument](../../instruments/fretted_instrument/),
   [instruments/saxophone](../../instruments/saxophone/), [instruments/accordina](../../instruments/accordina/), see
   [instruments/generate.py](../../instruments/generate.py)) draws a pattern within a single
   octave/position; none of them has a notion of "this chord spans two
   octaves, draw it that way."

If a future feature genuinely needs the real, wide voicing of a chord (e.g.
to render the Psalms chord's historical spacing verbatim), the recommended
design is a **new, separate value type** — e.g. a `Voicing` pairing a
`ChordPattern`/`ScalePattern` with an explicit list of octave-offsets (and
optional doubling) per note — that is *not* recorded in the singleton
`RecordKeeper`s and is *not* run through `ChordPattern.inversions()`. That
type is out of scope for now; nothing today needs it, so it is not built
speculatively.

## Summary

| Situation | What we store |
|---|---|
| Compound extension (9th/11th/13th, 6/9, add9…) | `ChordPattern`, octave-reduced to closest position; compound name kept in `notation`/`description` |
| Wide historical voicing that reduces to an existing chord shape (Tristan → half-diminished 7th, Psalms → minor triad, Neapolitan → major triad) | The existing `ChordPattern`, with the extra name/source/description added — no duplicate pattern |
| Wide historical/synthetic collection with more than 4 distinct pitch classes once reduced (Mystic/Prometheus, Petrushka, Elektra) | `ScalePattern`, following the precedent already used for "Whole tone"/"Augmented" |
| The register/doubling itself is the notable thing (Psalms chord's 4-octave-doubled middle note) | Prose only, in `description` — not representable in `_full_interval_list`/`_absolute_intervals` today; would need a future `Voicing` type (not built) |
