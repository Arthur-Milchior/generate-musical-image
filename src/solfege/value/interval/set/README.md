# set

An ordered list of intervals, all relative to a common starting note (the list always starts with the unison)
— this is the shape behind every chord/scale pattern, before it's anchored to a concrete tonic. See
[`../../pattern/README.md`](../../pattern/README.md) for how `ChordPattern`/`ScalePattern` build on top of this.

## Class hierarchy

- [`abstract_interval_list_pattern.py`](abstract_interval_list_pattern.py): `AbstractIntervalListPattern` — the
  common base, generic over the interval type it holds. Two ways to build one:
  - `make_absolute(absolute_intervals, add_implicit_unison=True)`: intervals already relative to the tonic
    (e.g. `[(0,0), (4,2), (7,4)]` for a major triad); a leading unison is inserted if missing.
  - `make_relative(relative_intervals, role_maker=None)`: intervals relative to the *previous* note (e.g.
    `[(4,2), (3,2)]` for the same major triad); `role_maker(index)` can assign each resulting absolute interval
    an [`IntervalRole`](../role/README.md).
  Also provides `relative_intervals()` (inverse of `make_relative`'s input), `from_note(note)` (instantiate the
  pattern starting at a concrete note, returning a `NoteList`/`ChromaticNoteList` — see
  [`../../note/set/README.md`](../../note/set/README.md)), and `in_base_octave()`/`is_in_base_octave()`.
  `__post_init__` enforces the list starts with the unison and is strictly monotonic (increasing or decreasing,
  per the `increasing` field).
- [`interval_list.py`](interval_list.py): `IntervalList` — holds full `Interval`s (chromatic+diatonic). Adds
  `get_chromatic_interval_list()` (drop diatonic spelling), `best_enharmonic_starting_note()` (pick the
  spelling of a chromatic note that gives the "easiest" instantiation), and
  `intervals_from_diatonic()`/`alterations_from_diatonic()` (look up every interval in the list sharing a given
  diatonic degree, and their alterations).
- [`chromatic_interval_list_pattern.py`](chromatic_interval_list_pattern.py): `ChromaticIntervalListPattern` —
  holds `ChromaticInterval`s only, used when diatonic spelling doesn't matter.

## Dependencies

Depends on [`../`](../README.md) (interval types) and, inside function bodies only, on
[`../../note/set/`](../../note/set/README.md) (to avoid an import cycle when instantiating a pattern into
notes).
