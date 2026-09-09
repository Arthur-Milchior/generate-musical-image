from utils.frozenlist import *
import unittest

@dataclass
class FakeType(MakeableWithSingleArgument):
    """Minimal `MakeableWithSingleArgument` implementation used only to exercise `FrozenList` in these tests."""

    value: int
    """The single wrapped int value."""

    #pragma mark - MakeableWithSingleArgument

    @classmethod
    def _make_single_argument(cls, arg) -> Self:
        """Build a `FakeType` from a bare `int`."""
        assert_typing(arg, int)
        return FakeType(arg)

    def repr_single_argument(self) -> str:
        """Just the wrapped value, as a string."""
        return f"{self.value}"

class FakeFrozenList(FrozenList[FakeType]):
    """A `FrozenList` of `FakeType`, used as the test fixture below."""
    type = FakeType
    """Restricts elements to `FakeType`."""


class TestFakeFrozenList(unittest.TestCase):
    """Tests for `FrozenList`, exercised via the `FakeFrozenList`/`FakeType` fixtures above."""

    def test_eq(self):
        """Two empty lists are equal; an empty and a non-empty list are not."""
        self.assertEqual(FakeFrozenList([]), FakeFrozenList([]))
        self.assertNotEqual(FakeFrozenList([]), FakeFrozenList([1]))

    def test_append(self):
        """`append` returns a new list with the value added, coercing a bare int via `MakeableWithSingleArgument`."""
        self.assertEqual(FakeFrozenList([]).append(1), FakeFrozenList([1]))

    def test_add(self):
        """`+` concatenates either a plain iterable or another `FrozenList` of the same element type."""
        self.assertEqual(FakeFrozenList([]) + [1], FakeFrozenList([1]))
        self.assertEqual(FakeFrozenList([]) + FakeFrozenList([1]), FakeFrozenList([1]))

    def test_iter(self):
        """Iterating yields coerced `FakeType` elements, not the raw ints passed in."""
        self.assertEqual(list(FakeFrozenList([1])), [FakeType(1)])

    def test_len(self):
        """`len()` reflects the number of elements."""
        self.assertEqual(len(FakeFrozenList([1])), 1)

    def test_bool(self):
        """A non-empty list is truthy; an empty one is falsy."""
        self.assertTrue(FakeFrozenList([1]))
        self.assertFalse(FakeFrozenList([]))

    def test_tail_head(self):
        """`head_tail` splits off the first element; calling it on an empty list raises."""
        self.assertEqual(FakeFrozenList([1]).head_tail(), (FakeType(1), FakeFrozenList([])))
        with self.assertRaises(Exception):
            FakeFrozenList([]).head_tail()

    def test_repr(self):
        """`repr()` uses `repr_single_argument()` for each element, not the class-qualified default repr."""
        self.assertEqual(repr(FakeFrozenList([1])), "FakeFrozenList([1])")