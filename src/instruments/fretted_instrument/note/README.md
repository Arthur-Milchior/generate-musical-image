# note

Generates the "single note" Anki deck for a fretted instrument: one card per chromatic note across the
instrument's whole playable range, showing where that note falls on every string that can play it.

## Layout

- [`generate_fretted_notes.py`](generate_fretted_notes.py) — `NoteOnFrettedInstrumentAnkiNote`
  (`DataClassWithDefaultArgument`, `CsvGenerator`, `SvgSaver`): one Anki note for one `ChromaticNote`, built via
  `make_note` by locating every `PositionOnFrettedInstrument` (across all strings) that plays it. Produces both
  a diagram with the note highlighted on every string (`svg`/`all_notes_field`) and one small diagram per
  string (`field_for_string`, using `PositionOnFrettedInstrument.singleton_diagram_svg_name`), plus a staff
  image via `lily`. Run as a script (module-level loop over `fretted_instruments`): for each instrument, walks
  every note from `lowest_note()` to `highest_note()`, saves its diagram(s), and writes `anki.csv` under
  `<instrument>/note/`.
- [`__main__.py`](__main__.py) — `python3 -m instruments.fretted_instrument.note` entry point; just runs
  `generate_fretted_notes.py`.
- [`__init__.py`](__init__.py) — empty; just makes `note` a package.

## Relation to siblings

Like [`../pair/`](../pair/), this is a small value-object/generator module built directly on
[`../position/`](../position/)'s `PositionOnFrettedInstrument` and
[`../fretted_instrument/`](../fretted_instrument/)'s `FrettedInstrument` — it doesn't know about chords or
scales as musical concepts (that's [`../chord/`](../chord/) and [`../scale/`](../scale/)). The single-note
diagrams generated here (and the near-identical ones from
[`../position/generate.py`](../position/generate.py)) are also referenced elsewhere to illustrate the
start/end note of a scale or chord.
