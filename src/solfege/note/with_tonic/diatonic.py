import unittest

from solfege.interval import DiatonicInterval
from solfege.note import DiatonicNote
from solfege.note.with_tonic.base import _NoteWithTonic


class DiatonicNoteWithTonic(_NoteWithTonic, DiatonicNote):
    # Saved as the interval from middle C
    role = ["tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading"]


class TestDiatonicNoteWithTonic(unittest.TestCase):
    C4 = DiatonicNoteWithTonic(value=0, tonic=True)
    D4 = DiatonicNoteWithTonic(value=1, tonic=C4)
    B3 = DiatonicNoteWithTonic(value=-1, tonic=C4)
    E4 = DiatonicNoteWithTonic(value=2, tonic=C4)
    F4 = DiatonicNoteWithTonic(value=3, tonic=C4)
    C5 = DiatonicNoteWithTonic(value=7, tonic=C4)
    B4 = DiatonicNoteWithTonic(value=6, tonic=C4)
    D3 = DiatonicNoteWithTonic(value=-6, tonic=C4)
    C3 = DiatonicNoteWithTonic(value=-7, tonic=C4)
    B2 = DiatonicNoteWithTonic(value=-8, tonic=C4)

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

    def test_get_octave(self):
        self.assertEquals(self.C4.get_octave(), 0)
        self.assertEquals(self.B4.get_octave(), 0)
        self.assertEquals(self.D3.get_octave(), -1)
        self.assertEquals(self.C3.get_octave(), -1)
        self.assertEquals(self.B2.get_octave(), -2)
        self.assertEquals(self.C5.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(self.C5.add_octave(-1), self.C4)
        self.assertEquals(self.C4.add_octave(1), self.C5)
        self.assertEquals(self.C5.add_octave(-2), self.C3)
        self.assertEquals(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        self.assertEquals(self.C5.get_in_base_octave(), self.C4)
        self.assertEquals(self.C3.get_in_base_octave(), self.C4)
        self.assertEquals(self.C4.get_in_base_octave(), self.C4)
        self.assertEquals(self.D4.get_in_base_octave(), self.D4)
        self.assertEquals(self.B3.get_in_base_octave(), self.B4)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.D4.equals_modulo_octave(self.C4))
        self.assertFalse(self.D4.equals_modulo_octave(self.C5))
        self.assertFalse(self.D4.equals_modulo_octave(self.C3))
        self.assertFalse(self.D4.equals_modulo_octave(self.B3))
        self.assertTrue(self.C4.equals_modulo_octave(self.C4))
        self.assertTrue(self.C4.equals_modulo_octave(self.C5))
        self.assertTrue(self.C4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C5.equals_modulo_octave(self.C3))
