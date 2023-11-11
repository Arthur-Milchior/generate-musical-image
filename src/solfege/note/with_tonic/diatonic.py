import unittest

from solfege.interval import DiatonicInterval
from solfege.note import DiatonicNote
from solfege.note.with_tonic.base import _NoteWithTonic


class DiatonicNoteWithTonic(_NoteWithTonic, DiatonicNote):
    # Saved as the interval from middle C
    role = ["tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading"]


class TestDiatonicNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        n1_1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n1_1_ = DiatonicNoteWithTonic(value=1, tonic=True)
        self.assertEquals(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n2_1 = DiatonicNoteWithTonic(value=2, tonic=n1_1)
        n2_2 = DiatonicNoteWithTonic(value=2, tonic=True)
        n3_1 = DiatonicNoteWithTonic(value=3, tonic=n1_1)
        self.assertNotEquals(n2_1, n2_2)
        self.assertNotEquals(n3_1, n2_1)

    def test_self_tonic(self):
        n = DiatonicNoteWithTonic(value=1, tonic=True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = DiatonicNoteWithTonic(value=1, tonic=False)
        self.assertIsNone(n.get_tonic())

    def test_self_set_tonic(self):
        n1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n2 = DiatonicNoteWithTonic(value=2, tonic=False)
        n2.set_tonic(n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n2 = DiatonicNoteWithTonic(value=2, tonic=n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n2 = DiatonicNoteWithTonic(value=2, tonic=n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n2 = n1 + DiatonicInterval(value=2)
        self.assertEquals(n2.get_tonic(), n1)
        self.assertEquals(n2.get_number(), 3)

    def test_sub_note(self):
        n1 = DiatonicNoteWithTonic(value=1, tonic=True)
        n2 = DiatonicNoteWithTonic(value=2, tonic=n1)
        diff = n2 - n1
        self.assertEquals(diff, DiatonicInterval(1))
        with self.assertRaises(Exception):
            _ = n1 - DiatonicNoteWithTonic(value=1, tonic=n2)

    def test_subDiatonicInterval(self):
        n = DiatonicNoteWithTonic(value=1, tonic=True)
        self.assertEquals(n - DiatonicInterval(1), DiatonicNoteWithTonic(value=0, tonic=n))

    def test_get_role(self):
        C4 = DiatonicNoteWithTonic(value=0, tonic=True)
        self.assertEquals(C4.get_role(), "tonic")
        D4 = DiatonicNoteWithTonic(value=1, tonic=True)
        self.assertEquals(D4.get_role(), "tonic")
        self.assertEquals(DiatonicNoteWithTonic(value=2, tonic=D4).get_role(), "supertonic")
        self.assertEquals(DiatonicNoteWithTonic(value=8, tonic=D4).get_role(), "tonic")
        self.assertEquals(DiatonicNoteWithTonic(value=-6, tonic=D4).get_role(), "tonic")
        self.assertEquals(DiatonicNoteWithTonic(value=-7, tonic=D4).get_role(), "leading")
