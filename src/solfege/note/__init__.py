from solfege.note.alteration import Alteration
from solfege.note.chromatic import ChromaticNote
from solfege.note.diatonic import DiatonicNote
from solfege.note.note import Note
from utils.util import tests_modules

from solfege.note import abstract, alteration, chromatic, diatonic, note, set_of_notes

ChromaticNote.RelatedDiatonicClass = DiatonicNote
DiatonicNote.RelatedChromaticClass = ChromaticNote
ChromaticNote.RelatedSolfegeClass = Note
ChromaticNote.AlterationClass = Alteration
