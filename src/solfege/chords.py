from .util import Solfege_Pattern
from .interval import SolfegeInterval
from util import debug


class Chord_Pattern(Solfege_Pattern):
    """A pattern describing a chord.

    intervals -- set of chromatic interval, between the tonic and a note of the chord.
    Optional -- Whether the 5th is optional
    fromInterval -- associate to a set of interval the class of the chord it represents.
    """
    fromInterval = dict()

    def __init__(self, names, intervals, optional=None):
        """A sequence of interval between the tonic and the other notes of this chord.

        """
        super().__init__(names)
        self.fifthOptional = optional
        intervals.add((0, 0))
        self.intervalsWithoutFifth = frozenset(
            {SolfegeInterval(chromatic=chromatic, diatonic=diatonic) for chromatic, diatonic in intervals if
             diatonic != 5})
        self.intervals = frozenset(
            {SolfegeInterval(chromatic=chromatic, diatonic=diatonic) for chromatic, diatonic in intervals})
        self.add(self.intervals)
        if optional:
            self.add(self.intervalsWithoutFifth)
        self.optional = optional

    def getFromInterval(intervals):
        """Given a set of interval, return the object having this set of intervals

        Class method."""
        return Chord_Pattern.fromInterval.get(frozenset(intervals))

    def add(self, intervals):
        """ensure that, given the set of intervals, current object can be retrieved"""
        self.fromInterval[intervals] = self

    def getNotes(self, base):
        return frozenset({base + interval for interval in self.intervals})


Solfege_Pattern.dic[Chord_Pattern] = dict()
Solfege_Pattern.set_[Chord_Pattern] = list()

Chord_Pattern(["Major triad"], {(4, 2), (7, 4)})
Chord_Pattern(["Minor triad"], {(3, 2), (7, 4)})
Chord_Pattern(["Augmented triad"], {(4, 2), (8, 4)})
Chord_Pattern(["Diminished triad"], {(3, 2), (6, 4)})
Chord_Pattern(["Minor major seventh chord"], {(3, 2), (7, 4), (11, 6)}, True)
Chord_Pattern(["Augmented major seventh chord"], {(4, 2), (8, 4), (11, 6)})
Chord_Pattern(["Diminished major seventh chord"], {(3, 2), (6, 4), (11, 6)})
Chord_Pattern(["Diminished seventh chord"], {(3, 2), (6, 4), (9, 6)})
Chord_Pattern(["Half-diminished seventh chord", "Half-diminished chord", "Minor seventh flat five"],
              {(3, 2), (6, 4), (10, 6)})
Chord_Pattern(["Augmented seventh chord", "seventh augmented fifth chord", "seventh sharp five chord"],
              {(4, 2), (8, 4), (10, 6)})
Chord_Pattern(["Dominant seventh flat five chord"], {(4, 2), (6, 4), (10, 6)})
Chord_Pattern(["Dominant seventh chord", "major minor seventh chord"], {(4, 2), (7, 4), (10, 6)}, True)
Chord_Pattern(["Major seventh chord"], {(4, 2), (7, 4), (11, 6)}, True)
Chord_Pattern(["Minor seventh chord"], {(3, 2), (7, 4), (10, 6)}, True)
