Generates saxophone fingering-chart images and Anki notes.

- `buttons.py`: `SaxophoneButton`, one physical key/button on the horn, drawn as an SVG shape.
- `fingering/`: `SaxophoneFingering` (which buttons are pressed for a given note) and `Fingerings`
  (`saxophone_fingerings.py`, the possibly-several alternate fingerings for one note) plus per-register
  button layouts (`main_column/`, `cn/`, `k/`, `overtone/` — each documented in its own README) and
  `rascher.py` (Rascher-style altissimo fingerings).
- `generate.py`: for every note, renders each known fingering as SVG and writes the corresponding Anki notes.
  Run via `python3 -m instruments.saxophone` from `src/` (see [`../../README.md`](../../README.md)).
