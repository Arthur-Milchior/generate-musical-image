from .util import Solfege_Pattern
from .interval import ChromaticInterval
from util import debug

class Chord_Pattern(Solfege_Pattern):
    fromInterval=dict()
    def __init__(self,names,intervals,optional=None):
        super().__init__(names)
        intervals={ChromaticInterval(chromatic=interval) for interval in intervals}
        intervals.add(ChromaticInterval(chromatic=0))
        intervals=frozenset(intervals)
        self.intervals=intervals
        self.add(intervals)
        if optional is not None:
            optional=ChromaticInterval(chromatic=optional)
            self.add(self.intervals|frozenset({optional}))
        self.optional =optional

    def getFromInterval(intervals):
        return Chord_Pattern.fromInterval.get(frozenset(intervals))

    def add(self,intervals):
        #debug("Adding %s for %s",(intervals,self.names[0]))
        self.fromInterval[intervals]=self
Solfege_Pattern.dic[Chord_Pattern]=dict()
Solfege_Pattern.set_[Chord_Pattern]=list()

Chord_Pattern(["Major triad"],{4,7})
Chord_Pattern(["Minor triad"],{3,7})
Chord_Pattern(["Augmented triad"],{4,8})
Chord_Pattern(["Diminished triad"],{3,6})
Chord_Pattern(["Minor major seventh chord"],{3,11},7)
Chord_Pattern(["Augmented major seventh chord"],{4,8,11})
Chord_Pattern(["Diminished major seventh chord"],{3,6,11})
Chord_Pattern(["Diminished seventh chord"],{3,6,9})
Chord_Pattern(["Half-diminished seventh chord","Half-diminished chord","Minor seventh flat five"],{3,6,10})
Chord_Pattern(["Augmented seventh chord","seventh augmented fifth chord","seventh sharp five chord"],{4,8,10})
Chord_Pattern(["Dominant seventh flat five chord"],{4,6,10})
Chord_Pattern(["Dominant seventh chord","major minor seventh chord"],{4,10},7)
Chord_Pattern(["Major seventh chord"],{4,11},7)
Chord_Pattern(["Minor seventh chord"],{3,10},7)

