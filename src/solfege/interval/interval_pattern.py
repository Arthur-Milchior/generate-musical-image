from typing import Iterator, List, Union
from solfege.interval.chromatic import ChromaticInterval
from solfege.note.abstract import NoteType
from solfege.note.chromatic import ChromaticNote
from solfege.solfege_pattern import SolfegePattern
from solfege.interval.interval import Interval


class IntervalPattern(SolfegePattern):
    _interval : List[Interval]

    interval : ChromaticInterval

    def __init__(self, name: str, interval: Union[int, ChromaticInterval], *args, **kwargs):
        super().__init__([name], *args, **kwargs)
        if isinstance(interval, int):
            interval = ChromaticInterval (interval)
        self.interval = interval

    def get_notes(self, tonic: NoteType)-> Iterator[ChromaticNote]:
        return [tonic, tonic+self.interval]

intervals_up_to_octave = [
    IntervalPattern("Second minor", Interval(diatonic=1, chromatic=1)),
    IntervalPattern("Second major", Interval(diatonic=1, chromatic=2)),
    IntervalPattern("Third minor", Interval(diatonic=2, chromatic=3)),
    IntervalPattern("Third major", Interval(diatonic=2, chromatic=4)),
    IntervalPattern("Fourth just", Interval(diatonic=3, chromatic=5)),
    IntervalPattern("Fourth augmented", Interval(diatonic=3, chromatic=6)),
    IntervalPattern("Fifth just", Interval(diatonic=5, chromatic=7)),
    IntervalPattern("Sixth minor", Interval(diatonic=5, chromatic=8)),
    IntervalPattern("Sixth major", Interval(diatonic=5, chromatic=9)),
    IntervalPattern("Seventh minor", Interval(diatonic=6, chromatic=10)),
    IntervalPattern("Seventh major", Interval(diatonic=6, chromatic=11)),
    IntervalPattern("Octave", Interval(diatonic=7, chromatic=12)),


    IntervalPattern("Unison augmented", Interval(diatonic=0, chromatic=1)),
    IntervalPattern("Second diminished", Interval(diatonic=1, chromatic=0)),
    IntervalPattern("Second augmented", Interval(diatonic=1, chromatic=3)),
    IntervalPattern("Third dimished", Interval(diatonic=2, chromatic=3)),
    IntervalPattern("Third augmented", Interval(diatonic=2, chromatic=5)),
    IntervalPattern("Fourth diminished", Interval(diatonic=3, chromatic=4)),
    IntervalPattern("Fifth diminished", Interval(diatonic=5, chromatic=6)),
    IntervalPattern("Fifth augmented", Interval(diatonic=5, chromatic=8)),
    IntervalPattern("Sixth diminished", Interval(diatonic=5, chromatic=7)),
    IntervalPattern("Sixth augmented", Interval(diatonic=5, chromatic=10)),
    IntervalPattern("Seventh diminished", Interval(diatonic=6, chromatic=9)),
    IntervalPattern("Seventh augmented", Interval(diatonic=6, chromatic=12)),
    IntervalPattern("Octave diminished", Interval(diatonic=7, chromatic=11)),
    IntervalPattern("Octave augmented", Interval(diatonic=7, chromatic=13)),
]