import unittest

from solfege.note import ChromaticNote
from solfege.note.with_tonic.base import _NoteWithTonic


class ChromaticNoteWithTonic(_NoteWithTonic, ChromaticNote):
    # The role this note is most likely to play in the standard chords
    # Especially used for guitar cards
    role = ["unison", None, None, "third", "third", "third", "fifth", "fifth", "fifth", "interval", "interval",
            "interval"]


    def get_color(self, color=True):
        if color:
            dic = {"unison": "black", "third": "violet", "fifth": "red", "interval": "green", None: None}
            return dic[self.get_role()]
        else:
            return "black"

class TestChromaticNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        zero = ChromaticNoteWithTonic(chromatic=0, tonic=True)
        self.assertEquals(zero.get_number(), 0)
        self.assertEquals(zero.get_tonic(), zero)

    # def get_diatonic(self):
    #     """Assuming no base is used"""
    #     if "diatonic" not in self.dic:
    #         if self.get_number() is None:
    #             diatonic = None
    #         elif self.get_tonic() is None:
    #             raise Exception("Diatonic asked when the current note %s has no base" % self)
    #         elif self == self.get_tonic():
    #             # If we can't use the base to determine the diatonic note, we take the more likely one
    #             diatonic = super().get_diatonic()
    #             diatonic.set_tonic(diatonic)
    #         else:
    #             # Otherwise, we use the role to figure out which diatonic note to use
    #             role = self.get_role()
    #             diatonicNumber = {"unison": 0, "third": 2, "fifth": 4, "interval": 6}[role]
    #             diatonicIntervalBaseOctave = DiatonicInterval(diatonic=diatonicNumber)
    #             octave = self.get_interval().get_octave()
    #             diatonicInterval = diatonicIntervalBaseOctave.add_octave(octave)
    #             diatonic = self.base.get_diatonic() + diatonicInterval
    #             diatonic.set_tonic(self.base.get_diatonic())
    #             debug("Note %s's diatonic is not base. Its interval is %s and its diatonic is %s" % (
    #             self, diatonicInterval, diatonic))
    #         self.dic["diatonic"] = diatonic
    #     return self.dic["diatonic"]
    #
    # def get_note(self):
    #     note = super().get_note(clazz=NoteWithBase)
    #     tonic = self.get_tonic()
    #     if self is tonic:
    #         note.set_tonic(note)
    #     elif tonic is not None:
    #         note.set_tonic(tonic.get_note())
    #     return note