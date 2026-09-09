# interval

The interval half of [`solfege/value/`](../README.md): the distance between two notes, in the same three
flavors as [`note/`](../note/README.md) — chromatic-only, diatonic-only, or the chromatic+diatonic pair.

## Class hierarchy

- [`abstract_interval.py`](abstract_interval.py): `AbstractInterval`, the common base for every interval
  representation. Adds an optional `_role` ([`role/`](role/README.md)) on top of
  [`../abstract.py`](../abstract.py)'s octave arithmetic — a role tags what an interval *means* in the pattern
  it came from (e.g. "the blue note"), independently of its raw size.
- [`singleton_interval.py`](singleton_interval.py): `AbstractSingletonInterval(AbstractInterval, Singleton)` —
  base for a single-int interval.
  - [`chromatic_interval.py`](chromatic_interval.py): `ChromaticInterval` — semitone count. Also defines
    `get_interval_name()`/`IntervalNameCreasing` for turning a chromatic interval into English ("second minor",
    "octave and fifth"...).
  - [`diatonic_interval.py`](diatonic_interval.py): `DiatonicInterval` — scale-degree count (ignores
    sharps/flats, so B and B# are the same diatonic interval). Has its own `get_interval_name()`.
- [`interval.py`](interval.py): `Interval(AbstractInterval, Pair[...])` — a chromatic+diatonic pair, the type
  actually used everywhere a "real" interval is needed (chord/scale definitions, note arithmetic). Key methods:
  `notation()` (compact form like `"3M"`), `get_alteration_constructor()` (picks `JustAlteration` for
  unison/fourth/fifth, `MinorMajorAlteration` otherwise — see [`alteration/`](alteration/README.md)),
  `get_role()` (falls back to `IntervalRoleFromInterval` when no explicit role was set).

`too_big_alterations_exception.py` (`TooBigAlterationException`) is raised whenever a note/interval's
alteration doesn't fit any known `Alteration` subclass (see [`alteration/`](alteration/README.md)).

## Subpackages

- [`alteration/`](alteration/README.md) — the sharp/flat-count alteration attached to an interval's diatonic
  degree.
- [`role/`](role/README.md) — the optional tag (`IntervalRole`) describing what an interval represents within
  its pattern.
- [`set/`](set/README.md) — ordered lists of intervals sharing a starting note (the shape behind chord/scale
  patterns).

## `interval_pattern.py`

`IntervalPattern(SolfegePattern)` is a pattern for a *single* interval (e.g. "Third major"), as opposed to a
chord/scale pattern which holds several — see [`../../pattern/README.md`](../../pattern/README.md) for the
shared `SolfegePattern` machinery. `intervals_up_to_octave` at the bottom of the file is the registered list of
every named interval up to an octave, both diatonic (seconds through sevenths, minor/major) and chromatic
(diminished/augmented variants).

## Dependencies

Depends on [`../note/`](../note/README.md) only inside function bodies (deferred imports), to avoid an import
cycle — see [`../../README.md`](../README.md)'s "Dependencies" note.
