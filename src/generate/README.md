Cross-instrument generation entry points that don't belong to any single `instruments/` subpackage.

- `generate_note.py`: renders every note name (each diatonic letter × alteration, a few octaves) as a single
  staff-notation image via LilyPond (`lily/sheet/lily_sheet_single_note.py`'s `sheet_single_note`).
- `scales.py`: for a handful of hard-coded chromatic wind instruments (ocarinas, tin whistle, recorder,
  harmonica — *not* the `instruments/` subpackages), generates one Anki CSV row per scale/arpeggio pattern,
  instrument and enharmonic key, sorted by difficulty (`AnkiNote(...).difficulties()` via `Difficulties`).
  **Currently fails to import**: it calls `compile_()` (`from _lily.lily import compile_`), a function that no
  longer exists in `_lily/lily.py` — a gap shared with a couple of other pre-existing entry points, see
  [`../_lily/README.md`](../_lily/README.md). Not fixed here; porting to the current `LilySheet` API is real
  feature work, out of scope for a documentation pass.
- `scale_number.py`: generates the scale-degree ("scale number") reference CSV — one row per
  scale/arpeggio pattern giving its interval structure (not tied to any instrument).
- `__main__.py`: `from generate import generate_note, scales` — run via `python3 -m generate` from `src/`.
  Currently fails because of the `scales.py` bug above (`generate_note` itself imports and runs fine on its
  own).
