Generates images and Anki notes for the [accordina](https://en.wikipedia.org/wiki/Accordina).

- `accordina_note.py`: extends `solfege.value.note` with the accordina's button-grid geometry (button radius,
  spacing between columns/rows) and draws a single button as SVG.
- `set_of_accordina_notes.py`: a set of accordina notes/positions (used to represent a scale or chord chunk on
  the button grid), mirroring what `fretted_instrument`'s `SetOfPos` does for frets.
- `generate.py` / `generate/`: the actual generation loops (`generate_accordina_scales.py`,
  `generate_accordina_intervals.py`, `generate_accordina_fingerings.py`) and shared constants
  (`generate/accordina_constants.py`). Run via `python3 -m instruments.accordina` from `src/` (see
  [`../../README.md`](../../README.md)).
