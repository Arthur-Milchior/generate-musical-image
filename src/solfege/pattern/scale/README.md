# Scale patterns

`ScalePattern` ([scale_pattern.py](scale_pattern.py)) is both a `SolfegePattern` (see [../README.md](../README.md))
and an `IntervalList`, so a scale *is* its interval list — there's no separate `_full_interval_list` field like
`ChordPattern` has. The catalog of scales actually used elsewhere in the app is
[scale_patterns.py](scale_patterns.py) — that's the file to edit to add a new scale. Most entries there are built
with `ScalePattern.make_relative(relative_intervals=[...], ...)`, giving the *steps* between successive notes
rather than each note's distance from the root (`make` + `_full_interval_list`/`_absolute_intervals` is used
when you already have absolute values, e.g. from a chord's `to_arpeggio_pattern()`).

## Uniqueness: scales are a singleton-per-shape registry

Unlike `ChordPattern` (which records into a plain `list`, so several differently-named chords can share one
shape), the scale record keepers use a `SingletonContainer` with `SameKeyBehavior.IMPOSSIBLE` (see
[../../../utils/recording/README.md](../../../utils/recording/README.md)): **two `ScalePattern`s with the exact
same interval list cannot both be registered.** If your new scale turns out to have the same shape as an
existing one, don't create a second pattern — add the new name to the existing entry's `names` list instead
(there are many examples of this already: `"Locrian"` / `"Greek Mixolydian tonos (diatonic genus)"`,
`"Prometheus"` / `"Mystic chord"`, etc.). [scale_patterns.py](scale_patterns.py)'s `_chords_without_auto_arpeggio`
set/comment documents one instance of this happening with an auto-generated chord arpeggio.

## One octave, hard limit — but a softer one than chords

Every absolute interval in a scale must land strictly under one octave, **except the very last note**, which
may land exactly on the octave (`is_in_base_octave(accepting_octave=True)`; see
[../multi_octave_patterns.md](../multi_octave_patterns.md)). That's why a normal 7-note scale's
`relative_intervals` sums to a diatonic step of 7 and a chromatic step of 12 by the end. Scales genuinely wider
than an octave in their "real" form (Scriabin's Mystic chord, the Petrushka and Elektra chords) are stored here
collapsed to their pitch-class set within one octave — see
[../multi_octave_patterns.md](../multi_octave_patterns.md) for why, and the "Petrushka chord"/"Elektra chord"
entries for worked examples of picking a diatonic spelling for an invented/synthetic collection (there's no
canonical staff notation to defer to; any strictly-increasing, sum-to-7-diatonic-steps spelling that reaches
exactly the octave is acceptable).

Unlike `ChordPattern`, two notes in a scale *can* share a diatonic index (e.g. `blues`'s `(1, 0, "BN")` passing
tone, or the `"Two-semitone tritone"`/`"Augmented"` symmetric scales) — scales don't get auto-inverted the way
chords do, so the diminished-octave problem described in [../chord/README.md](../chord/README.md) doesn't apply
here.

## `_descending` and `role_maker`

- `_descending`: an optional different `ScalePattern` to use when playing the scale downward (its main real use
  is melodic minor, whose descending form is the natural minor).
- `role_maker`: assigns an `IntervalRole` per step index instead of leaving it to be inferred from the interval
  itself — used for symmetric/non-diatonic scales (whole tone, chromatic) where degree names like "3rd"/"5th"
  don't map cleanly.
