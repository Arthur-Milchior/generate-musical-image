import unittest
from typing import Generic, Set

from solfege.interval import DiatonicInterval
from solfege.interval.abstract import IntervalType


class SetOfIntervals(Generic[IntervalType]):
    """A set of intervals, modulo octave"""

    def __init__(self, set_=Set[IntervalType]):
        self.set_ = set()
        self.set_base_octave = set()
        if set_:
            for interval in set_:
                self.set_.add(interval)
                self.set_base_octave.add(interval.get_in_base_octave())

    def __contains__(self, interval):
        """Whether this note belongs to the set (up to octave)"""
        return interval.get_in_base_octave() in self.set_base_octave

    def __iter__(self):
        """Intervals belonging to this set."""
        return iter(self.set_base_octave)


class TestSetOfIntervals(unittest.TestCase):
    soi = SetOfIntervals[DiatonicInterval]({
        DiatonicInterval(value=0),
        DiatonicInterval(value=3),
        DiatonicInterval(value=7),
    })

    def test_contains(self):
        self.assertIn(0, self.soi)
        self.assertIn(3, self.soi)
        self.assertIn(10, self.soi)
        self.assertNotIn(2, self.soi)

    def test_iter(self):
        l = list(self.soi)  # use of list to keep duplicate
        self.assertEquals(len(l), 2)
        self.assertEquals(set(l), {DiatonicInterval(0, DiatonicInterval(3))})
