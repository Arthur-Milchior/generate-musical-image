# import unittest

# from solfege.pattern.chord.chord_pattern import *

# from solfege.value.interval.set.set_of_intervals import *

# major_chord = SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(4), ChromaticInterval.make(7)])
# augmented = SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(4), ChromaticInterval.make(8)])
# dominant =  SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(4), ChromaticInterval.make(7), ChromaticInterval.make(10)])
# minor_major_7th =  SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(3), ChromaticInterval.make(7), ChromaticInterval.make(11)])
# diminshed_7th =  SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(3), ChromaticInterval.make(6), ChromaticInterval.make(9)])

# major_first_inversion = SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(3), ChromaticInterval.make(8)])
# major_second_inversion = SetOfIntervals.make([ChromaticInterval.make(0), ChromaticInterval.make(9), ChromaticInterval.make(5)])

# class TestSetOfIntervals(unittest.TestCase):

#     def test_eq(self):
#         self.assertEqual(major_chord, major_chord)
#         self.assertNotEqual(major_chord, dominant)

#     def test_add(self):
#         self.assertEqual(major_chord, major_chord+ChromaticInterval.make(0))
#         self.assertEqual(major_chord+ChromaticInterval.make(1), SetOfIntervals.make([ChromaticInterval.make(1), ChromaticInterval.make(5), ChromaticInterval.make(8)]))
#         self.assertEqual(major_chord+ChromaticInterval.make(5), SetOfIntervals.make([ChromaticInterval.make(5), ChromaticInterval.make(9), ChromaticInterval.make(0)]))

#     def test_contains(self):
#         self.assertIn(ChromaticInterval.make(0), major_chord)
#         self.assertIn(ChromaticInterval.make(4), major_chord)
#         self.assertNotIn(ChromaticInterval.make(10), major_chord)

#     def test_inversion(self):
#         self.assertEqual(major_inversion(ChromaticInterval.make(4)), )

#     def test_inversion(self):
#         self.assertEqual(set(major_inversions()), 
#                          {InversionPattern(0, major_chord), InversionPattern(1, major_first_inversion), InversionPattern(2, major_second_inversion)})
        
#     def test_minor(self):
#         self.assertFalse(major_chord.is_minor())
#         self.assertTrue(minor_major_7th.is_minor())

#     def test_major(self):
#         self.assertTrue(major_chord.is_major())
#         self.assertFalse(minor_major_7th.is_major())

#     def test_third(self):
#         self.assertEqual(major_chord.third(), Third.MAJOR)
#         self.assertEqual(minor_major_7th.third(), Third.MINOR)
#         self.assertEqual(major_second_inversion.third(), Third.NONE)

#     def test_fifth(self):
#         self.assertEqual(augmented.fifth(), Fifth.AUGMENTED)
#         self.assertEqual(diminshed_7th.fifth(), Fifth.DIMINISHED)
#         self.assertEqual(major_chord.fifth(), Fifth.JUST)
#         self.assertEqual(major_second_inversion.fifth(), Fifth.NONE)

#     def test_has_quality(self):
#         self.assertFalse(major_chord.has_quality())
#         self.assertTrue(diminshed_7th.has_quality())
        
#     def test_has_quality(self):
#         self.assertFalse(major_chord.has_quality())
#         self.assertTrue(diminshed_7th.has_quality())

#     def test_pattern(self):
#         self.assertEqual(major_chord, major_triad)