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

## Guitar (and other physical instruments) still need extensions voiced high

Reducing a chord's *stored* intervals to one octave does not mean a real fingering has to squeeze all its notes
into one octave too — a guitar chord routinely spans two or three octaves across six strings, and for a chord
like a 6/9 or a thirteenth the 9th/13th should still sound *above* the root/3rd/5th/7th, exactly like it would
on a real fingering, even though `ChordPattern._full_interval_list` only stores it as a plain 2nd/6th.

`ChordPattern` has a second, optional field for this: `extension_intervals` — the subset of
`_full_interval_list`'s (still octave-reduced) intervals that represent a compound extension. It's set on
`six_nine_chord`, `minor_six_nine_chord` (their 9th) and the three thirteenth chords (their 13th, reduced to a
6th) in [chord/chord_patterns.py](chord/chord_patterns.py) — not on `added_ninth_chord` (whose Wikipedia
source itself treats "add2, voiced low" and "add9, voiced high" as the same shape, so it's deliberately left
unconstrained).

`InversionPattern.voicing_respects_extensions(tonic, physical_notes)` (see
[inversion/inversion_pattern.py](inversion/inversion_pattern.py)) checks a *concrete, physical* voicing (real
`ChromaticNote`s, not octave-reduced) against this: every note playing an extension tone must have a higher
pitch than every note playing a non-extension tone. The guitar chord generator
([instruments/fretted_instrument/chord/generate_chords.py](../../instruments/fretted_instrument/chord/generate_chords.py))
already brute-force-enumerates every fret combination and matches each one's *reduced* pitch-class set back to
a registered `InversionPattern` to identify it (see `intervals_frow_lowest_note_in_base_octave()` on
[instruments/fretted_instrument/position/set/abstract_set_of_fretted_instrument_positions.py](../../instruments/fretted_instrument/position/set/abstract_set_of_fretted_instrument_positions.py));
it now also checks the *un-reduced* physical fingering against `voicing_respects_extensions` and skips any
fingering that fails it, so only correctly-voiced fingerings of these chords ever get generated.

This is deliberately narrow: it's a yes/no filter on voicings the brute-force search already produces, not a
general "chords wider than an octave" feature. It doesn't change what `_full_interval_list` stores, doesn't
touch the `RecordKeeper`/`InversionPattern` octave assertions described above, and doesn't (yet) do anything for
`instruments/piano` or the other instrument packages, which don't enumerate physical voicings the same way.

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
2. **No current consumer needs the full generality.** Guitar chord generation does need *some* notion that a
   9th/13th should be voiced above the rest (see "Guitar (and other physical instruments) still need extensions
   voiced high" above) — but that's satisfied by a per-chord extension marker plus a filter over voicings the
   brute-force fretted-instrument search already enumerates, not by relaxing the stored pattern's span. Nothing
   asks for the fuller thing an `InversionPattern`-level relaxation would provide — a small, settled notion of
   "the second inversion of a spread 13-chord" — or for register/doubling (point 1 above; the Psalms chord's
   4-octave-doubled middle note is still not representable). [instruments/piano](../../instruments/piano/),
   [instruments/saxophone](../../instruments/saxophone/) and [instruments/accordina](../../instruments/accordina/)
   (see [instruments/generate.py](../../instruments/generate.py)) don't enumerate physical voicings the way the
   fretted-instrument code does, so they have no place to plug an equivalent check into yet.

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
| The extension must sound above the rest in a real, physical voicing (6/9 and thirteenth chords) | `ChordPattern.extension_intervals` marks which reduced tones are extensions; `InversionPattern.voicing_respects_extensions(...)` checks a concrete un-reduced voicing against it; the fretted-instrument chord generator filters on it |
| Wide historical voicing that reduces to an existing chord shape (Tristan → half-diminished 7th, Psalms → minor triad, Neapolitan → major triad) | The existing `ChordPattern`, with the extra name/source/description added — no duplicate pattern |
| Wide historical/synthetic collection with more than 4 distinct pitch classes once reduced (Mystic/Prometheus, Petrushka, Elektra) | `ScalePattern`, following the precedent already used for "Whole tone"/"Augmented" |
| The register/doubling itself is the notable thing (Psalms chord's 4-octave-doubled middle note) | Prose only, in `description` — not representable in `_full_interval_list`/`_absolute_intervals` today; would need a future `Voicing` type (not built) |
