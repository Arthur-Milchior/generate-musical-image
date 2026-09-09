# chord

Generates the "chord" Anki decks: brute-forces every way to place fingers on a fretted instrument, keeps the
ones that form a recognizable, playable chord, and for each resulting chord *pattern* (in any inversion)
produces both a diagram and a "decomposition" note breaking down which notes play which role (tonic, third,
fifth, ...).

## Layout

- [`chord_utils.py`](chord_utils.py) — the brute-force search: `enumerate_frets` recursively yields every
  combination of one fret (or not-played) per string within a `Frets` range, as plain
  `SetOfPositionOnFrettedInstrument`s; `enumerate_fretted_instrument_chords` wraps that as
  `ChordOnFrettedInstrument`s.
- [`chord_on_fretted_instrument.py`](chord_on_fretted_instrument.py) — `ChordOnFrettedInstrument`, a
  `SetOfPositionOnFrettedInstrument` fixing exactly one fret per string (some possibly not-played), the central
  value type of this package: `Barred`/`is_barred`, `is_open`, `is_transposable`, `playable` (via
  `hand_for_chord.py`), `chord_pattern_is_redundant`, `has_not_played_in_middle`, ordering, and the `svg` name
  helpers. Also `ChordColors` (a `ColorsWithTonic` scheme for coloring a chord diagram) and
  `FrettedInstrumentChordFrozenList`.
- [`hand_for_chord.py`](hand_for_chord.py) — `HandForChordForFrettedInstrument`: works out, for a given chord,
  which of the 4 fretting fingers (or a bar) covers each closed position (`compute_hand`), and whether that
  assignment is physically playable (`playable`, checking every finger pair against
  `FrettedInstrument.finger_to_fret_delta`).
- [`playable.py`](playable.py) — the `Playable` enum (`EASY`/`YES`/`NO`) returned by the playability checks
  above.
- [`chromatic_inversion_instantiation_to_chords.py`](chromatic_inversion_instantiation_to_chords.py) /
  [`chromatic_inversion_instantiation_and_its_chords.py`](chromatic_inversion_instantiation_and_its_chords.py) /
  [`chromatic_inversion_instantiation_pattern_with_note_and_its_open_chords.py`](chromatic_inversion_instantiation_pattern_with_note_and_its_open_chords.py)
  — the bookkeeping layer built on `utils`' `RecordKeeper`/`RecordedContainer`: groups every fingering found by
  `chord_utils` under its `ChromaticInversionInstantiation` key (the chord pattern, inversion, and lowest note),
  so each distinct chord accumulates all of its playable fingerings, sorted easiest-first, and can render itself
  as CSV.
- [`generate_chords.py`](generate_chords.py) — `AnkiNotesPreparation`, the top-level driver: enumerates
  candidate fingerings across the fretboard for one instrument (`register_all_chords`), then, once fingerings
  are grouped by chord, derives one `ChordDecompositionAnkiNote` per maximal non-redundant fingering
  (`register_decompositions`). `generate_instrument`/`generate_instruments()` run this end-to-end and write the
  resulting diagrams/CSV.
- [`chord_decomposition_anki_note.py`](chord_decomposition_anki_note.py) — `ChordDecompositionAnkiNote`: the
  Anki note for one specific fingering, breaking its notes down by interval role (tonic/third/fifth/etc, via
  `ClassWithEasyness`) with black and colored diagram variants.
- [`playable.py`](playable.py), [`chord_utils.py`](chord_utils.py) — see above.
- `test_*.py` — unit tests for the modules above (`chord_on_fretted_instrument`, `hand_for_chord`, `generate`,
  the chromatic-inversion record-keeping classes) plus shared fixtures in `test_constants.py`.
- [`__main__.py`](__main__.py) — `python3 -m instruments.fretted_instrument.chord` entry point; just runs
  `generate_chords.py`.
- [`__init__.py`](__init__.py) — empty; just makes `chord` a package.

## Relation to siblings

Chord generation shares [`../position/`](../position/)'s `PositionOnFrettedInstrument`/`SetOfPositionOnFrettedInstrument`
and [`../fretted_instrument/`](../fretted_instrument/)'s `FrettedInstrument` with every other subpackage here,
but is the only one that searches *simultaneous* fret combinations (a chord is a fixed fret per string, held
down all at once) rather than sequential note-to-note motion (that's [`../scale/`](../scale/)) or a single
fixed pair of positions (that's [`../note/`](../note/) and [`../pair/`](../pair/)). Diagrams are rendered the
same way as everywhere else, via a `FrettedPositionMaker` from
[`../position/fretted_position_maker/`](../position/fretted_position_maker/).
