import unittest

from .interval.interval import Interval
from .solfege_pattern import SolfegePattern


class ChordPattern(SolfegePattern):
    """A pattern describing a chord.

    names -- the list of names of this chord. Or a single name.
    intervals -- set of chromatic interval, between the tonic and a note of the chord.
    optional -- Whether the 5th is optional
    fromInterval -- associate to a set of interval the class of the chord it represents.
    """
    fromInterval = dict()

    def __init__(self, names, intervals, optional=None):
        """A sequence of interval between the tonic and the other notes of this chord.

        """
        super().__init__(names)
        self.fifthOptional = optional
        intervals.add((0, 0))
        self.intervals = frozenset(Interval.factory(interval) for interval in intervals)
        self.intervalsWithoutFifth = frozenset(
            interval for interval in self.intervals if interval.get_diatonic().get_number() != 4)
        self._add(self.intervals)
        if optional:
            self._add(self.intervalsWithoutFifth)
        self.optional = optional

    @staticmethod
    def getFromInterval(intervals):
        """Given a set of interval, return the object having this set of intervals."""
        return ChordPattern.fromInterval.get(frozenset(intervals))

    def _add(self, intervals):
        """ensure that, given the set of intervals, current object can be retrieved"""
        self.fromInterval[intervals] = self

    def getNotes(self, base):
        return frozenset({base + interval for interval in self.intervals})


ChordPattern(["Major triad"], {(4, 2), (7, 4)})
minor = ChordPattern(["Minor triad"], {(3, 2), (7, 4)})
ChordPattern(["Augmented triad"], {(4, 2), (8, 4)})
ChordPattern(["Diminished triad"], {(3, 2), (6, 4)})
ChordPattern(["Minor major seventh chord"], {(3, 2), (7, 4), (11, 6)}, True)
ChordPattern(["Augmented major seventh chord"], {(4, 2), (8, 4), (11, 6)})
ChordPattern(["Diminished major seventh chord"], {(3, 2), (6, 4), (11, 6)})
ChordPattern(["Diminished seventh chord"], {(3, 2), (6, 4), (9, 6)})
ChordPattern(["Half-diminished seventh chord", "Half-diminished chord", "Minor seventh flat five"],
             {(3, 2), (6, 4), (10, 6)})
ChordPattern(["Augmented seventh chord", "seventh augmented fifth chord", "seventh sharp five chord"],
             {(4, 2), (8, 4), (10, 6)})
ChordPattern(["Dominant seventh flat five chord"], {(4, 2), (6, 4), (10, 6)})
ChordPattern(["Dominant seventh chord", "major minor seventh chord"], {(4, 2), (7, 4), (10, 6)}, True)
ChordPattern(["Major seventh chord"], {(4, 2), (7, 4), (11, 6)}, True)
minor_seven = ChordPattern(["Minor seventh chord"], {(3, 2), (7, 4), (10, 6)}, True)


class TestChordPattern(unittest.TestCase):
    def test_from_interval(self):
        self.assertEquals(ChordPattern.getFromInterval(frozenset({
            Interval(chromatic=0, diatonic=0),
            Interval(chromatic=3, diatonic=2),
            Interval(chromatic=7, diatonic=4),
            Interval(chromatic=10, diatonic=6)
        }
        )), minor_seven)

    def test_from_interval_no_fifth(self):
        self.assertEquals(ChordPattern.getFromInterval(frozenset({
            Interval(chromatic=0, diatonic=0),
            Interval(chromatic=3, diatonic=2),
            Interval(chromatic=10, diatonic=6)
        }
        )), minor_seven)
