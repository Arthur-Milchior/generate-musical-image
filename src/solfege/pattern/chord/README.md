# Chord patterns

`ChordPattern` ([chord_pattern.py](chord_pattern.py)) is a `SolfegePattern` (see [../README.md](../README.md) for
the shared mechanics) whose shape is a `_full_interval_list: IntervalList` of notes stacked from a root, e.g.
major triad = `[(4, 2), (7, 4)]`. The actual catalog of chords (the instances used elsewhere in the app) lives in
[chord_patterns.py](chord_patterns.py) — that's the file to edit to add a new chord type.

## What happens automatically when you `.make()` a chord

`ChordPattern.__post_init__` calls `self.inversions(record=self.record)`, which builds an `InversionPattern`
(see [../inversion/README.md](../inversion/README.md)) for **every** note of the chord as potential bass, and —
since `record` defaults to `True` — registers all of them immediately. This means every `ChordPattern.make(...)`
call at module import time has real side effects (populating `ChordPattern.name_to_pattern`/`all_patterns` and
the interval-list record keepers), not just constructing a value object.

Two consequences to know before adding a chord:
1. **One octave, hard limit.** The record keepers backing chords require every interval, in every inversion, to
   stay strictly under one octave from that inversion's bass note (`is_in_base_octave(accepting_octave=False)`).
   A chord whose top note reaches a compound interval (9th, 11th, 13th...) cannot be registered as-is. See
   [../multi_octave_patterns.md](../multi_octave_patterns.md) for the reduction rule this codebase uses instead
   (fold compound intervals back under an octave; keep the traditional name only in `notation`/`description`).
2. **No two notes may share a diatonic index.** Unlike scales, a chord whose two notes have the same diatonic
   index (e.g. a "split third" with both `(3, 2)` and `(4, 2)`) will pass construction but blow up inside
   `interval_list_of_inversion` for whichever inversion puts the lower of the two as the new bass — it produces
   a "diminished octave" that fails the base-octave check above. Work around it by respelling one of the two
   notes enharmonically at an adjacent diatonic index (e.g. `(4, 3)`, a diminished fourth, instead of `(4, 2)`,
   a major third) — see the "Mixed third chord" entry in [chord_patterns.py](chord_patterns.py) for a worked
   example.

## `optional_fifth`

If `optional_fifth=True`, the pattern additionally registers a second interval list with the fifth
(`diatonic == 4`) dropped — used for chords like the dominant seventh, where a guitarist/pianist routinely omits
the fifth. `intervals_without_fifth()` / `_index_of_fifth()` implement this; there must be exactly one note at
diatonic index 4 for it to work.

## Arpeggios: chords feeding into the scale catalog

`to_arpeggio_pattern()` turns a chord into a `ScalePattern` (root position, ascending, plus a closing octave) —
this is how [../scale/scale_patterns.py](../scale/scale_patterns.py)'s `chord_patterns_as_scales` is built,
automatically, from every entry in `chord_patterns`. It carries the chord's `source`/`description` over into the
derived scale. If a chord's arpeggio happens to have the exact same interval list as an already-registered scale
(this happens — e.g. the six-nine chord arpeggiated *is* the major pentatonic scale), the scale record keeper
will refuse the duplicate; see the `_chords_without_auto_arpeggio` exclusion set at the top of
[../scale/scale_patterns.py](../scale/scale_patterns.py) for how that's handled (add the chord's alternate name
onto the pre-existing scale instead of registering a second, identical one).
