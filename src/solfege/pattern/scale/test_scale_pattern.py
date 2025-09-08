import unittest
from solfege.pattern.scale.scale_pattern import *
from solfege.pattern.scale.scale_patterns import *


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
        self.assertNotEqual(minor_melodic,
                             ScalePattern.make_relative([2, 1, 2, 2, 2, 2, 1], names=["Minor melodic"], interval_for_signature=four_flats, record=False))
        self.assertNotEqual(minor_melodic, ScalePattern.make_relative( [2, 1, 2, 2, 2, 2],names=["Minor melodic"],
                                                                  interval_for_signature= three_flats, suppress_warning=False, record=False))
        self.assertNotEqual(minor_melodic, ScalePattern.make_relative([2, 1, 2, 2, 2, 2, 1],names=["Minor"], 
                                                                   interval_for_signature=three_flats, record=False))

    def test_eq(self):
        self.assertEqual(minor_melodic.interval_for_signature, three_flats)
        self.assertEqual(list(minor_melodic.relative_intervals()), [
            Interval.make(chromatic=2, diatonic=1),
            Interval.make(chromatic=1, diatonic=1),
            Interval.make(chromatic=2, diatonic=1),
            Interval.make(chromatic=2, diatonic=1),
            Interval.make(chromatic=2, diatonic=1),
            Interval.make(chromatic=2, diatonic=1),
            Interval.make(chromatic=1, diatonic=1),
        ])

    def test_get_notes(self):
        tonic = Note.make(0, 0)
        self.assertEqual(minor_melodic.from_note(tonic).notes,
                          ([
                              Note.make(0, 0),
                              Note.make(2, 1),
                              Note.make(3, 2),
                              Note.make(5, 3),
                              Note.make(7, 4),
                              Note.make(9, 5),
                              Note.make(11, 6),
                              Note.make(12, 7),
                          ]))

    def test_neg(self):
        reversed = -minor_melodic
        expected = ScalePattern.make_relative(names=["Minor melodic"],
                                          relative_intervals=[
                                              Interval.make(diatonic=-1, chromatic=- 1),
                                              Interval.make(diatonic=-1, chromatic=-2),
                                              Interval.make(diatonic=-1, chromatic=-2),
                                              Interval.make(diatonic=-1, chromatic=-2),
                                              Interval.make(diatonic=-1, chromatic=-2),
                                              Interval.make(diatonic=-1, chromatic=-1),
                                              Interval.make(diatonic=-1, chromatic=-2)], interval_for_signature=three_flats, increasing=False,
                                          record=False, descending=minor_natural)
        self.assertEqual(reversed,
                          expected)

    def test_generate(self):
        expected = Scale(notes=[
            Note.make(0, 0),
            Note.make(2, 1),
            Note.make(3, 2),
            Note.make(5, 3),
            Note.make(7, 4),
            Note.make(9, 5),
            Note.make(11, 6),
            Note.make(12, 7),
        ], pattern=minor_melodic)
        generated = minor_melodic.from_note(Note.make(0, 0))
        self.assertScaleEqual(expected, generated)

    def test_generate_two(self):
        expected = Scale(notes=[
            Note.make(0, 0),
            Note.make(2, 1),
            Note.make(3, 2),
            Note.make(5, 3),
            Note.make(7, 4),
            Note.make(9, 5),
            Note.make(11, 6),
            Note.make(12, 7),
            Note.make(14, 8),
            Note.make(15, 9),
            Note.make(17, 10),
            Note.make(19, 11),
            Note.make(21, 12),
            Note.make(23, 13),
            Note.make(24, 14),
        ], pattern=minor_melodic)
        generated = minor_melodic.from_note(Note.make(0, 0), number_of_octaves=2)
        self.assertScaleEqual(expected, generated)

    def test_generate_two_extra(self):
        expected = Scale(notes=[
            Note.make(0, 0),
            Note.make(2, 1),
            Note.make(3, 2),
            Note.make(5, 3),
            Note.make(7, 4),
            Note.make(9, 5),
            Note.make(11, 6),
            Note.make(12, 7),
            Note.make(14, 8),
            Note.make(15, 9),
            Note.make(17, 10),
            Note.make(19, 11),
            Note.make(21, 12),
            Note.make(23, 13),
            Note.make(24, 14),
            Note.make(26, 15),
        ], pattern=minor_melodic)
        generated = minor_melodic.from_note(Note.make(0, 0), number_of_octaves=2, add_an_extra_note=True)
        self.assertEqual(expected, generated)

    def test_generate_minus_two(self):
        expected = Scale(notes=[
            Note.make(0, 0),
            Note.make(-1, -1),
            Note.make(-3, -2),
            Note.make(-5, -3),
            Note.make(-7, -4),
            Note.make(-9, -5),
            Note.make(-10, -6),
            Note.make(-12, -7),
            Note.make(-13, -8),
            Note.make(-15, -9),
            Note.make(-17, -10),
            Note.make(-19, -11),
            Note.make(-21, -12),
            Note.make(-22, -13),
            Note.make(-24, -14),
        ], pattern=minor_melodic)
        generated = minor_melodic.from_note(Note.make(0, 0), number_of_octaves=-2)
        self.assertScaleEqual(expected, generated)

    def test_generate_minus_two_extra(self):
        expected = Scale(notes=[
            Note.make(0, 0),
            Note.make(-1, -1),
            Note.make(-3, -2),
            Note.make(-5, -3),
            Note.make(-7, -4),
            Note.make(-9, -5),
            Note.make(-10, -6),
            Note.make(-12, -7),
            Note.make(-13, -8),
            Note.make(-15, -9),
            Note.make(-17, -10),
            Note.make(-19, -11),
            Note.make(-21, -12),
            Note.make(-22, -13),
            Note.make(-24, -14),
            Note.make(-25, -15),
        ], pattern=minor_melodic)
        generated = minor_melodic.from_note(Note.make(0, 0), number_of_octaves=-2, add_an_extra_note=True)
        self.assertEqual(expected, generated)

    def test_multiple_octave(self):
        self.assertEqual(
            IntervalList.make_relative([]), 
            major_scale.multiple_octaves(0))
        
        self.assertEqual(
            IntervalList.make_relative([2, 2, 1, 2, 2, 2, 1,]), 
            major_scale.multiple_octaves(1))
        
        self.assertEqual(
            IntervalList.make_relative([2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, ]), 
            major_scale.multiple_octaves(2))