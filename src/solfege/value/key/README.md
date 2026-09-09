# key

Key signatures: which note is the tonic, and how many flats/sharps that implies.

## Classes

- [`key.py`](key.py): `Key(DataClassWithDefaultArgument)` — a tonic `Note` plus `number_of_flats`/
  `number_of_sharps`. Keys order by "simplicity" (`__le__`/`__lt__` compare by alteration count then note), and
  every constructed `Key` self-registers into the class-level `_from_note` map so `Key.from_note(note)` can find
  it later — construction order therefore matters (see [`keys.py`](keys.py)). `simplest_enharmonic_major()`/
  `simplest_enharmonic_minor()` return the enharmonically-equivalent key with the fewest alterations (e.g. C
  major instead of B# major), using the `_key_to_simplest_enharmonic` map populated by
  `Key.add_enharmonic_set()`.
- [`keys.py`](keys.py): module-level registry — constructs every key up to a wide range of enharmonic
  spellings, groups them into `sets_of_enharmonic_keys` (each group registered via `add_enharmonic_set`), and
  exposes the `Interval` shift from "playing a C scale" to each standard key signature (`one_sharp`,
  `two_flats`, ... `height_flats`), used when drawing key signatures.

## Dependencies

Depends on [`../note/`](../note/README.md) (a key's tonic is a `Note`) and
[`../interval/`](../interval/README.md) (signature shifts, relative-major lookup). See
[`../README.md`](../README.md#dependencies) for the overall `key` → `note` → `interval` dependency direction.
