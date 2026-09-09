# set

Collections of [`../fretted_instrument_position.py`](../fretted_instrument_position.py)s — a chord shape, a
scale run, a single illustrated note — with set-algebra-like operations (subset comparison, adding a position,
restricting by role/interval) and the machinery that renders a whole collection to one SVG fretboard diagram.

## Layout

- [`abstract_set_of_fretted_instrument_positions.py`](abstract_set_of_fretted_instrument_positions.py) —
  `AbstractSetOfFrettedPositions`: the base class, generic over the concrete position type it holds. Provides
  subset/equality comparisons (`<`, `<=`, `==`, order-independent over `played_positions()`), role queries
  relative to a tonic (`get_tonics`/`get_thirds`/`get_fifths`/`get_quality`/`get_other`), fret-span helpers used
  to pick the easiest fingering (`number_of_frets`, `best_chord_key`, `easy_key` for `ClassWithEasyness`),
  transposition (`transpose_same_string`, `transpose_to_fret_one`), and the `SvgGenerator` implementation
  (`svg_lines`/`svg_width`/`svg_height`/`_svg_name_base`) that turns the set into a fretboard diagram given a
  [`../fretted_position_maker/`](../fretted_position_maker/).
- [`set_of_fretted_instrument_positions.py`](set_of_fretted_instrument_positions.py) —
  `SetOfPositionOnFrettedInstrument`: the concrete instantiation holding plain `PositionOnFrettedInstrument`
  (no finger annotation), plus `empty_set_of_position` to build an empty one for a given instrument.
- [`set_of_fretted_instrument_positions_with_fingers.py`](set_of_fretted_instrument_positions_with_fingers.py) —
  `SetOfFrettedInstrumentPositionsWithFingers`: the concrete instantiation holding
  `PositionOnFrettedInstrumentWithFingers`, plus `resolve_fingers` (narrows every position's candidate fingers
  down to the single finger expected to play it, walking the set in melodic order) and `ScaleColors` (a
  `ColorsWithTonic` scheme coloring tonic/third/fifth/quality notes distinctly). This file is the house style
  reference for docstring/attribute-doc conventions in this subtree.
- [`colors.py`](colors.py) — currently dead code: an early, entirely commented-out sketch of a
  `ConditionalFrettedPositionMaker` keyed on a set of selected notes rather than intervals, superseded by
  [`../fretted_position_maker/conditional_fretted_position_maker.py`](../fretted_position_maker/conditional_fretted_position_maker.py).
- `test_set_of_fretted_instrument_positions.py` — unit tests, using a small `SetOfPositionOnGuitar` test
  subclass that accepts raw `(string, fret)` int tuples in `add`.

## Relation to the rest of `position/`

A set is built up from individual [`../fretted_instrument_position.py`](../fretted_instrument_position.py)/
`fretted_instrument_position_with_fingers.py` positions (typically by the chord/scale generators in
[`../../chord/`](../../chord/) and [`../../scale/`](../../scale/)), and rendered by picking a
[`../fretted_position_maker/`](../fretted_position_maker/) and calling the `SvgGenerator` methods inherited from
`AbstractSetOfFrettedPositions`. `String`/`Fret` geometry ([`../string/`](../string/), [`../fret/`](../fret/))
underlies the drawing; [`../positions_consts.py`](../positions_consts.py) supplies the size constants.
