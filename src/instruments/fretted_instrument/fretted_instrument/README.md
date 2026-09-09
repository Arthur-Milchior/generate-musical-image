# fretted_instrument

The instrument/tuning abstraction: what a "guitar", "bass" or "ukulele" *is* (frets, strings, clef, how far
fingers can reasonably be spread) and how a specific tuning strings it, independent of any note/chord/scale
being played on it. Every other subpackage of [`../`](../) takes a `FrettedInstrument` from here as the
starting point for its own generation.

## Layout

- [`abstract_fretted_instrument.py`](abstract_fretted_instrument.py) — `AbstractFrettedInstrument`: the
  tuning-independent characteristics of an instrument family — `number_of_frets`, `number_of_strings`, `clef`,
  and `finger_to_fret_delta_chord`/`finger_to_fret_delta_scale` (per finger-pair allowed fret-span ranges,
  looser for chords than for scales since a chord holds still), plus `number_of_scales_reachable_per_string`
  (a sanity-check bound used by scale generation).
- [`tuning.py`](tuning.py) — `Tuning`: a named (or default) sequence of open-string notes,
  `open_string_chromatic_note`, one per string from string 1 up. Provides `string`/`strings` lookup and
  `pair_of_string_with_distinct_intervals` (one representative string pair per distinct open-string interval,
  used by [`../pair/`](../pair/) to avoid redundant Anki cards).
- [`fretted_instrument.py`](fretted_instrument.py) — `FrettedInstrument`: the concrete, playable combination of
  an `AbstractFrettedInstrument` and a `Tuning`. This is the object actually passed around everywhere else —
  `string`/`strings`, `clef`, `number_of_strings`/`number_of_frets`, `lowest_note`/`highest_note`,
  `generated_folder_name` (where this instrument's output goes), `width` (diagram pixel width),
  `max_distance_between_two_closed_frets` (how many frets a chord diagram needs to show), and
  `finger_to_fret_delta` (delegating to the `AbstractFrettedInstrument`).
- [`fretted_instruments.py`](fretted_instruments.py) — the concrete singletons: `Guitar`, `Bass`, `Ukulele`
  (each an `AbstractFrettedInstrument` + default `Tuning`), a handful of alternate guitar tunings (`drop_d`,
  `double_drop_d`, `vestapol`, `english_guitar`, `overtone_G` — defined but not wired into any generator), and
  `fretted_instruments = [Guitar, Ukulele, Bass]`, the list every generator in this package iterates over.
- [`__init__.py`](__init__.py) — empty; just makes `fretted_instrument` a package.

## Relation to siblings

[`../position/`](../position/) (fretboard geometry), [`../note/`](../note/), [`../pair/`](../pair/),
[`../scale/`](../scale/) and [`../chord/`](../chord/) (the actual generators) all take a `FrettedInstrument`
from here as their entry point, and iterate `fretted_instruments` to run themselves once per instrument. This
package itself knows nothing about the fretboard's geometry (that's [`../position/`](../position/)) or about
musical content (chords/scales — that's [`../chord/`](../chord/)/[`../scale/`](../scale/)).
