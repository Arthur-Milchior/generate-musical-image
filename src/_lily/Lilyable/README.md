# Lilyable

The "make yourself into LilyPond source" abstraction that [`../lily.py`](../lily.py) compiles. This is the
lowest-level piece of the LilyPond stack (below [`../../lily/staff/`](../../lily/staff/) and
[`../../lily/sheet/`](../../lily/sheet/)), and predates/overlaps with it: `lily/staff` + `lily/sheet` is the
newer, `DataClassWithDefaultArgument`-based way to build piano notation, while this folder is an older
protocol-style abstraction still used directly by some piano generation code.

- [`lilyable.py`](lilyable.py): `Lilyable`, the base protocol — one abstract method `lily(midi: bool) -> str`
  returning a full `\score{...}` block, plus `LiteralLilyable`, a fake/leaf implementation with a fixed string.
- [`local_lilyable.py`](local_lilyable.py): `LocalLilyable` — a smaller unit than `Lilyable`: the LilyPond syntax
  for a single note/chord/token (`syntax_for_lily()`), as opposed to a whole renderable score. Plus
  `LiteralLocalLilyable`, a fixed-string fake.
- [`piano_lilyable.py`](piano_lilyable.py): `PianoLilyable`, a `Lilyable` specialized to piano — separates a
  piece into an optional left-hand staff (bass clef), an optional right-hand staff (treble clef), and an
  optional annotation (rendered as `\new Lyrics`), then `lily()` combines whichever are present into one
  `PianoStaff` group. `LiteralPianoLilyable` is the concrete leaf (fixed key/hand/annotation strings) that other
  code builds from; `lilypond_code_for_one_hand()` / `lilypond_code_for_two_hands()` are convenience functions
  building one directly from lists of `LocalLilyable` fingerings.
- [`list_piano_lilyable.py`](list_piano_lilyable.py): `ListPianoLilyable` — concatenates several `PianoLilyable`s
  (e.g. successive chords of a scale) into one, inserting `\key` changes between elements when their key
  differs.

All `__eq__` implementations here compare by *generated LilyPond code* (or, for `PianoLilyable`, by the
key/hands/annotation components that feed into it), not by field identity — so two differently-constructed
instances that render to the same code are equal.
