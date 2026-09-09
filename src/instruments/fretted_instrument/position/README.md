# position

Everything about *where* a note sits on a fretted instrument (which string, which fret) and how to turn one or
many such positions into an SVG fretboard diagram. This package knows nothing about chords/scales as musical
concepts (that's [`../chord/`](../chord/), [`../scale/`](../scale/), [`../pair/`](../pair/)) — it only models the
geometry of the fretboard and the positions on it.

## Layout

- [`fret/`](fret/) — a single fret, and ranges/relative offsets of frets. See its own README.
- [`string/`](string/) — a single string, and sets/relative offsets of strings. See its own README.
- [`abstract_delta.py`](abstract_delta.py) — `AbstractDelta`: shared base for `fret/fret_delta.py`'s `FretDelta`
  and `string/string_deltas.py`'s `StringDelta` — a relative offset range from a reference point, resolved
  against a `FrettedInstrument` into a concrete `Frets`/`Strings` range.
- [`fretted_instrument_position.py`](fretted_instrument_position.py) — `PositionOnFrettedInstrument`: one
  string + one fret, i.e. a single playable position. Provides chromatic-note lookup (`get_chromatic`),
  searching for positions reachable by some interval (`positions_for_interval_with_restrictions`, using a
  `StringDelta`/`FretDelta` or a resolved `Strings`/`Frets`), transposition, and the single-note diagram
  helpers (`singleton_diagram_svg`/`singleton_diagram_svg_name`/`singleton_diagram_key`).
- [`fretted_instrument_position_with_fingers.py`](fretted_instrument_position_with_fingers.py) —
  `PositionOnFrettedInstrumentWithFingers`: a `PositionOnFrettedInstrument` annotated with the set of candidate
  fingers that could play it, narrowed over time (`restrict_to_compatible_fingering`,
  `restrict_to_specific_fingers`) down to a single resolved finger (`finger_label`).
- `fretted_instrument_position_with_finger.py` — a stale, entirely commented-out prior attempt at per-finger
  positions, superseded by `fretted_instrument_position_with_fingers.py` above. Left as-is (dead code, not
  imported anywhere).
- [`fretted_position_maker/`](fretted_position_maker/) — turns a single position into SVG (a colored/labelled
  dot on the fretboard). See its own README.
- [`set/`](set/) — collections of positions (a chord shape, a scale run) with set-algebra-like operations and
  the top-level diagram-generation entry points. See its own README.
- [`positions_consts.py`](positions_consts.py) — the SVG size constants (margins, fret/string spacing, circle
  radius, font sizes, …) shared by every geometry/drawing method in this package and its subfolders.
- [`generate.py`](generate.py) — script run for its side effect: for every `FrettedInstrument` in
  `fretted_instruments`, writes one single-note SVG diagram per (string, fret) pair under
  `<instrument>/positions/` in the generated output. Used to illustrate the start/end note of a scale or chord
  elsewhere.
- [`__main__.py`](__main__.py) — `python3 -m instruments.fretted_instrument.position` entry point; just runs
  `generate.py`.
- `test_fretted_instrument_position.py` / `test_fretted_instrument_position_with_fingers.py` — unit tests for
  the two position classes above.

## Relation to `fretted_instrument/`

This package is the geometric foundation the rest of [`../`](../) (`chord/`, `scale/`, `pair/`, the solo-note
generator) builds on: they work out *which* `PositionOnFrettedInstrument`s to play (given a `FrettedInstrument`
from [`../fretted_instrument/`](../fretted_instrument/) and a `solfege` pattern), collect them into a
[`set/`](set/) collection, and render that collection to SVG via a [`fretted_position_maker/`](fretted_position_maker/).
