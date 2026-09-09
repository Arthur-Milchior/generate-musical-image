# set

An ordered list of notes — e.g. the concrete notes making up a chord or scale once a
[`../../interval/set/`](../../interval/set/README.md) pattern has been anchored to a tonic (via
`AbstractIntervalListPattern.from_note()`).

## Class hierarchy

- [`abstract_note_list.py`](abstract_note_list.py): `AbstractNoteList(DataClassWithDefaultArgument, Generic[...])`
  — the common base, generic over the note/interval/interval-list-pattern types it's built from. Holds
  `notes` (a `FrozenList`) and `list_order` (`ListOrder.INCREASING`/`DECREASING`/`NOT`, see
  [`../../../list_order.py`](../../../list_order.py)), enforced in `__post_init__`. Key methods:
  `interval_list_from_min_note()` (the intervals from the lowest note to each note, requires increasing
  order), `is_in_base_octave()`/`all_blacks()`, `__reversed__` (flips `list_order` too), and `add_octave()`.
- [`chromatic_note_list.py`](chromatic_note_list.py): `ChromaticNoteList` — holds `ChromaticNote`s only.
- [`note_list.py`](note_list.py): `NoteList` — holds full `Note`s (chromatic+diatonic). Adds the LilyPond
  chord-rendering helpers (`lily_chord()`, `lily_file_with_only_chord()`, `lily_file_name()`),
  `chromatic()` (drop diatonic spelling, returning a `ChromaticNoteList`),
  `find_note_from_list_up_to_octave()`/`change_octave_to_be_enharmonic()` (match this list's notes against a
  `ChromaticNoteList`, up to octave), and `easy_key()` (sum of each note's easiness, for picking the simplest
  chord voicing).

## Dependencies

Depends on [`../`](../README.md) (the note types held by these lists) and
[`../../interval/set/`](../../interval/set/README.md) (each list's matching interval-list-pattern type, used
by `interval_list_from_min_note()`).
