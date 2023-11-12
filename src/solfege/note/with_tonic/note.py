import unittest

from solfege.interval.interval import Interval
from solfege.note import Note, DiatonicNote, ChromaticNote
from solfege.note.with_tonic import ChromaticNoteWithTonic


class NoteWithTonic(ChromaticNoteWithTonic, Note):
    """A note of the scale, as an interval from middle C."""

    IntervalClass = Interval
    DiatonicClass = DiatonicNote
    ChromaticClass = ChromaticNote
    #
    # def get_interval_name(self, forFile=None):
    #     """The name of this note.
    #
    #     Args: `forFile` -- whether we should avoid non ascii symbol"""
    #     diatonic = self.get_diatonic()
    #     try:
    #         alteration = self.get_alteration()
    #     except TooBigAlteration as tba:
    #         tba.addInformation("Note", self)
    #         raise
    #     diatonicName = diatonic.get_interval_name().upper()
    #     alterationName = alteration.get_interval_name(forFile=forFile)
    #     return "%s%s" % (diatonicName, alterationName)
    #
    # def correctAlteration(self):
    #     return self.get_alteration().printable()


class TestNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        zero = NoteWithTonic(chromatic=0, diatonic=0, tonic=True)
        self.assertEquals(zero.get_chromatic().get_number(), 0)
        self.assertEquals(zero.get_diatonic().get_number(), 0)
        self.assertEquals(zero.get_tonic(), zero)
