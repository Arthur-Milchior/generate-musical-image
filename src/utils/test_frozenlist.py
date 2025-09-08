from utils.frozenlist import *
import unittest

@dataclass
class FakeType(MakeableWithSingleArgument):
    value: int

    @classmethod
    def _make_single_argument(cls, arg) -> Self:
        assert_typing(arg, int)
        return FakeType(arg)

    def repr_single_argument(self) -> str:
        return f"{self.value}"
    
class FakeFrozenList(FrozenList[FakeType]):
    type = FakeType


class TestFakeFrozenList(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(FakeFrozenList([]), FakeFrozenList([]))
        self.assertNotEqual(FakeFrozenList([]), FakeFrozenList([1]))

    def test_append(self):
        self.assertEqual(FakeFrozenList([]).append(1), FakeFrozenList([1]))

    def test_add(self):
        self.assertEqual(FakeFrozenList([]) + [1], FakeFrozenList([1]))
        self.assertEqual(FakeFrozenList([]) + FakeFrozenList([1]), FakeFrozenList([1]))

    def test_iter(self):
        self.assertEqual(list(FakeFrozenList([1])), [FakeType(1)])

    def test_len(self):
        self.assertEqual(len(FakeFrozenList([1])), 1)

    def test_bool(self):
        self.assertTrue(FakeFrozenList([1]))
        self.assertFalse(FakeFrozenList([]))

    def test_tail_head(self):
        self.assertEqual(FakeFrozenList([1]).head_tail(), (FakeType(1), FakeFrozenList([])))
        with self.assertRaises(Exception):
            FakeFrozenList([]).head_tail()

    def test_repr(self):
        self.assertEqual(repr(FakeFrozenList([1])), "FakeFrozenList([1])")