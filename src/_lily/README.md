The low-level LilyPond integration layer ([`lily/`](../lily/) builds the actual staff/sheet notation on top of
this). Named `_lily` rather than `lily` seemingly just to keep it distinct from and sorted before that package;
there is no other significance to the underscore.

- `lily.py`: used to write a `.ly` source file and shell out to the `lilypond` binary to compile it to SVG
  (`compile_`, `chord`, plus `indent` for pretty-printing), on top of `shell()` from
  [`../sh.py`](../sh.py). An incomplete refactor (see the "clean lily" commit) gutted it down to just its
  shared layout constants (staff ambitus limits per clef) and a few re-exported helpers
  (`indent`/`save_file` from [`../utils/util.py`](../utils/util.py), `clean_svg`/`display_svg_file` from
  [`../lily/lily_svg_utils.py`](../lily/lily_svg_utils.py)) — the real rendering logic moved to
  [`../lily/`](../lily/)'s `LilySheet`/`LilyStaff` classes, but **`compile_` and `chord` no longer exist
  here**, while at least three call sites still import `compile_` from here and fail immediately
  (`generate/scales.py`, `instruments/piano/chord_successions/main.py`,
  `instruments/piano/scale_variant/main.py`; see each one's own README) and its own `test_lily.py`'s
  `test_chord`/`test_compile`/`test_chord_compile` would fail the same way if collection got that far (it
  currently fails to even collect, for an unrelated pytest-rootdir reason — see that file). Not fixed here —
  porting those callers to the new `LilySheet` API is real feature work, out of scope for a documentation
  pass.
- `Lilyable/`: `Lilyable` — the protocol/base for "things that know how to render themselves as a chunk of
  LilyPond code" (`LocalLilyable`, `PianoLilyable`, `ListPianoLilyable` for combining several).

Requires a `lilypond` binary on `PATH`; nothing else here needs external dependencies.
