# colored_position_maker

[`../fretted_position_maker.py`](../fretted_position_maker.py)'s `FrettedPositionMaker` subclasses that pick a
dot's fill/outline color from the note being played, rather than adding any text.

## Layout

- [`constants.py`](constants.py) — the named colors used across this subfolder (`COLOR_TONIC`, `COLOR_THIRD`,
  `COLOR_FIFTH`, `COLOR_QUALITY`, `DEFAULT_COLOR`, `BACKGROUND_COLOR`, `SELECTED_STRING_COLOR`).
- [`colored_position_from_note.py`](colored_position_from_note.py) — `Colors`: the base `FrettedPositionMaker`
  that draws a filled circle (or "not played" cross) whose color comes from `get_color_from_note`, an abstract
  method subclasses must implement.
- [`black_only.py`](black_only.py) — `BlackOnly`: the trivial `Colors` subclass that always returns
  `DEFAULT_COLOR`, i.e. every note drawn identically in black. Used for plain (non-analytical) diagrams, e.g.
  the single-note illustrations from [`../../generate.py`](../../generate.py).
- [`interval_dependant_colored_position_maker.py`](interval_dependant_colored_position_maker.py) —
  `ColorsWithTonic`: a `Colors` subclass that colors a note by its interval above a fixed `tonic` rather than by
  its absolute pitch, via the abstract `get_color_from_interval`. Concrete interval-role colorings (e.g.
  `ScaleColors`, tonic/third/fifth/quality) live alongside the sets that use them, e.g.
  [`../../set/set_of_fretted_instrument_positions_with_fingers.py`](../../set/set_of_fretted_instrument_positions_with_fingers.py).
- `note_dependant_colored_position_maker.py` — currently empty; reserved for a `Colors` subclass keyed on
  absolute note rather than interval (the note-name equivalent of `ColorsWithTonic`).

## Relation to the rest of `fretted_position_maker/`

These classes only ever answer "what color for this note/interval?" — they're combined with
[`../maker_with_letters/`](../maker_with_letters/) (which needs a `circle_color`) or used directly wherever a
plain colored dot is enough, and can be composed via
[`../conditional_fretted_position_maker.py`](../conditional_fretted_position_maker.py) to switch coloring
strategy based on interval.
