# note

A note (an absolute pitch, as opposed to [`../interval/`](../interval/README.md)'s distance between two
notes), in the same three flavors used throughout `value/`: chromatic-only, diatonic-only, or the
chromatic+diatonic pair that most other code actually uses.

## Class hierarchy

- [`abstract_note.py`](abstract_note.py): `AbstractNote(Abstract, Generic[IntervalType])` — the common base
  for every note representation. Adds a note to an interval (`__add__`, abstract) and subtracts either an
  interval (yielding a note) or another note (yielding an interval, via the `__sub__` overloads). Also defines
  the shared name-formatting entry point `get_name_with_octave()` (letter/number/French/LilyPond name plus
  octave marker) and the `AlterationOutput`/`NoteOutput`/`OctaveOutput`/`FixedLengthOutput` enums controlling
  how that text is rendered. `low_and_high()`/`pinky_and_thumb_side()` are free functions ordering a pair of
  notes (by pitch, or by which hand-side plays them).
- [`singleton_note.py`](singleton_note.py): `AbstractSingletonNote(AbstractNote, Singleton)` — base for a
  single-int note (chromatic-only or diatonic-only); `__add__`/`__sub__` operate on the raw int `value`.
  - [`chromatic_note.py`](chromatic_note.py): `ChromaticNote` — a note as a semitone count from middle C.
    Can't distinguish enharmonic spellings (G# vs Ab) on its own; `get_note()`/`non_ambiguous_string_for_file_name()`
    guess a diatonic spelling via `Note.from_chromatic()` when one is needed. Also defines
    `is_white_key_on_piano()`/`is_black_key_on_piano()`.
  - [`diatonic_note.py`](diatonic_note.py): `DiatonicNote` — a note as a scale-degree count from middle C
    (ignores sharps/flats, so B and B# are the same diatonic note).
- [`note.py`](note.py): `Note(AbstractNote, Pair[ChromaticNote, DiatonicNote, NoteAlteration], ...)` — a
  chromatic+diatonic pair, the type actually used everywhere a "real" note is needed. Key methods:
  `from_name()`/`__repr__` (parse/print names like `"C#4"`), `simplest_enharmonic()`/`canonize()` (pick a
  simpler enharmonic spelling), `adjacent()` (within two semitones), `change_octave_to_be_enharmonic()`
  (shift by whole octaves to match a given chromatic note), and the piano-key/lily helpers.
- [`note_alteration.py`](note_alteration.py): `NoteAlteration(Alteration)` — the sharp/flat-count offset
  attached to a note (as opposed to `IntervalAlteration`, attached to an interval's diatonic degree — see
  [`../interval/alteration/README.md`](../interval/alteration/README.md)). Ranges from double flat (-2) to
  double sharp (+2); `NATURAL`/`SHARP`/`FLAT`/`DOUBLE_SHARP`/`DOUBLE_FLAT` are the module-level singletons.
- [`clef.py`](clef.py): `Clef` — `TREBLE`/`BASS`, used when picking which staff to render a note on.

## Subpackage

- [`set/`](set/README.md) — ordered lists of notes, e.g. the notes making up a chord or scale.

## Dependencies

Depends on [`../interval/`](../interval/README.md) (a note's difference is an interval, and a note is built
from/decomposed into intervals) and on the base classes directly under [`../`](../README.md) (`Abstract`,
`Pair`, `Singleton`, `Chromatic`, `Diatonic`). Depended on by [`../key/`](../key/README.md) (a key's tonic is
a `Note`).
