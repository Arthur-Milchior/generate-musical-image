# piano

Generates piano scale/chord/progression scores (as LilyPond-rendered SVGs) and Anki notes, using
[`../../_lily/`](../../_lily/) (the `Lilyable` protocol) and [`../../lily/`](../../lily/) (the newer staff/sheet
layer) for the actual LilyPond rendering.

## Layout

- [`piano_note.py`](piano_note.py): `PianoNote`, a `solfege.value.note.Note` extended with a `finger` (1 =
  thumb, ..., 5 = pinky). This is the unit fingering-generation and scale-rendering code passes around.
- [`fingering_generation/`](fingering_generation/) — the fingering *algorithm*: exhaustively searches legal
  finger assignments for a melody/scale and keeps the lowest-penalty one(s). See its own README.
- [`scales/`](scales/) — the main, working generator: renders every scale/arpeggio pattern, starting on every
  note, in every direction/hand/octave-count combination, using `fingering_generation` to finger each one. See
  its own README.
- [`scale_variant/`](scale_variant/) — a smaller top-level script generating scale pairs a half-tone apart
  (increasing then decreasing back down, in the other key). See its own README.
- [`chord_successions/`](chord_successions/) — intended to generate runs of same-type chords climbing a scale
  (e.g. every triad of the C major scale in order). **Currently non-functional** (its generation code is
  entirely commented out) — see its own README.
- [`progression/`](progression/) — intended to generate full two-hand chord progressions (e.g. ii-V-I) in every
  key/voicing. **Currently non-functional** (entirely commented out) — see its own README.
- [`__main__.py`](__main__.py): entry point for `python3 -m instruments.piano` (see
  [`../../README.md`](../../README.md)) — imports each submodule's `main`, triggering generation as an import
  side effect.
- [`tests.py`](tests.py): commented-out legacy test-running harness, superseded by plain `pytest` discovery.
- [`README`](README) (no `.md` extension, not this file): a stale, pre-reorganization description referencing
  files (`lily.py`, `penalty.py`, `note.py`) that no longer exist at this path — left in place but superseded
  by this `README.md` and the per-submodule READMEs it links to.

## Known issues

Several submodules here are dead code or have pre-existing bugs (not fixed as part of documentation passes,
since fixing them is a behavior change):

- `chord_successions/` and `progression/` are entirely commented out — running them does nothing (or, for
  `progression`, raises `ImportError`).
- `scales/__main__.py` imports `solfege.scale.scale_pattern`, which does not exist (the real module is
  `solfege.pattern.scale.scale_pattern`) — running `python3 -m instruments.piano.scales` currently raises
  `ModuleNotFoundError`. `scales/generate.py`'s `generate_scores` also silently relies on `scale_patterns` being
  registered as a global rather than importing it directly.
- `fingering_generation/generate.py`'s `generate_best_fingering_for_scale` calls a `FingeringSymbol` that isn't
  defined anywhere in the package (only `Fingering` is) — calling it raises `NameError`.

See each submodule's own README for details specific to it.
