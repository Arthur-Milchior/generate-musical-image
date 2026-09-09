# string

Everything about a single string and about sets/offsets of strings of a fretted instrument. The mirror image of
[`../fret/`](../fret/), one level up in the string dimension instead of the fret dimension.

## Layout

- [`string.py`](string.py) — `String`: one string of the instrument. `value` is the 1-indexed string number,
  `note_open` the `ChromaticNote` sounded when played open. Provides ordering by string number, note/fret lookup
  (`fret_for_note`, `position_for_note`, both instrument-aware since the number of frets is instrument-dependent),
  and the geometry/SVG helpers (`x`, `svg_line`, `svg_for_x`) used to draw the string line and its "not played"
  marker — see [`../positions_consts.py`](../positions_consts.py) for the underlying size constants.
- [`strings.py`](strings.py) — `Strings`: a set of `String`s (backed by a `StringFrozenList`). Supports set-like
  comparisons (`<`, `<=`, `==`), building a contiguous range (`make_interval`), popping the first string, and
  drawing every string in the set (`svg_lines`, with optional highlight `colored_strings`).
- [`string_deltas.py`](string_deltas.py) — `StringDelta`: the string-specific implementation of
  [`../abstract_delta.py`](../abstract_delta.py)'s `AbstractDelta`. Represents a string constraint *relative* to
  a reference string (e.g. "the next string only", "this string or any later one") rather than an absolute set;
  `range()` resolves it against a concrete reference `String` and instrument into a concrete `Strings`. Exposes
  the common cases as named constructors: `SAME_STRING_ONLY`, `SAME_OR_NEXT_STRING`, `NEXT_STRING_ONLY`,
  `NEXT_STRING_OR_GREATER`, `SAME_STRING_OR_GREATER`, `ANY_STRING`.
- `test_string.py` / `test_strings.py` / `test_string_deltas.py` — unit tests for the three classes above.

## Relation to the rest of `position/`

`String` pairs with [`../fret/`](../fret/)'s `Fret` to form a `PositionOnFrettedInstrument` (one string + one
fret) — see [`../fretted_instrument_position.py`](../fretted_instrument_position.py). `StringDelta` plays the
same relative-offset role for strings that [`../fret/fret_delta.py`](../fret/fret_delta.py)'s `FretDelta` plays
for frets, and both are consumed together by
`PositionOnFrettedInstrument.positions_for_interval_with_restrictions` when searching for reachable positions.
The SVG-drawing methods on `String`/`Strings` are called from the
[`../fretted_position_maker/`](../fretted_position_maker/) machinery when rendering a fretboard diagram.
