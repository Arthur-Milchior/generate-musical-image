Generic SVG-generation helpers, used by every instrument's diagram code (and by `lily/lily_svg_utils.py` for
post-processing LilyPond's own SVG output). Nothing here knows about music; see the parent
[`utils/README.md`](../README.md) for how this fits into the rest of `utils/`.

- [`svg_lines.py`](svg_lines.py) / [`svg_line.py`](svg_line.py): `SvgLines` — the single abstract method,
  `svg_lines()`, that anything renderable as SVG must implement (yield one tag/text fragment per line).
  `SvgLine` is a convenience specialization for generators that only ever produce a single line.
- [`svg_generator.py`](svg_generator.py): `SvgGenerator(SvgSaver, SvgLines)` — the base class most SVG-producing
  classes actually extend. Implements `svg()` by wrapping `svg_lines()`'s content in an `<svg>` root (with a
  white background rect) and auto-indenting every line according to tag nesting (via `_SvgLine`, below).
  Subclasses only need to implement `svg_lines()`, `svg_width()`, `svg_height()` and `_svg_name_base()`.
- [`svg_saver.py`](svg_saver.py): `SvgSaver` — the abstract `svg()` method plus the shared save-to-disk logic
  (`svg_name()`'s naming convention, `save_svg()` writing the file).
- [`_svg_line.py`](_svg_line.py): `_SvgLine` — parses one line of SVG to decide whether it opens, closes, or is a
  self-contained/leaf tag, so `SvgGenerator.svg()` can auto-indent the assembled document. Internal to this
  package; not part of the public API.
- [`svg_atom.py`](svg_atom.py): smallest, single-tag SVG building blocks (`svg_circle`, `svg_text`) used by
  concrete generators instead of hand-writing SVG markup.
