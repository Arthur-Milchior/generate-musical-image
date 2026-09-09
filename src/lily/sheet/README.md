# sheet

A full LilyPond sheet built on top of [`../staff/`](../staff/): the code that writes a sheet's `.ly` source
file, shells out to `lilypond` (via [`../../_lily/lily.py`](../../_lily/lily.py)) to compile it to SVG, and
caches/skips recompilation when the source hasn't changed and the SVG already exists.

- [`lily_sheet.py`](lily_sheet.py): `LilySheet`, the abstract base. `maybe_generate()` is the main entry point —
  writes the `.ly` file (`save_file()`), and only recompiles (`compile()`) if the source changed or the output
  SVG is missing. Subclasses implement `file_prefix()` (base file name) and `_lily_code()` (the actual staff
  content); `LilySheet.lily_code()` wraps that with the `\version` header.
- [`lily_sheet_single_staff.py`](lily_sheet_single_staff.py): `LilySheetSingleStaff` — a sheet made of exactly
  one staff (this codebase currently only ever renders single-staff sheets; nothing here combines multiple
  staves into one system).
- [`lily_chord_sheet.py`](lily_chord_sheet.py): `LilyChordSheet` — a single-staff sheet whose staff is a
  `LilyChordStaff` (used both for actual chords and, via `LilySingleNoteStaff`, for single notes). Also the
  `lily_chord_sheet()` convenience constructor.
- [`lily_sheet_single_note.py`](lily_sheet_single_note.py): `sheet_single_note()`, a convenience function
  building a `LilyChordSheet` around a `LilySingleNoteStaff` for exactly one note.
- [`lily_scale_sheet.py`](lily_scale_sheet.py): `LilyScaleSheet` — a single-staff sheet whose staff is a
  `LilyScaleStaff` (a melodic sequence, e.g. a scale/arpeggio).
- [`fake_lily_sheet.py`](fake_lily_sheet.py): `FakeLilySheet`, a test double with a fixed prefix/content.

Each `file_prefix()` implementation also doubles as the generated SVG's base file name, so it encodes enough of
the sheet's content (clef, note names, octave-shift suffix, etc.) to make the file names unique and readable.

All classes here are `DataClassWithDefaultArgument`s constructed via `.make(...)` (see
[`../../utils/README.md`](../../utils/README.md)).
