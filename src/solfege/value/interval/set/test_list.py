import unittest

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from solfege.value.interval.test_chromatic_interval import TestChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note


major_triad_absolut_list = [Interval.make(0, 0), Interval.make(4, 2), Interval.make(7, 4)] # pyright: ignore[reportUndefinedVariable]
major_triad_relative_list = [Interval.make(4, 2), Interval.make(3, 2)]
minor_triad_relative = IntervalList.make_relative([(3, 2), (4, 2)])
major_triad_relative = IntervalList.make_relative(major_triad_relative_list)
major_triad_absolute = IntervalList.make_absolute(major_triad_absolut_list)
major_triad_zero = IntervalList.make_absolute([Interval.make(4, 2), Interval.make(7, 4)])

class TestIntervalList(unittest.TestCase):
    """Tests for `IntervalList`, built via both `make_relative` and `make_absolute`."""
    def test_eq(self) -> None:
        """`make_relative` and `make_absolute` build equal lists for the same shape, and different
        shapes compare unequal."""
        self.assertEqual(major_triad_relative, major_triad_absolute)
        self.assertEqual(major_triad_relative, major_triad_absolute)
        self.assertNotEqual(major_triad_relative, minor_triad_relative)

    def test_absolute(self) -> None:
        """`absolute_intervals()` returns the intervals relative to the shared starting note."""
        self.assertEqual(list(major_triad_absolute.absolute_intervals()), major_triad_absolut_list)

    def test_relative(self) -> None:
        """`relative_intervals()` returns the pairwise differences between consecutive intervals."""
        self.assertEqual(list(major_triad_absolute.relative_intervals()), major_triad_relative_list)

    # def test_chromatic_absolute(self):
    #     self.assertEqual(list(major_triad_absolute.absolute_chromatic()), [ChromaticInterval.make(0), ChromaticInterval.make(4), ChromaticInterval.make(7)])
    
    # def test_chromatic_relative(self):
    #     self.assertEqual(list(major_triad_absolute.relative_chromatic()), [ChromaticInterval.make(4), ChromaticInterval.make(3)])

    # def test_diatonic_absolute(self):
    #     self.assertEqual(list(major_triad_absolute.absolute_diatonic()), [DiatonicInterval.make(0), DiatonicInterval.make(2), DiatonicInterval.make(4)])
    
    # def test_diatonic_relative(self):
    #     self.assertEqual(list(major_triad_absolute.relative_diatonic()), [DiatonicInterval.make(2), DiatonicInterval.make(2)])

    def test_from_chromatic_note(self) -> None:
        """`from_note` on a chromatic-only interval list instantiates it starting at a given chromatic note."""
        self.assertEqual(list(major_triad_absolute.get_chromatic_interval_list().from_note(ChromaticNote(0))), [ChromaticNote(0), ChromaticNote(4), ChromaticNote(7)])

    def test_from_note(self) -> None:
        """`from_note` instantiates the pattern starting at a given `Note`."""
        self.assertEqual(list(major_triad_absolute.from_note(Note.make(0, 0))), [Note.make(0, 0), Note.make(4, 2), Note.make(7, 4)])

    def test_chromatic(self) -> None:
        """`get_chromatic_interval_list` drops diatonic spelling, matching the equivalent
        chromatic-only relative pattern."""
        self.assertEqual(major_triad_absolute.get_chromatic_interval_list(), ChromaticIntervalListPattern.make_relative([4, 3]))

    def test_repr(self) -> None:
        """`repr` is evaluable, reusing `make_absolute` and the raw interval tuples/values."""
        self.assertEqual(repr(major_triad_absolute), "IntervalListPattern.make_absolute([(0, 0), (4, 2), (7, 4)])")
        self.assertEqual(repr(major_triad_absolute.get_chromatic_interval_list()), "ChromaticIntervalListPattern.make_absolute([0, 4, 7])")