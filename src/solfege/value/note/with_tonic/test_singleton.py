import unittest

from solfege.value.interval.singleton_interval import AbstractSingletonInterval
from solfege.value.note.with_tonic.singleton import AbstractSingletonNoteWithTonic

class TestSingletonNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        n1_1 = AbstractSingletonNoteWithTonic.make(1, True)
        n1_1_ = AbstractSingletonNoteWithTonic.make(1, True)
        self.assertEqual(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = AbstractSingletonNoteWithTonic.make(1, True)
        n2_1 = AbstractSingletonNoteWithTonic.make(2, n1_1)
        n2_2 = AbstractSingletonNoteWithTonic.make(2, True)
        n3_1 = AbstractSingletonNoteWithTonic.make(3, n1_1)
        self.assertNotEqual(n2_1, n2_2)
        self.assertNotEqual(n3_1, n2_1)

    def test_self_tonic(self):
        n = AbstractSingletonNoteWithTonic.make(1, True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = AbstractSingletonNoteWithTonic.make(1, False)
        self.assertIsNone(n.get_tonic())

    # def test_self_set_tonic(self):
    #     n1 = AbstractSingletonNoteWithTonic.make(1, True)
    #     n2 = AbstractSingletonNoteWithTonic.make(2, False)
    #     n2.set_tonic(n1)
    #     self.assertEqual(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = AbstractSingletonNoteWithTonic.make(1, True)
        n2 = AbstractSingletonNoteWithTonic.make(2, n1)
        self.assertEqual(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = AbstractSingletonNoteWithTonic.make(1, True)
        n2 = AbstractSingletonNoteWithTonic.make(2, n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = AbstractSingletonNoteWithTonic.make(1, True)
        n2 = n1 + AbstractSingletonInterval(value=2)
        self.assertEqual(n2.get_tonic(), n1)
        self.assertEqual(n2.value, 3)
        self.assertEqual(n2, AbstractSingletonNoteWithTonic.make(3, n1))
        with self.assertRaises(Exception):
            _ = n1 + n1

    def test_sub_note(self):
        n1 = AbstractSingletonNoteWithTonic.make(1, True)
        n2 = AbstractSingletonNoteWithTonic.make(2, n1)
        diff = n2 - n1
        self.assertEqual(diff, AbstractSingletonInterval(1))
        with self.assertRaises(Exception):
            _ = n1 - AbstractSingletonNoteWithTonic.make(1, n2)

    def test_sub_interval(self):
        n1 = AbstractSingletonNoteWithTonic.make(1, True)
        n2 = AbstractSingletonNoteWithTonic.make(2, n1)
        self.assertEqual(n1 - AbstractSingletonInterval(1), AbstractSingletonNoteWithTonic.make(0, n1))
        self.assertEqual(n2 - AbstractSingletonInterval(1), AbstractSingletonNoteWithTonic.make(1, n1))
