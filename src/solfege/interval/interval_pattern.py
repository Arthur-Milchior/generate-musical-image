from typing import Iterator, List, Union
from solfege.interval.chromatic_interval import ChromaticInterval
from solfege.note.abstract_note import NoteType
from solfege.note.chromatic_note import ChromaticNote
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
    IntervalPattern("Second minor", Interval.make(diatonic=1, chromatic=1)),
    IntervalPattern("Second major", Interval.make(diatonic=1, chromatic=2)),
    IntervalPattern("Third minor", Interval.make(diatonic=2, chromatic=3)),
    IntervalPattern("Third major", Interval.make(diatonic=2, chromatic=4)),
    IntervalPattern("Fourth just", Interval.make(diatonic=3, chromatic=5)),
    IntervalPattern("Fourth augmented", Interval.make(diatonic=3, chromatic=6)),
    IntervalPattern("Fifth just", Interval.make(diatonic=5, chromatic=7)),
    IntervalPattern("Sixth minor", Interval.make(diatonic=5, chromatic=8)),
    IntervalPattern("Sixth major", Interval.make(diatonic=5, chromatic=9)),
    IntervalPattern("Seventh minor", Interval.make(diatonic=6, chromatic=10)),
    IntervalPattern("Seventh major", Interval.make(diatonic=6, chromatic=11)),
    IntervalPattern("Octave", Interval.make(diatonic=7, chromatic=12)),


    IntervalPattern("Unison augmented", Interval.make(diatonic=0, chromatic=1)),
    IntervalPattern("Second diminished", Interval.make(diatonic=1, chromatic=0)),
    IntervalPattern("Second augmented", Interval.make(diatonic=1, chromatic=3)),
    IntervalPattern("Third dimished", Interval.make(diatonic=2, chromatic=3)),
    IntervalPattern("Third augmented", Interval.make(diatonic=2, chromatic=5)),
    IntervalPattern("Fourth diminished", Interval.make(diatonic=3, chromatic=4)),
    IntervalPattern("Fifth diminished", Interval.make(diatonic=5, chromatic=6)),
    IntervalPattern("Fifth augmented", Interval.make(diatonic=5, chromatic=8)),
    IntervalPattern("Sixth diminished", Interval.make(diatonic=5, chromatic=7)),
    IntervalPattern("Sixth augmented", Interval.make(diatonic=5, chromatic=10)),
    IntervalPattern("Seventh diminished", Interval.make(diatonic=6, chromatic=9)),
    IntervalPattern("Seventh augmented", Interval.make(diatonic=6, chromatic=12)),
    IntervalPattern("Octave diminished", Interval.make(diatonic=7, chromatic=11)),
    IntervalPattern("Octave augmented", Interval.make(diatonic=7, chromatic=13)),
]