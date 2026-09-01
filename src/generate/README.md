Cross-instrument generation entry points that don't belong to any single `instruments/` subpackage.

- `generate_note.py`: renders every note name (each diatonic letter × alteration, a few octaves) as a single
  staff-notation image via LilyPond (`_lily/lily.py`).
- `scales.py`: for every scale/chord-arpeggio pattern in `solfege.pattern`, generates one Anki CSV row per
  instrument (piano, guitar, ...) and enharmonic key, sorted by difficulty (`AnkiNote(...).difficulties()`).
- `scale_number.py`: generates the scale-degree ("scale number") notation/reference material.
- `__main__.py`: `from generate import generate_note, scales` — run via `python3 -m generate` from `src/`.
