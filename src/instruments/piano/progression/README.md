# progression

Intended to generate scores and Anki notes for full harmonic *chord progressions* (e.g. ii-V-I) played with
both hands, in every key and in several voicings — as opposed to a run of same-type chords up a scale (see
[`../chord_successions/`](../chord_successions/)) or a single-hand melodic scale (see [`../scales/`](../scales/)).

## Status

Currently **non-functional**: `chord_progression.py`, `generate.py`, `pattern.py` and `progressions_in_C.py`
are entirely commented out (a work in progress). What they were meant to provide:

- `pattern.py` — `NamedIntervalsPattern`/`ChordProgressionPattern`: a progression expressed as intervals
  relative to a key, so it can be transposed by adding a `Note`.
- `chord_progression.py` — `TwoHandsChord`/`ChordProgression`: the transposed, concrete result (actual notes
  for each hand), renderable to LilyPond.
- `progressions_in_C.py` — the actual data: the ii-V-I progression in C, in four different voicings
  (which chord tone is on top: third-and-seventh, seventh-and-third, etc.).
- `generate.py` — `progressions`/`progressions_for_pattern`/`progression_for_pattern_tonic`: for every
  progression pattern and every key, render the first chord alone and the full progression, and produce the
  corresponding Anki CSV line.

`main.py` is the would-be entry point: it imports `progressions` from `generate.py`, which does not currently
exist there (the whole module is commented out), so running `python3 -m instruments.piano.progression` (via
`__main__.py`) fails with an `ImportError` — a pre-existing bug, see [`../README.md`](../README.md)'s "Known
issues". `test_generate.py`/`test_pattern.py`/`tests.py` are commented-out or no-op test harnesses for the same
code.
