from .diatonic import *

class TestDiatonicNoteWithTonic(unittest.TestCase):
    C4 = DiatonicNoteWithFundamental(value=0, fundamental=True)
    D4 = DiatonicNoteWithFundamental(value=1, fundamental=C4)
    B3 = DiatonicNoteWithFundamental(value=-1, fundamental=C4)
    E4 = DiatonicNoteWithFundamental(value=2, fundamental=C4)
    F4 = DiatonicNoteWithFundamental(value=3, fundamental=C4)
    C5 = DiatonicNoteWithFundamental(value=7, fundamental=C4)
    B4 = DiatonicNoteWithFundamental(value=6, fundamental=C4)
    D3 = DiatonicNoteWithFundamental(value=-6, fundamental=C4)
    C3 = DiatonicNoteWithFundamental(value=-7, fundamental=C4)
    B2 = DiatonicNoteWithFundamental(value=-8, fundamental=C4)

    def test_eq(self):
        n1_1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n1_1_ = DiatonicNoteWithFundamental(value=1, fundamental=True)
        self.assertEquals(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n2_1 = DiatonicNoteWithFundamental(value=2, fundamental=n1_1)
        n2_2 = DiatonicNoteWithFundamental(value=2, fundamental=True)
        n3_1 = DiatonicNoteWithFundamental(value=3, fundamental=n1_1)
        self.assertNotEquals(n2_1, n2_2)
        self.assertNotEquals(n3_1, n2_1)

    def test_self_tonic(self):
        n = DiatonicNoteWithFundamental(value=1, fundamental=True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = DiatonicNoteWithFundamental(value=1, fundamental=False)
        self.assertIsNone(n.get_tonic())

    def test_self_set_tonic(self):
        n1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n2 = DiatonicNoteWithFundamental(value=2, fundamental=False)
        n2.set_tonic(n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n2 = DiatonicNoteWithFundamental(value=2, fundamental=n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n2 = DiatonicNoteWithFundamental(value=2, fundamental=n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n2 = n1 + DiatonicInterval(value=2)
        self.assertEquals(n2.get_tonic(), n1)
        self.assertEquals(n2.get_number(), 3)

    def test_sub_note(self):
        n1 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        n2 = DiatonicNoteWithFundamental(value=2, fundamental=n1)
        diff = n2 - n1
        self.assertEquals(diff, DiatonicInterval(1))
        with self.assertRaises(Exception):
            _ = n1 - DiatonicNoteWithFundamental(value=1, fundamental=n2)

    def test_subDiatonicInterval(self):
        n = DiatonicNoteWithFundamental(value=1, fundamental=True)
        self.assertEquals(n - DiatonicInterval(1), DiatonicNoteWithFundamental(value=0, fundamental=n))

    def test_get_role(self):
        C4 = DiatonicNoteWithFundamental(value=0, fundamental=True)
        self.assertEquals(C4.get_role(), "tonic")
        D4 = DiatonicNoteWithFundamental(value=1, fundamental=True)
        self.assertEquals(D4.get_role(), "tonic")
        self.assertEquals(DiatonicNoteWithFundamental(value=2, fundamental=D4).get_role(), "supertonic")
        self.assertEquals(DiatonicNoteWithFundamental(value=8, fundamental=D4).get_role(), "tonic")
        self.assertEquals(DiatonicNoteWithFundamental(value=-6, fundamental=D4).get_role(), "tonic")
        self.assertEquals(DiatonicNoteWithFundamental(value=-7, fundamental=D4).get_role(), "leading")

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
