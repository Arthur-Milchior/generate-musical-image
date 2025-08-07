from .note import *

class TestNoteWithTonic(unittest.TestCase):
    C4 = NoteWithTonic(chromatic=0, diatonic = 0, fundamental=True)
    D4 = NoteWithTonic(chromatic=2, diatonic = 1, fundamental=C4)
    B3 = NoteWithTonic(chromatic=-1, diatonic = -1, fundamental=C4)
    E4 = NoteWithTonic(chromatic=4, diatonic = 2, fundamental=C4)
    F4 = NoteWithTonic(chromatic=5, diatonic = 3, fundamental=C4)
    C5 = NoteWithTonic(chromatic=12, diatonic = 7, fundamental=C4)
    B4 = NoteWithTonic(chromatic=11, diatonic = 6, fundamental=C4)
    D3 = NoteWithTonic(chromatic=-10, diatonic = 6, fundamental=C4)
    C3 = NoteWithTonic(chromatic=-12, diatonic = -7, fundamental=C4)
    B2 = NoteWithTonic(chromatic=-13, diatonic = -8, fundamental=C4)
    def test_eq(self):
        zero = NoteWithTonic(chromatic=0, diatonic=0, fundamental=True)
        self.assertEquals(zero.get_chromatic().get_number(), 0)
        self.assertEquals(zero.get_diatonic().get_number(), 0)
        self.assertEquals(zero.get_tonic(), zero)

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
