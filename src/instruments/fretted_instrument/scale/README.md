# scale

Generates the "scale/arpeggio fingering" Anki decks: for each registered `ScalePattern` (scales, arpeggios,
and — via the pattern list imports — chords treated as patterns), works out playable fingerings on a fretted
instrument and renders each as a diagram. Open-position scales (using open strings) are not covered yet (see
the top-level [`../README.md`](../README.md) TODO).

## Layout

- [`anki_scale.py`](anki_scale.py) — the fingering-search engine, instrument-agnostic:
  - `_generate_scale` recursively enumerates every fingering of a scale as a list of
    `PositionOnFrettedInstrumentWithFingers`, one per interval of the pattern, using
    `PositionOnFrettedInstrumentWithFingers.positions_for_interval`/`restrict_to_compatible_fingering` to keep
    only fingerings where consecutive notes can actually be played together.
  - `generate_scale(instrument, start_pos, scale_pattern, number_of_octaves, filter=..., pattern_to_avoid_list=...)`
    drives `_generate_scale` from one starting position, groups the results by starting finger set, and
    returns an `AnkiScalesWithSameFirstString`.
  - `AnkiScaleWithFingersAndString` — all the ways to play one pattern, from one start string/octave count,
    starting with one specific set of fingers.
  - `AnkiScalesWithSameFirstString` — the same, but across every starting finger set; provides
    `all_scales()` (every fingering, sorted easiest-first), `scales_starting_with_finger`, and
    `best_for_each_finger()` (picks one good fingering each for the first, a middle, and the last finger).
- [`generate_guitar.py`](generate_guitar.py) / [`generate_bass.py`](generate_bass.py) /
  [`generate_ukulele.py`](generate_ukulele.py) — one `ScaleOnAnkiNote` class + `generate_<instrument>()`
  script per instrument, each picking its own set of reference starting positions (different strings/octave
  counts per instrument) and calling `generate_scale`/`best_for_each_finger`/`all_scales` to build the Anki
  fields. Guitar's version is the most elaborate (covers strings 1-4 and both one- and two-octave forms);
  bass/ukulele use a single starting string. Each writes `<instrument>_scales.csv` under
  `<instrument>/scale/transposable/`.
- [`generate_scales.py`](generate_scales.py) — imports all three `generate_*` modules above for their
  generation side effect.
- [`test_generate_scale.py`](test_generate_scale.py) — unit tests for `_generate_scale`/`generate_scale` against
  hand-picked expected major-scale fingering shapes on guitar.
- [`__main__.py`](__main__.py) — `python3 -m instruments.fretted_instrument.scale` entry point; just runs
  `generate_scales.py`.
- [`__init__.py`](__init__.py) — empty; just makes `scale` a package.

## Relation to siblings

Built on the same foundations as [`../chord/`](../chord/) —
[`../position/`](../position/)'s `PositionOnFrettedInstrumentWithFingers`/`SetOfFrettedInstrumentPositionsWithFingers`
and [`../fretted_instrument/`](../fretted_instrument/)'s `FrettedInstrument` — but searches for *sequential*
fingerings (one note at a time, in melodic order) rather than chord's simultaneous fret combinations. Diagrams
are rendered the same way, via a `FrettedPositionMaker` from
[`../position/fretted_position_maker/`](../position/fretted_position_maker/).
