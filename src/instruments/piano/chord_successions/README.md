# chord_successions

Intended to generate scores and Anki notes for *successions of same-type chords climbing a scale* — e.g. "play
the triad built on every degree of the C major scale, in order" — as opposed to a single harmonic cadence (see
[`../progression/`](../progression/)) or a single melodic scale (see [`../scales/`](../scales/)).

## Status

Currently **non-functional**: `__init__.py`/`__main__.py` are both empty, and `generate.py` (the actual
generation logic) is entirely commented out:

- `ChordPattern` — an interval skeleton for one chord (`triad`, `seventh`).
- `chord_from_scale_pattern_and_position_key` / `chord_succession_from_scale_pattern_and_position_key` — build
  one chord, resp. a run of chords, from a `Scale` and a `ChordPattern`.
- `succession_for_key_pattern` / `successions_for_pattern` / `successions` — assemble the increasing,
  decreasing, "total" (increasing then decreasing) and "inverse" (decreasing then increasing) versions, for
  both hands together and separately, across every key.

`main.py` is **not** commented out (only a legacy inline `TestChordSuccessionGenerationMain` test class at its
end is) — it's live code that calls into `generate.successions` under `if __name__ == '__main__':` — but it
currently fails at its very first import: `from _lily.lily import compile_` (`compile_` no longer exists in
`_lily/lily.py`, a gap shared with a few other pre-existing entry points, see
[`../../../_lily/README.md`](../../../_lily/README.md)). Fixing that would only uncover the next problem:
`generate.successions` doesn't exist either, since `generate.py` is fully commented out. `test_generate.py`/
`tests.py` are commented-out test harnesses for the same code.

Nothing here is wired into [`../__main__.py`](../__main__.py)'s import list correctly triggering generation,
since importing an empty module is a no-op — see [`../README.md`](../README.md)'s "Known issues" for the
piano package's other pre-existing rough edges.
