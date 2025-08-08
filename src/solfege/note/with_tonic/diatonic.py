
from solfege.interval import DiatonicInterval
from solfege.note import DiatonicNote
from solfege.note.with_tonic.base import AbstractNoteWithTonic


class DiatonicNoteWithTonic(AbstractNoteWithTonic, DiatonicNote):
    # Saved as the interval from middle C
    role = ["tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading"]


