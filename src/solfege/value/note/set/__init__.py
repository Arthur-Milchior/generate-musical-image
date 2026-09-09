"""Package marker for `solfege.value.note.set`: ordered lists of notes (`NoteList` for
chromatic+diatonic, `ChromaticNoteList` for chromatic-only), such as the notes making up a chord
or scale. Eagerly imports both modules for their module-level registrations."""

import solfege.value.note.set.note_list
import solfege.value.note.set.chromatic_note_list
