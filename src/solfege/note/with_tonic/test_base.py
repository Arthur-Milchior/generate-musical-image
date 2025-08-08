import unittest
from .base import *

class TestNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        n1_1 = AbstractNoteWithTonic(value=1, tonic=True)
        n1_1_ = AbstractNoteWithTonic(value=1, tonic=True)
        self.assertEqual(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2_1 = AbstractNoteWithTonic(value=2, tonic=n1_1)
        n2_2 = AbstractNoteWithTonic(value=2, tonic=True)
        n3_1 = AbstractNoteWithTonic(value=3, tonic=n1_1)
        self.assertNotEqual(n2_1, n2_2)
        self.assertNotEqual(n3_1, n2_1)

    def test_self_tonic(self):
        n = AbstractNoteWithTonic(value=1, tonic=True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = AbstractNoteWithTonic(value=1, tonic=False)
        self.assertIsNone(n.get_tonic())

    def test_self_set_tonic(self):
        n1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2 = AbstractNoteWithTonic(value=2, tonic=False)
        n2.set_tonic(n1)
        self.assertEqual(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2 = AbstractNoteWithTonic(value=2, tonic=n1)
        self.assertEqual(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2 = AbstractNoteWithTonic(value=2, tonic=n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2 = n1 + AbstractInterval(value=2)
        self.assertEqual(n2.get_tonic(), n1)
        self.assertEqual(n2.get_number(), 3)
        self.assertEqual(n2, AbstractNoteWithTonic(value=3, tonic=n1))
        with self.assertRaises(Exception):
            _ = n1 + n1

    def test_sub_note(self):
        n1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2 = AbstractNoteWithTonic(value=2, tonic=n1)
        diff = n2 - n1
        self.assertEqual(diff, AbstractInterval(1))
        with self.assertRaises(Exception):
            _ = n1 - AbstractNoteWithTonic(value=1, tonic=n2)

    def test_sub_interval(self):
        n1 = AbstractNoteWithTonic(value=1, tonic=True)
        n2 = AbstractNoteWithTonic(value=2, tonic=n1)
        self.assertEqual(n1 - AbstractInterval(1), AbstractNoteWithTonic(value=0, tonic=n1))
        self.assertEqual(n2 - AbstractInterval(1), AbstractNoteWithTonic(value=1, tonic=n1))
