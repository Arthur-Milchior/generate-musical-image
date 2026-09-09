One subpackage per instrument. Each turns a `solfege` pattern (a scale, chord, interval...) into rendered
SVG diagrams and Anki-note CSVs for that instrument; see [`../README.md`](../README.md) for how the whole
repo fits together and how to run a generator (`python3 -m instruments.<name>` from `src/`), and each
subpackage's own README for its details.

- [`piano/`](piano/) — generates fingering diagrams (as LilyPond-rendered staff notation) for scales played
  on piano, choosing a fingering by penalty score across one/two octaves, both hands, and every
  increasing/decreasing direction.
- [`fretted_instrument/`](fretted_instrument/) — generates fret-diagram images (single notes, note pairs,
  scales, and chords) for guitar/bass/ukulele-style fretted instruments.
- [`saxophone/`](saxophone/) — generates fingering-chart images (which keys are pressed) for every saxophone
  note, including alternate/trill/altissimo fingerings.
- [`accordina/`](accordina/) — generates button-grid diagrams (single notes, intervals, and — not currently
  wired up, see [`accordina/generate/README.md`](accordina/generate/README.md) — scales) for the
  [accordina](https://en.wikipedia.org/wiki/Accordina).
- [`harmonica/`](harmonica/) — the smallest/least developed package: draws a fixed 10-hole outline with one
  hole highlighted, for every hole and blow/draw direction; see its README for a gotcha where the generator
  currently writes its output to the sibling top-level `src/harmonica/` folder instead of its own `images/`.

`generate.py` at this level runs the accordina, saxophone and fretted-instrument generators together (piano
and harmonica are currently commented out there); `__init__.py` is empty (just makes `instruments` a
package).
