import unittest
from solfege.pattern.scale.scale_pattern import *
from solfege.pattern_instantiation.scale.scale import Scale
from solfege.value.interval.role.interval_role_from_string import IntervalRoleFromString
from solfege.value.note.set.note_list import NoteList
from utils.util import assert_typing

from solfege.value.key.keys import *

class TestScalePattern(unittest.TestCase):

    def assertScalePatternEqual(self, scale1: ScalePattern, scale2:ScalePattern):
        assert_typing(scale1, ScalePattern)
        assert_typing(scale2, ScalePattern)
        self.assertEqual(scale1._absolute_intervals, scale2._absolute_intervals)
        self.assertEqual(scale1.descending, scale2.descending)
        self.assertEqual(scale1.names, scale2.names)
        self.assertEqual(scale1.notation, scale2.notation)
        self.assertEqual(scale1.interval_for_signature, scale2.interval_for_signature)

    def assertScaleEqual(self, scale1: Scale, scale2:Scale):
        assert_typing(scale1, Scale)
        assert_typing(scale2, Scale)
        self.assertEqual(scale1.notes, scale2.notes)

    def test_ne(self):
        from solfege.pattern.scale.scale_patterns import minor_melodic
        self.assertNotEqual(minor_melodic,
                             ScalePattern.make_relative([2, 1, 2, 2, 2, 2, 1], names=["Minor melodic"], interval_for_signature=four_flats, record=False))
        self.assertNotEqual(minor_melodic, ScalePattern.make_relative( [2, 1, 2, 2, 2, 2],names=["Minor melodic"],
                                                                  interval_for_signature= three_flats, suppress_warning=False, record=False))
        self.assertNotEqual(minor_melodic, ScalePattern.make_relative([2, 1, 2, 2, 2, 2, 1],names=["Minor"], 
                                                                   interval_for_signature=three_flats, record=False))

    def test_eq(self):
        from solfege.pattern.scale.scale_patterns import minor_melodic
        self.assertEqual(minor_melodic.interval_for_signature, three_flats)
        self.assertEqual(list(minor_melodic.relative_intervals()), [
            Interval.make(_chromatic=2, _diatonic=1),
            Interval.make(_chromatic=1, _diatonic=1),
            Interval.make(_chromatic=2, _diatonic=1),
            Interval.make(_chromatic=2, _diatonic=1),
            Interval.make(_chromatic=2, _diatonic=1),
            Interval.make(_chromatic=2, _diatonic=1),
            Interval.make(_chromatic=1, _diatonic=1),
        ])


    def test_neg(self):
        from solfege.pattern.scale.scale_patterns import minor_melodic, minor_natural
        reversed = -minor_melodic
        expected = ScalePattern.make_relative(names=["Minor melodic"],
                                          relative_intervals=[
                                              Interval.make(_diatonic=-1, _chromatic=- 1),
                                              Interval.make(_diatonic=-1, _chromatic=-2),
                                              Interval.make(_diatonic=-1, _chromatic=-2),
                                              Interval.make(_diatonic=-1, _chromatic=-2),
                                              Interval.make(_diatonic=-1, _chromatic=-2),
                                              Interval.make(_diatonic=-1, _chromatic=-1),
                                              Interval.make(_diatonic=-1, _chromatic=-2)], interval_for_signature=three_flats, increasing=False,
                                          record=False, _descending=minor_natural)
        self.assertEqual(reversed,
                          expected)


    def test_multiple_octave(self):
        from solfege.pattern.scale.scale_patterns import major_scale
        self.assertEqual(
            IntervalListPattern.make_relative([]), 
            major_scale.multiple_octaves(0))
        
        self.assertEqual(
            IntervalListPattern.make_relative([2, 2, 1, 2, 2, 2, 1,]), 
            major_scale.multiple_octaves(1))
        
        self.assertEqual(
            IntervalListPattern.make_relative([2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, ]), 
            major_scale.multiple_octaves(2))
        
    def test_keep_role(self):
        blues = ScalePattern.make_relative(names=["Blues"], relative_intervals=[(3, 2), 2, (1, 0, "b"), 1, (3, 2), 2], interval_for_signature=three_flats, record=False)
        absolute_intervals = blues.absolute_intervals()
        blue_note = absolute_intervals[3]
        self.assertEqual(blue_note.get_chromatic().value, 6)
        self.assertEqual(blue_note.get_diatonic().value, 3)
        self.assertEqual(blue_note._role, IntervalRoleFromString("b"))