# maker_with_letters

[`../fretted_position_maker.py`](../fretted_position_maker.py)'s `FrettedPositionMaker` subclasses that draw a
text label inside each position's circle (a note name, an interval role, and/or — for
`PositionOnFrettedInstrumentWithFingers`— a finger number), rather than only coloring it.

## Layout

- [`fretted_position_maker_with_letters.py`](fretted_position_maker_with_letters.py) —
  `FrettedPositionMakerWithLetter`: the base class. Draws a circle (outlined in `circle_color`, defaulting to
  `DEFAULT_COLOR`) plus a text label from the abstract `text` method, and — if the position carries fingers
  (`PositionOnFrettedInstrumentWithFingers`) — a smaller finger-number label offset below-right of it.
- [`fretted_position_maker_for_note.py`](fretted_position_maker_for_note.py) — `FrettedPositionMakerForNote`:
  labels each position with its absolute note name (e.g. `"C#4"`).
- [`fretted_position_maker_for_interval.py`](fretted_position_maker_for_interval.py) —
  `FrettedPositionMakerForInterval`: labels each position with its interval role relative to a `tonic` (e.g.
  `"3m"`, `"5"`, `"T"`), looked up from a `SolfegePattern` so the label matches the actual scale/chord degree
  names rather than a fixed generic table.

## Relation to the rest of `fretted_position_maker/`

`FrettedPositionMakerWithLetter` is a sibling strategy to
[`../colored_position_maker/`](../colored_position_maker/)'s `Colors` — both are `FrettedPositionMaker`s picked
by whatever builds a [`../../set/`](../../set/) diagram, depending on whether the caller wants a plain colored
dot or a labelled one (typically for teaching diagrams where the note/interval name needs to be legible, e.g.
scale/chord practice sheets built from `../../set/set_of_fretted_instrument_positions_with_fingers.py`).
