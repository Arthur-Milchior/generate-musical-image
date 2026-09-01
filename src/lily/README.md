Higher-level LilyPond notation builders (see [`../_lily/README.md`](../_lily/README.md) for the actual
LilyPond-invocation layer this builds on).

- `staff/`: `LilyStaff` and subclasses — the lilypond code for one staff (clef + key signature), specialized for
  a single note, a scale, or a chord.
- `sheet/`: `LilySheet` and subclasses — a full sheet (one or more staves, e.g. treble+bass), which knows how to
  write its own `.ly` source, compile it (`_lily/lily.py`, requires `lilypond` on `PATH`), and cache/skip
  recompiling when the output already exists (`maybe_generate()`).
- `lily_svg_utils.py`: post-processes the SVG LilyPond produces (cleanup, cropping/display helpers).
