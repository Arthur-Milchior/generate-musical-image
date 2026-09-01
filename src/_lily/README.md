The low-level LilyPond integration layer ([`lily/`](../lily/) builds the actual staff/sheet notation on top of
this). Named `_lily` rather than `lily` seemingly just to keep it distinct from and sorted before that package;
there is no other significance to the underscore.

- `lily.py`: writes a `.ly` source file and shells out to the `lilypond` binary (`shell()` from
  [`../sh.py`](../sh.py)) to compile it to SVG (`compile_`); also defines shared layout constants
  (staff ambitus limits per clef).
- `Lilyable/`: `Lilyable` — the protocol/base for "things that know how to render themselves as a chunk of
  LilyPond code" (`LocalLilyable`, `PianoLilyable`, `ListPianoLilyable` for combining several).

Requires a `lilypond` binary on `PATH`; nothing else here needs external dependencies.
