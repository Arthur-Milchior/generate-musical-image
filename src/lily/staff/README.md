# staff

The lowest layer of LilyPond piano-notation generation: the code for **one staff** (one clef, one key
signature, one line of notes), before it's wrapped into a full sheet by [`../sheet/`](../sheet/).

- [`lily_staff.py`](lily_staff.py): `LilyStaff`, the abstract base — holds `clef`/`first_key` and renders the
  shared `\new Staff{...}` wrapper (`staff_lily_code()`); each subclass only has to implement `staff_content()`
  for the notes inside. Also `FakeLilyStaff`, a test double with a fixed content string.
- [`lily_chord_staff.py`](lily_chord_staff.py): `LilyChordStaff` — renders a list of `notes` stacked as a single
  simultaneous chord (`<...>`), with automatic `\ottava` shifting (`get_ottava()`/`get_8_va()`/`get_8_vb()`) when
  the chord falls outside the staff's normal range for its clef.
- [`lily_single_note_staff.py`](lily_single_note_staff.py): `LilySingleNoteStaff`, a `LilyChordStaff` specialized
  to exactly one note, with its own `get_8_va()`/`get_8_vb()` computing the actual ambitus thresholds (treble:
  E3-F6, bass: C2-F4).
- [`lily_scale_staff.py`](lily_scale_staff.py): `LilyScaleStaff` — renders a list of `notes` as a melodic
  sequence (space-separated), not a chord.

All of these are `DataClassWithDefaultArgument`s (see [`../../utils/README.md`](../../utils/README.md)) and are
constructed with `.make(...)`, not called directly. They only produce LilyPond source text; compiling that text
to SVG is handled one layer down in [`../../_lily/lily.py`](../../_lily/lily.py), and combining staves into a
full sheet is handled one layer up in [`../sheet/`](../sheet/).
