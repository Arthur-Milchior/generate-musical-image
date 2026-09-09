# fretted_instrument

Generates fret-diagram images and Anki-note CSVs for guitar/bass/ukulele-style fretted instruments: single
notes, note pairs (for learning interval distances), scales/arpeggios with fingerings, and chords.

## Layout

- [`fretted_instrument/`](fretted_instrument/) — the instrument/tuning abstraction itself: `FrettedInstrument`,
  `Tuning`, `AbstractFrettedInstrument`, and the concrete `Guitar`/`Bass`/`Ukulele` singletons. Every other
  subpackage below starts from a `FrettedInstrument` defined here. See its own README.
- [`position/`](position/) — the fretboard geometry: `PositionOnFrettedInstrument` (one string + one fret),
  `Fret`/`String` and their ranges/relative offsets, collections of positions (`set/`) with the SVG-rendering
  machinery, and the position-to-SVG drawing strategies (`fretted_position_maker/`). Everything else here
  builds on top of it. Documented by another agent — see its own README (and the READMEs of its subfolders:
  `fret/`, `string/`, `set/`, `fretted_position_maker/`) rather than this one.
- [`note/`](note/) — the single-note deck: one Anki card per chromatic note in the instrument's range, showing
  it on every string that can play it. See its own README.
- [`pair/`](pair/) — the note-pair/interval deck: for every pair of strings, cards showing two positions
  together and the interval between them, used to learn to read distances across strings. See its own README.
- [`scale/`](scale/) — scale/arpeggio fingering generation: searches for playable fingerings of each
  registered `ScalePattern` and renders one diagram per fingering, grouped by starting finger. See its own
  README.
- [`chord/`](chord/) — chord generation: brute-forces every fret combination across the strings, keeps the
  ones that are recognizable, playable chords, and generates diagrams plus note-role "decomposition" notes.
  See its own README.
- [`left_hand_finger.py`](left_hand_finger.py) — `LeftHandFinger`: an unused, fieldless placeholder for a
  future per-finger abstraction; finger numbers are represented as plain `int`s/`FingersType` elsewhere instead
  (see `position/fretted_instrument_position_with_fingers.py`).
- [`generate.py`](generate.py) — runs every generator above (note, pair, position, scale, chord) as an import
  side effect; imported by `instruments/generate.py`, the cross-instrument entry point.
- [`__main__.py`](__main__.py) — `python3 -m instruments.fretted_instrument` entry point; runs a *subset* of
  the generators (position, note, pair, and guitar scales only — not chords, and not the bass/ukulele scale
  generators). Use `generate.py` (or `python3 -m instruments.fretted_instrument.chord`/`.scale`) to run
  everything.
- [`__init__.py`](__init__.py) — empty; just makes `fretted_instrument` a package.

## How the pieces fit together

A `FrettedInstrument` (from [`fretted_instrument/`](fretted_instrument/)) plus a `solfege` pattern (a scale,
chord, or interval) go into one of the generators ([`note/`](note/), [`pair/`](pair/), [`scale/`](scale/),
[`chord/`](chord/)), which work out which [`position/`](position/) positions to play, collect them into a
`SetOfPositionOnFrettedInstrument`(-with-fingers), and render that to SVG via a `FrettedPositionMaker`. Each
generator also writes an `anki.csv` alongside its diagrams under the instrument's own generated folder
(`<generate_root_folder>/fretted/<instrument>/<tuning>/...`).

Open-position scales/chords using open strings are not generated for scales yet (TODO).

## Running

From `src/`: `python3 -m instruments.fretted_instrument` (subset, see `__main__.py` above) or
`python3 -m instruments.fretted_instrument.<chord|scale|note|pair|position>` for one generator specifically.
See the top-level [`../../README.md`](../../README.md) for how this fits into running the whole repo.
