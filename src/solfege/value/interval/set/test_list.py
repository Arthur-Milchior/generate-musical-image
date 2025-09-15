import unittest

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from solfege.value.interval.test_chromatic_interval import TestChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note


major_triad_absolut_list = [Interval.make(0, 0), Interval.make(4, 2), Interval.make(7, 4)] # pyright: ignore[reportUndefinedVariable]
major_triad_relative_list = [Interval.make(4, 2), Interval.make(3, 2)]
minor_triad_relative = IntervalListPattern.make_relative([(3, 2), (4, 2)])
major_triad_relative = IntervalListPattern.make_relative(major_triad_relative_list)
major_triad_absolute = IntervalListPattern.make_absolute(major_triad_absolut_list)
major_triad_zero = IntervalListPattern.make_absolute([Interval.make(4, 2), Interval.make(7, 4)])

class TestIntervalList(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(major_triad_relative, major_triad_absolute)
        self.assertEqual(major_triad_relative, major_triad_absolute)
        self.assertNotEqual(major_triad_relative, minor_triad_relative)

    def test_absolute(self):
        self.assertEqual(list(major_triad_absolute.absolute_intervals()), major_triad_absolut_list)
    
    def test_relative(self):
        self.assertEqual(list(major_triad_absolute.relative_intervals()), major_triad_relative_list)

    # def test_chromatic_absolute(self):
    #     self.assertEqual(list(major_triad_absolute.absolute_chromatic()), [ChromaticInterval(0), ChromaticInterval(4), ChromaticInterval(7)])
    
    # def test_chromatic_relative(self):
    #     self.assertEqual(list(major_triad_absolute.relative_chromatic()), [ChromaticInterval(4), ChromaticInterval(3)])

    # def test_diatonic_absolute(self):
    #     self.assertEqual(list(major_triad_absolute.absolute_diatonic()), [DiatonicInterval(0), DiatonicInterval(2), DiatonicInterval(4)])
    
    # def test_diatonic_relative(self):
    #     self.assertEqual(list(major_triad_absolute.relative_diatonic()), [DiatonicInterval(2), DiatonicInterval(2)])

    def test_from_chromatic_note(self):
        self.assertEqual(list(major_triad_absolute.get_chromatic_interval_list().from_note(ChromaticNote(0))), [ChromaticNote(0), ChromaticNote(4), ChromaticNote(7)])

    def test_from_note(self):
        self.assertEqual(list(major_triad_absolute.from_note(Note.make(0, 0))), [Note.make(0, 0), Note.make(4, 2), Note.make(7, 4)])
        
    def test_chromatic(self):
        self.assertEqual(major_triad_absolute.get_chromatic_interval_list(), ChromaticIntervalListPattern.make_relative([4, 3]))

    def test_repr(self):
        self.assertEqual(repr(major_triad_absolute), "IntervalListPattern.make_absolute([(0, 0), (4, 2), (7, 4)])")
        self.assertEqual(repr(major_triad_absolute.get_chromatic_interval_list()), "ChromaticIntervalListPattern.make_absolute([0, 4, 7])")