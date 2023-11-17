from solfege.note.alteration import Alteration
from solfege.note.chromatic import ChromaticNote
from solfege.note.diatonic import DiatonicNote
from solfege.note.note import Note

ChromaticNote.RelatedDiatonicClass = DiatonicNote
DiatonicNote.RelatedChromaticClass = ChromaticNote
ChromaticNote.RelatedSolfegeClass = Note
ChromaticNote.AlterationClass = Alteration
