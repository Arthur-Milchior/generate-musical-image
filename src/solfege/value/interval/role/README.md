# role

An `IntervalRole` is an optional tag attached to an `Interval` (via its `_role` field, see
[`../abstract_interval.py`](../abstract_interval.py)) describing what that interval *means* within the pattern
it came from — independently of its raw chromatic/diatonic size. The main use is labelling notes on generated
fretted-instrument diagrams (`text_for_guitar_image()`).

## Classes

- [`interval_role.py`](interval_role.py): `IntervalRole`, the abstract base — just one abstract method,
  `text_for_guitar_image() -> str`.
- [`interval_role_from_interval.py`](interval_role_from_interval.py): `IntervalRoleFromInterval` — the default
  role, derived straight from the interval itself: its 1-based diatonic degree plus alteration letter (e.g.
  `"3M"`). Used by `Interval.get_role()` whenever no explicit role was set.
- [`interval_role_from_string.py`](interval_role_from_string.py): `IntervalRoleFromString` — a role whose label
  is an arbitrary given string. Also defines `blue_role` (label `"b"`, for the blues-scale blue note) and
  `role_from_interval_index(i)` (label = plain scale-degree index, for degrees with no more specific role).

## Dependencies

`interval_role_from_interval.py` depends on [`../interval.py`](../interval.py) (an `Interval` is what it wraps);
`interval_role.py`/`interval_role_from_string.py` don't depend on the rest of `interval/`.
