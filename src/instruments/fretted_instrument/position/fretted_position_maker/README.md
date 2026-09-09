# fretted_position_maker

Strategies for drawing one played [`../fretted_instrument_position.py`](../fretted_instrument_position.py)
(a single fret/string dot) as SVG. A `FrettedPositionMaker` doesn't know about whole chord/scale shapes — that's
[`../set/`](../set/), which iterates its positions and calls a maker on each one; the maker only decides what a
*single* dot looks like (its color, and optionally a text label).

## Layout

- [`fretted_position_maker.py`](fretted_position_maker.py) — `FrettedPositionMaker`: the abstract base. Defines
  `svg_content`/`svg_lines` (draw one position) and `__str__` (a short identifier used when naming generated
  files, so diagrams made with different makers don't collide).
- [`conditional_fretted_position_maker.py`](conditional_fretted_position_maker.py) —
  `ConditionalFrettedPositionMaker`: delegates to one of two other makers depending on whether a position's
  interval above a `tonic` falls in a given set of `selected_intervals` — e.g. drawing compound chord
  extensions in a different style from the rest of the notes.
- [`colored_position_maker/`](colored_position_maker/) — makers that color each dot by note or by interval
  role. See its own README.
- [`maker_with_letters/`](maker_with_letters/) — makers that draw a text label (note name, interval role, and/or
  finger number) inside each dot. See its own README.

## Relation to the rest of `position/`

`FrettedPositionMaker` instances are passed into
[`../set/abstract_set_of_fretted_instrument_positions.py`](../set/abstract_set_of_fretted_instrument_positions.py)'s
`svg_lines`/`svg`/`_svg_name_base` (and into
[`../fretted_instrument_position.py`](../fretted_instrument_position.py)'s `singleton_diagram_svg`), which call
`svg_content` on the maker for every position in the set to build the full fretboard diagram, and call `str()`
on the maker to build the output filename. The geometry each maker draws against (dot radius, coordinates, …)
comes from [`../positions_consts.py`](../positions_consts.py) via `String.x()`/`Fret.y_dots()` etc.
