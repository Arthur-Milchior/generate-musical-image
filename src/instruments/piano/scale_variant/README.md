# scale_variant

A small, standalone top-level script (not organized around `generate.py`/`main.py` layering like
[`../scales/`](../scales/)) that renders, for every scale pattern and every pair of enharmonic keys a half-tone
apart: the scale increasing in one key immediately followed by the same scale decreasing in the other key (and
the symmetric decreasing-then-increasing version) — i.e. "play the scale up, then continue down a half-tone
away", a common practice exercise.

- [`main.py`](main.py): the entire generator. For each scale pattern and each set of enharmonic keys, builds
  the two half-tone-away scales, fingers them together as one continuous melody (via
  `fingering_generation.generate_best_fingering_for_melody`, not the octave-only `generate_best_fingering_for_scale`
  used in `scales/`, since this melody crosses a key change), assembles the two halves into one
  `ListPianoLilyable` (see [`../../../_lily/Lilyable/README.md`](../../../_lily/Lilyable/README.md)), and
  compiles/writes the SVG plus an `anki.csv` entry under `generated/piano/scales_half_tone_off/`.
- [`__main__.py`](__main__.py): entry point for `python3 -m instruments.piano.scale_variant`, just imports
  `main` for its side effect.

Note: `main.py` currently fails to import — its `compile_()` call (`from _lily.lily import compile_`) depends
on a function that no longer exists there; see [`../../../_lily/README.md`](../../../_lily/README.md) for the
shared gap this is part of. Not fixed here.
