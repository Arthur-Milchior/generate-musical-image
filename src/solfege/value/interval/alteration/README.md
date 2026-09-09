# alteration

The sharp/flat-count offset applied on top of a "natural" diatonic value — the `+1` in `G# = G + 1 semitone`,
or the `-1` in a diminished fifth relative to a just fifth.

## Class hierarchy

- [`alteration.py`](alteration.py): `Alteration(ChromaticInterval, ClassWithEasyness[int])` — the common base.
  An alteration *is* a `ChromaticInterval` (its `value` is the raw semitone offset), constrained to
  `[min_value, max_value]` (declared by each subclass); building one outside that range raises
  `TooBigAlterationException` (defined in [`../too_big_alterations_exception.py`](../too_big_alterations_exception.py)).
  `easy_key()` ranks natural (0) as easiest, then single sharp/flat, then double.
- [`../interval_alteration.py`](../interval_alteration.py): `IntervalAlteration(Alteration)` — alterations used
  on an `Interval`'s diatonic degree. Adds `letter()`/`name()` (abstract) plus `Name()`/`NAME()` helpers.
  - [`just_alteration.py`](just_alteration.py): `JustAlteration` — for the "perfect" degrees (unison, fourth,
    fifth): diminished/just/augmented only, `value` in `[-1, 1]`.
  - [`minor_major_alteration.py`](minor_major_alteration.py): `MinorMajorAlteration` — for every other degree
    (second, third, sixth, seventh): diminished/minor/major/augmented, `value` in `[-2, 1]`.
  - [`wrong_alteration.py`](wrong_alteration.py): `WrongAlteration` — a placeholder returned instead of raising,
    when `Pair.get_alteration(throw=False)` is asked for an out-of-range alteration; its `letter()`/`name()`
    just print the raw offset.

Which of `JustAlteration`/`MinorMajorAlteration` applies to a given `Interval` is decided by
`Interval.get_alteration_constructor()` in [`../interval.py`](../interval.py), based on the diatonic degree.

There is a second, note-side family of alterations (`NoteAlteration`) in
[`../../note/note_alteration.py`](../../note/note_alteration.py) — same idea (a constrained `ChromaticInterval`
offset), used for notes rather than interval degrees.
