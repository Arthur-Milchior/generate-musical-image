"""Package marker for `solfege.value.note`: notes, represented as chromatic-only (`ChromaticNote`),
diatonic-only (`DiatonicNote`), or paired (`Note`). Eagerly imports the concrete note modules and the
`solfege.value.note.set` subpackage for their module-level registrations."""

import solfege.value.note.note
import solfege.value.note.chromatic_note
import solfege.value.note.diatonic_note
import solfege.value.note.set
