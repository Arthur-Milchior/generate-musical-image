# Scale instantiation

Anchors a [`ScalePattern`](../../pattern/scale/README.md) to a concrete tonic. See [../README.md](../README.md)
for the shared `AbstractPatternInstantiation` mechanics and the diatonic+chromatic vs. chromatic-only split
this folder plugs into.

- [`abstract_scale_instantiation.py`](abstract_scale_instantiation.py)'s `AbstractScale`: fixes
  `pattern_type = ScalePattern`, and overrides `get_notes(number_of_octaves=1, add_an_extra_note=False)` to
  walk the pattern's *relative* steps rather than a single absolute interval list -- this is what lets a scale
  span several octaves and run in either direction (`number_of_octaves < 0` reverses and negates the steps).
  `get_key()` transposes `lowest_note` by `pattern.interval_for_signature` to get the scale's key signature.
- [`scale.py`](scale.py)'s `Scale`: a `ScalePattern` anchored on a concrete (diatonic+chromatic) `Note` tonic --
  e.g. "C melodic minor". Also carries the LilyPond rendering hooks (`_to_lily_staff()`, `to_lily_sheet()`) used
  by the piano-notation generator (see [`../../../lily/`](../../../lily/)).
- [`chromatic_scale.py`](chromatic_scale.py)'s `ChromaticScale`: the chromatic-only counterpart. It adds no
  behavior of its own -- Python's MRO resolves `get_notes()` to `AbstractScale`'s version (which only needs
  `lowest_note + interval`, valid for both `Note` and `ChromaticNote`), so
  `AbstractChromaticInstantiation.get_intervals()` (which calls `pattern.intervals_with_all_notes()`, a method
  `ScalePattern` doesn't define) is never actually reached.

Unlike [chord/](../chord/README.md), there is no separate "inversion" instantiation here: a scale doesn't get
auto-inverted the way a chord does (see [../../pattern/scale/README.md](../../pattern/scale/README.md)), so
`Scale`/`ChromaticScale` are the only two classes in this subtree.
