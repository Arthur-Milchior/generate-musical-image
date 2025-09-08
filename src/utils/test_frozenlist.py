from utils.frozenlist import *
import unittest

class TestFrozenList(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(FrozenList([]), FrozenList([]))
        self.assertNotEqual(FrozenList([]), FrozenList([1]))

    def test_append(self):
        self.assertEqual(FrozenList([]).append(1), FrozenList([1]))

    def test_add(self):
        self.assertEqual(FrozenList([]) + [1], FrozenList([1]))
        self.assertEqual(FrozenList([]) + FrozenList([1]), FrozenList([1]))

    def test_iter(self):
        self.assertEqual(list(FrozenList([1])), [1])

    def test_len(self):
        self.assertEqual(len(FrozenList([1])), 1)

    def test_bool(self):
        self.assertTrue(FrozenList([1]))
        self.assertFalse(FrozenList([]))

    def test_tail_head(self):
        self.assertEqual(FrozenList([1]).head_tail(), (1, FrozenList([])))
        with self.assertRaises(Exception):
            FrozenList([]).head_tail()

    def test_repr(self):
        self.assertEqual(repr(FrozenList([1])), "FrozenList([1])")