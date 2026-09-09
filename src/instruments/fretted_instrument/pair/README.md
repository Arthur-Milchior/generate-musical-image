# pair

Generates the "interval between two strings" Anki deck: for every pair of strings on a fretted instrument, one
card per fret combination showing the two positions together and the interval between them. Used to learn to
read the distance between two notes played on different strings.

## Layout

- [`generate_fretted_instrument_interval.py`](generate_fretted_instrument_interval.py) —
  `FrettedInstrumentIntervalAnkiNote` (`CsvGenerator`, `SvgSaver`): one Anki note for a pair of positions
  `(pos1, pos2)` on two distinct strings, where at least one of the two frets is 0 or 1 (so the deck only covers
  distances measured from an open/near-open reference, not every possible pair of frets). Renders both
  positions on one diagram (`svg`) and reports the fret difference, the raw interval, and its name
  (`pos_difference`, `interval`, `difference_name`). `pairs_of_frets_values(max_distance)` is the generator of
  (low fret, high fret) combinations to quiz, fret 1 paired against every fret up to `max_distance + 2` in both
  directions.
- [`generate_pairs.py`](generate_pairs.py) — the script: `generate_instrument` iterates every string pair
  returned by `FrettedInstrument.pair_of_string_with_distinct_intervals` (skipping pairs with a redundant
  open-string interval), saves a plain two-string-highlighted diagram, then one
  `FrettedInstrumentIntervalAnkiNote` per fret combination from `pairs_of_frets_values`; `generate()` runs this
  for every instrument in `fretted_instruments` and writes `anki.csv` under `<instrument>/pair/`.
- [`test.py`](test.py) — unit test for `pairs_of_frets_values`.
- [`__main__.py`](__main__.py) — `python3 -m instruments.fretted_instrument.pair` entry point; just runs
  `generate_pairs.py`.
- [`__init__.py`](__init__.py) — empty; just makes `pair` a package.

## Relation to siblings

Like [`../note/`](../note/), this is a small value-object/generator module built directly on
[`../position/`](../position/)'s `PositionOnFrettedInstrument` and
[`../fretted_instrument/`](../fretted_instrument/)'s `FrettedInstrument`, with no knowledge of chords or scales
as musical concepts (that's [`../chord/`](../chord/) and [`../scale/`](../scale/)).
