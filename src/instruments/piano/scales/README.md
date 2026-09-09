# scales

The main, working piano generator: renders every scale/arpeggio pattern, starting on every note (one
representative per set of enharmonic keys), for 1 and 2 octaves, in all four directions (increasing,
decreasing, increasing-then-decreasing, decreasing-then-increasing), for left hand, right hand, and both hands
together — as SVG scores plus Anki CSV entries and a browsable HTML index.

## Files

- [`fingering.py`](fingering.py): `Fingering` — an immutable finger assignment for one octave of a scale (which
  finger plays each scale degree, plus the tonic's two possible extremity fingers). `from_scale()` builds one
  from an already-fingered `PianoNote` sequence (see [`../fingering_generation/`](../fingering_generation/) for
  how that sequence is computed); `generate()` applies a `Fingering` back onto a fresh scale starting on an
  arbitrary note, for however many octaves are needed.
- [`generate.py`](generate.py): the actual score-generation pipeline, layered from the bottom up:
  `generate_fingering()` (best fingering for one octave, one hand) →
  `generate_score_fixed_pattern_first_note_direction_number_of_octaves()` (renders left/right/both-hands scores
  for one already-fingered direction) → `generate_score_fixed_pattern_first_note()` (all octave-counts and
  directions for one starting note, writes that note's `index.html`) →
  `generate_score_fixed_pattern()` (every enharmonic starting note for one scale pattern, writes that pattern's
  `index.html`/`anki.csv`) → `generate_scores()`, the top-level entry point, iterating every scale pattern and
  writing the overall `index.html`/`about.html`/`anki.csv`/`cant_exists.txt`/`too_big_alterations.txt`.
  `MissingFingering` records a (scale pattern, note, hand) for which no acceptable fingering exists (written to
  `cant_exists.txt`); `TooBigAlterationException` is caught per starting note when a note in that key would need
  too many sharps/flats to notate (written to `too_big_alterations.txt`).
- [`main.py`](main.py) / [`__main__.py`](__main__.py): entry point for `python3 -m instruments.piano.scales`.
  **Currently broken**: `__main__.py` also imports `solfege.scale.scale_pattern`, which doesn't exist (the real
  module is `solfege.pattern.scale.scale_pattern`), so running this raises `ModuleNotFoundError` — a
  pre-existing bug, not fixed here (see [`../README.md`](../README.md)).
- [`test_fingering.py`](test_fingering.py), [`tests.py`](tests.py): tests for `Fingering` and the generation
  pipeline.

Depends on [`../fingering_generation/`](../fingering_generation/) for the fingering search, and on
[`../../../_lily/`](../../../_lily/)'s `Lilyable` (via `lilypond_code_for_one_hand`/`lilypond_code_for_two_hands`)
for rendering.
