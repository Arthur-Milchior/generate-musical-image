from .base import *

class TestNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        n1_1 = _NoteWithFundamental(value=1, fundamental=True)
        n1_1_ = _NoteWithFundamental(value=1, fundamental=True)
        self.assertEquals(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = _NoteWithFundamental(value=1, fundamental=True)
        n2_1 = _NoteWithFundamental(value=2, fundamental=n1_1)
        n2_2 = _NoteWithFundamental(value=2, fundamental=True)
        n3_1 = _NoteWithFundamental(value=3, fundamental=n1_1)
        self.assertNotEquals(n2_1, n2_2)
        self.assertNotEquals(n3_1, n2_1)

    def test_self_tonic(self):
        n = _NoteWithFundamental(value=1, fundamental=True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = _NoteWithFundamental(value=1, fundamental=False)
        self.assertIsNone(n.get_tonic())

    def test_self_set_tonic(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=False)
        n2.set_tonic(n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = n1 + AbstractInterval(value=2)
        self.assertEquals(n2.get_tonic(), n1)
        self.assertEquals(n2.get_number(), 3)
        self.assertEquals(n2, _NoteWithFundamental(value=3, fundamental=n1))
        with self.assertRaises(Exception):
            _ = n1 + n1

    def test_sub_note(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        diff = n2 - n1
        self.assertEquals(diff, AbstractInterval(1))
        with self.assertRaises(Exception):
            _ = n1 - _NoteWithFundamental(value=1, fundamental=n2)

    def test_sub_interval(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        self.assertEquals(n1 - AbstractInterval(1), _NoteWithFundamental(value=0, fundamental=n1))
        self.assertEquals(n2 - AbstractInterval(1), _NoteWithFundamental(value=1, fundamental=n1))
