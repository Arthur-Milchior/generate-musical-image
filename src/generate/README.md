Cross-instrument generation entry points that don't belong to any single `instruments/` subpackage.

- `generate_note.py`: renders every note name (each diatonic letter × alteration, a few octaves) as a single
  staff-notation image via LilyPond (`_lily/lily.py`).
- `scales.py`: for a handful of hard-coded chromatic wind instruments (ocarinas, tin whistle, recorder,
  harmonica — *not* the `instruments/` subpackages), generates one Anki CSV row per scale/arpeggio pattern,
  instrument and enharmonic key, sorted by difficulty (`AnkiNote(...).difficulties()` via `Difficulties`).
  **Currently has a pre-existing syntax error** (`AnkiField.field()` is written as
  `yield anki_field.field())`, an extra closing paren) and cannot be imported as-is; not fixed here — this
  documentation pass is documentation-only. See the module's own docstring for more.
- `scale_number.py`: generates the scale-degree ("scale number") reference CSV — one row per
  scale/arpeggio pattern giving its interval structure (not tied to any instrument).
- `__main__.py`: `from generate import generate_note, scales` — run via `python3 -m generate` from `src/`.
  Currently fails because of the `scales.py` bug above.
