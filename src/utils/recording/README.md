# Recording: looking patterns up by their interval content

This package answers "given a set of intervals, which pattern(s) have exactly that shape?" — the reverse
direction from normal attribute access. It backs `SolfegePattern.get_from_name(...)`'s sibling lookup, used e.g.
to identify a chord from the notes a user played.

## Pieces

- [`record_keeper.py`](record_keeper.py) — `RecordKeeper[KeyType, RecordedType, RecordedContainerType]`: a dict
  from `KeyType` (typically an `IntervalList`) to a `RecordedContainerType` holding the pattern(s) registered
  under that key. `register(key, recorded)` asserts `is_key_valid(key)` first — subclasses implement that to
  reject keys outside what they're willing to index (e.g. chord/scale record keepers reject anything spanning
  more than an octave; see [../../solfege/pattern/multi_octave_patterns.md](../../solfege/pattern/multi_octave_patterns.md)).
- [`recorded_container.py`](recorded_container.py) / [`recording_var_type.py`](recording_var_type.py) — the
  abstract container interface and its type variable.
- [`singleton_container.py`](singleton_container.py) — `SingletonContainer[RecordedType]`, a `RecordedContainer`
  holding **at most one** value, with a `SameKeyBehavior` policy for what happens when a second value tries to
  claim the same key: `IMPOSSIBLE` (assert-fail — used by scales: two `ScalePattern`s can never share a shape),
  `ASSERT_SAME` (fine only if it's literally equal), `MINIMUM`/`REPLACE`/`IGNORE` (pick a winner). Chords use a
  plain `list` container instead of `SingletonContainer`, since several differently-named chords legitimately
  share one interval shape.
- [`recordable.py`](recordable.py) — `Recordable[KeyType, RecordKeeperType]` mixin: gives a class a
  lazily-created, class-level `RecordKeeper` (`get_record_keeper()`) and `_associate_keys_to_self()`, which
  registers `self` under `self.get_interval_lists()`. This is what
  [`PatternWithIntervalLists.__post_init__`](../../solfege/pattern/pattern_with_interval_lists.py) calls whenever
  a pattern is constructed with `record=True`.

## Debugging a registration assertion

If a pattern definition fails with an assertion inside [`record_keeper.py`](record_keeper.py) (`is_key_valid`)
or [`singleton_container.py`](singleton_container.py) (`SameKeyBehavior.IMPOSSIBLE`), it means either:
- the pattern's interval list falls outside what that record keeper accepts (most often: it spans an octave or
  more — see [../../solfege/pattern/multi_octave_patterns.md](../../solfege/pattern/multi_octave_patterns.md)
  for the fix), or
- an identical shape is already registered under a `SingletonContainer` (scales only) — add the new name to the
  existing pattern's `names` instead of creating a duplicate (see
  [../../solfege/pattern/scale/README.md](../../solfege/pattern/scale/README.md)).
