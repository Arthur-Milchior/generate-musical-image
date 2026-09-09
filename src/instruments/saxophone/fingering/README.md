# fingering

The saxophone fingering model: for every playable note, every alternate way to finger it (normal, alternate,
trill, drop, altissimo/overtone, ...), each expressed as the set of buttons pressed (see
[`../buttons.py`](../buttons.py)). This is the data consumed by the saxophone chart/Anki generation code (see
[`../README.md`](../README.md)).

- [`saxophone_fingering.py`](saxophone_fingering.py): `SaxophoneFingering` — one specific fingering for one
  note: which buttons are pressed, its `FingeringSymbol` role (normal, trill, alternate, drop, velocity, ...),
  and how exposed/idiomatic it is. Every concrete fingering defined anywhere in this package is built via
  `SaxophoneFingering.make()` or its `add_*`/`remove_*`/`silent_button` chaining helpers, and registers itself
  in `value_to_fingering`. `FingeringSymbol` is the enum of possible roles, following Jay's/Rascher's fingering
  book terminology.
- [`saxophone_fingerings.py`](saxophone_fingerings.py): `Fingerings` — groups every alternate fingering for one
  note together, and builds `value_to_fingerings` (one `Fingerings` per note from `b_flat_3` up to `c8`,
  Rascher's altissimo ceiling) by importing every fingering-defining submodule below.
- [`rascher.py`](rascher.py): `RascherFingering` — fingerings from Rascher's "Top Tones" altissimo book; these
  always implicitly press `octave` and `e_flat` in addition to whatever is given explicitly.
- [`main_column/`](main_column/): fingerings using only the main column of keys (no overtone/altissimo key, no
  `H`/`C_n` key, no `K_n` key) — see its own README.
- [`k/`](k/): fingerings using a `k1`/`k2`/`k3` (Jay notation; `Tf`/`Ta`/`Tc` in Londeix notation) key, except
  when they also use overtone or a `C_n` button (those live in `overtone/`/`cn/` instead) — see its own README.
- [`cn/`](cn/): fingerings using a `C1`/`C2`/`C3`/`C4` button (Londeix notation; `H1`-`H3`/`K4` in Jay notation)
  — see its own README.
- [`overtone/`](overtone/): fingerings using the overtone/altissimo key (`A` in Jay notation, `x` in Londeix
  notation) — see its own README.
- [`test_fingerings.py`](test_fingerings.py): tests for the fingering catalog.

Each of the four subfolders' fingering-defining modules also has a `*_silent` sibling (e.g. `k.k_silent`,
`cn.cn_silent`) for the equivalent fingering with the octave key not pressed, imported alongside the main one
in `saxophone_fingerings.py`.
