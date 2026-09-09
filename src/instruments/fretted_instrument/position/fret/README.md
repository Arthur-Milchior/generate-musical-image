# fret

Everything about a single fret and about ranges/offsets of frets, for one string of a fretted instrument.

## Layout

- [`fret.py`](fret.py) — `Fret`: one fret on a string. `value` is the fret number (`0` = open string, `None` =
  not played); `absolute` says whether `value` is an absolute fret number on the instrument or a relative offset
  (e.g. a transposition amount). Provides ordering (`not played` sorts as greater than any played fret),
  arithmetic against a `ChromaticInterval`/another `Fret` (`add`/`sub`, instrument-aware since the number of
  frets is instrument-dependent), and the geometry/SVG helpers (`height`, `y_fret`, `x_dots`, `fret_svg`,
  `dots_svg`) used to draw the fret line and its position-marker dots — see
  [`../positions_consts.py`](../positions_consts.py) for the underlying size constants.
- [`frets.py`](frets.py) — `Frets`: an allowed *range* of frets, expressed as an optional closed interval
  `[min_fret, max_fret]` plus independent flags for whether the open string and/or "not played" are allowed.
  Iterating a `Frets` yields every allowed `Fret`. Used to represent both a static allowed fret range (e.g.
  `Frets.all_played(instrument)`) and the resolved output of a `FretDelta`.
- [`fret_delta.py`](fret_delta.py) — `FretDelta`: the fret-specific implementation of
  [`../abstract_delta.py`](../abstract_delta.py)'s `AbstractDelta`. Represents a fret constraint *relative* to a
  reference fret (e.g. "within 2 frets of the current one") rather than an absolute range; `range()` resolves it
  against a concrete reference `Fret` and instrument into a concrete `Frets`.
- `test_fret.py` / `test_frets.py` — unit tests for the two classes above.

## Relation to the rest of `position/`

`Fret` pairs with [`../string/`](../string/)'s `String` to form a `PositionOnFrettedInstrument` (one
string + one fret) — see [`../fretted_instrument_position.py`](../fretted_instrument_position.py). `FretDelta`
plays the same relative-offset role for frets that [`../string/string_deltas.py`](../string/string_deltas.py)'s
`StringDelta` plays for strings, and both are consumed together by
`PositionOnFrettedInstrument.positions_for_interval_with_restrictions` when searching for reachable positions.
The SVG-drawing methods on `Fret`/`Frets` are called from the
[`../fretted_position_maker/`](../fretted_position_maker/) machinery when rendering a fretboard diagram.
