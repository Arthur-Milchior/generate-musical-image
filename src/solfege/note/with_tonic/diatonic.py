import unittest

from solfege.interval import DiatonicInterval
from solfege.note import DiatonicNote
from solfege.note.with_tonic.base import _NoteWithFundamental


class DiatonicNoteWithFundamental(_NoteWithFundamental, DiatonicNote):
    # Saved as the interval from middle C
    role = ["tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading"]


