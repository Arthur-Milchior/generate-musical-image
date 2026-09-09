The actual generation scripts for the accordina, imported (for their side effects) by
[`../generate.py`](../generate.py) in the order: scales, then intervals, then fingerings.

- `accordina_constants.py`: `accordina_folder`, the shared output root (`<generate_root_folder>/accordina`)
  every script below writes into.
- `generate_accordina_fingerings.py`: for every single note in the accordina's range, renders an SVG of that
  one note's button and writes `accordina_fingering.csv`.
- `generate_accordina_intervals.py`: for every interval pattern up to two octaves, renders it from 3 starting
  button positions and writes `accordina_intervals.csv`.
- `generate_accordina_scales.py`: `SetOfAccordinaNoteForScale` (a `SetOfAccordinaNote` named after the scale
  it pictures) and `generate()`, meant to render every practiced scale pattern at 1/2 octaves from 3 starting
  positions into `accordina_scale.csv` — **currently dead code**: `generate()` is never called by this
  module or by `../generate.py`, and even if it were, `SetOfAccordinaNoteForScale(notes)` is called without
  the `scale`/`number_of_octaves` arguments its `__init__` requires. See the docstrings in that file for
  specifics; fixing it is outside the scope of this documentation pass.

See [`../README.md`](../README.md) for how the accordina package as a whole fits together, and
[`../../README.md`](../../README.md) for how to run the generators.
