# value

The class hierarchy for every musical *value* used elsewhere in `solfege`: notes and intervals, in three
flavors each — chromatic-only, diatonic-only, or the chromatic+diatonic pair that most other code actually
uses. `key/` builds on top of `note/` for key signatures.

## Class hierarchy

The files directly under `value/` define the shared abstractions that `note/` and `interval/` both build on:

- [`abstract.py`](abstract.py): `Abstract` — the common root for every note/interval representation. Factors
  out octave arithmetic (`add_octave`, `in_base_octave`, `equals_modulo_octave`, `is_in_base_octave`) and the
  `+`/`-` glue (`__radd__`, `__sub__` defined as `self + (-other)`). Declares the abstract `octave()`/
  `one_octave()` that subclasses must implement.
- [`singleton.py`](singleton.py): `Singleton(Abstract)` — base for a value represented by a single int (a
  count of semitones or scale degrees). `Chromatic`/`Diatonic` are its direct subclasses; comparison
  (`__eq__`/`__lt__`/`__le__`) and hashing are by that raw `value`.
- [`chromatic.py`](chromatic.py) / [`diatonic.py`](diatonic.py): `Chromatic`/`Diatonic` — the two concrete
  single-int representations, with no information about the other axis. `ChromaticNote`/`ChromaticInterval`
  and `DiatonicNote`/`DiatonicInterval` (in `note/`/`interval/`) are their respective subclasses.
- [`pair.py`](pair.py): `Pair(Abstract, Generic[ChromaticType, DiatonicType, AlterationType])` — base for a
  value holding *both* a chromatic and a diatonic component together (`_chromatic`/`_diatonic`), which is what
  distinguishes e.g. G# from Ab even though they share a chromatic value. `Note` and `Interval` are its
  concrete subclasses. Key methods: `from_chromatic()`/`all_from_chromatic()` (guess/enumerate diatonic
  spellings of a chromatic value), `from_diatonic()` (the reverse, assuming a major scale), and
  `get_alteration()` (the gap between the diatonic component's "natural" chromatic value and the actual one,
  as an `Alteration` — see [`interval/alteration/`](interval/alteration/README.md)).
- [`getters.py`](getters.py): `ChromaticGetter`/`DiatonicGetter` — tiny `Generic[T]` protocols declaring
  `get_chromatic()`/`get_diatonic()`, mixed into both `Singleton` subclasses (returning `self`) and `Pair`
  subclasses (returning the matching component).

## Subpackages

- [`note/`](note/README.md) — notes (an absolute pitch): `ChromaticNote`, `DiatonicNote`, `Note`.
- [`note/set/`](note/set/README.md) — ordered lists of notes, e.g. the notes making up a chord or scale.
- [`interval/`](interval/README.md) — intervals (the distance between two notes): `ChromaticInterval`,
  `DiatonicInterval`, `Interval`; plus `alteration/`, `role/` and `set/` subpackages.
- [`key/`](key/README.md) — key signatures (`Key`): a tonic `Note` plus how many flats/sharps that implies.

## Dependencies

`key` depends on `note`, which depends on `interval` (which depends on the files directly under `value/`
described above). Where the reverse is needed (e.g. `Pair.get_alteration()` needing an `Alteration` class
defined under `interval/`), the import is deferred to inside a function body to avoid a cycle — see
[`../README.md`](../README.md).
