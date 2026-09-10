"""Tests for `SetOfAccordinaNote`'s pictured-range computation (`number_of_rows`, `_min_pictured_note`,
`_max_pictured_note`, `pictured_notes`)."""
import unittest

from instruments.accordina.set_of_accordina_notes import SetOfAccordinaNote
from instruments.accordina.test_note import *
from instruments.accordina.accordina_note import *

class FakeSetOfAccordinaNote(SetOfAccordinaNote):
    """Minimal concrete `SetOfAccordinaNote` used only to exercise the abstract class in tests."""
    def _svg_name_base(self) -> str:
        """Fixed dummy name; the SVG file name itself isn't under test here."""
        return "fake"

class TestSetOfAccordinaNote(unittest.TestCase):
    """Checks that a set built from two notes (C4 and D#4) computes the expected pictured range and
    selected/unselected buttons."""
    set_c_dsharp = FakeSetOfAccordinaNote({C4, D4_sharp})
    """Shared fixture: the set of `{C4, D4_sharp}`, reused by `test`."""

    def test(self) -> None:
        """The pictured range spans 5 rows from C4 to F4, with C4/D#4 selected and the rest not."""
        self.assertEqual(self.set_c_dsharp.number_of_rows(), 5)
        self.assertEqual(self.set_c_dsharp._min_pictured_note(), C4)
        self.assertEqual(self.set_c_dsharp._max_pictured_note(), F4)
        self.assertEqual(set(self.set_c_dsharp.pictured_notes()), {AccordinaNote(0, selected=True), C4_sharp, D4, AccordinaNote(3, selected=True), E4, F4})