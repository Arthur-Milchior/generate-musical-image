# chord_successions

Intended to generate scores and Anki notes for *successions of same-type chords climbing a scale* — e.g. "play
the triad built on every degree of the C major scale, in order" — as opposed to a single harmonic cadence (see
[`../progression/`](../progression/)) or a single melodic scale (see [`../scales/`](../scales/)).

## Status

Currently **non-functional**: every module except `__init__.py`/`__main__.py` (both empty) is entirely
commented out. `generate.py` holds the (commented) generation logic:

- `ChordPattern` — an interval skeleton for one chord (`triad`, `seventh`).
- `chord_from_scale_pattern_and_position_key` / `chord_succession_from_scale_pattern_and_position_key` — build
  one chord, resp. a run of chords, from a `Scale` and a `ChordPattern`.
- `succession_for_key_pattern` / `successions_for_pattern` / `successions` — assemble the increasing,
  decreasing, "total" (increasing then decreasing) and "inverse" (decreasing then increasing) versions, for
  both hands together and separately, across every key.

`main.py` (also commented, except for a legacy inline `TestChordSuccessionGenerationMain` test class kept as a
comment) is the would-be entry point, calling into `generate.successions`. `test_generate.py`/`tests.py` are
commented-out test harnesses for the same code.

Nothing here is wired into [`../__main__.py`](../__main__.py)'s import list correctly triggering generation,
since importing an empty module is a no-op — see [`../README.md`](../README.md)'s "Known issues" for the
piano package's other pre-existing rough edges.
