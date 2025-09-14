from dataclasses import dataclass
from typing import ClassVar, Dict, Iterator, List, Type, Union
from solfege.pattern.solfege_pattern import SolfegePattern
from solfege.value.interval.interval import Interval

@dataclass(frozen=True)
class IntervalPattern(SolfegePattern):
    """A pattern for a single interval."""

    """See SoflegePattern"""
    name_to_pattern: ClassVar[Dict[str, "IntervalPattern"]] = dict()
    all_patterns: ClassVar[List['IntervalPattern']] = list()
    
    @classmethod
    def _get_instantiation_type(cls) -> Type["Chord"]:
        return NotImplemented

    @classmethod
    def _new_record_keeper(cls):
        # we won't record interval
        return NotImplemented

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def singleton(x):
            return [x]
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "name", singleton)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "interval", lambda interval: [Interval.make(0,0), Interval.make_single_argument(interval)])
        kwargs["record"] = False
        kwargs["names"] = kwargs["name"]
        kwargs["_absolute_intervals"] = kwargs["interval"]
        del kwargs["name"]
        del kwargs["interval"]
        return super()._clean_arguments_for_constructor(args, kwargs)


second_minor_interval = Interval.make(diatonic=1, chromatic=1)
second_minor_pattern = IntervalPattern.make(name="Second minor", interval=second_minor_interval)
intervals_up_to_octave = [
    second_minor_pattern,
    IntervalPattern.make(name="Second major", interval=Interval.make(diatonic=1, chromatic=2)),
    IntervalPattern.make(name="Third minor", interval=Interval.make(diatonic=2, chromatic=3)),
    IntervalPattern.make(name="Third major", interval=Interval.make(diatonic=2, chromatic=4)),
    IntervalPattern.make(name="Fourth just", interval=Interval.make(diatonic=3, chromatic=5)),
    IntervalPattern.make(name="Fourth augmented", interval=Interval.make(diatonic=3, chromatic=6)),
    IntervalPattern.make(name="Fifth just", interval=Interval.make(diatonic=5, chromatic=7)),
    IntervalPattern.make(name="Sixth minor", interval=Interval.make(diatonic=5, chromatic=8)),
    IntervalPattern.make(name="Sixth major", interval=Interval.make(diatonic=5, chromatic=9)),
    IntervalPattern.make(name="Seventh minor", interval=Interval.make(diatonic=6, chromatic=10)),
    IntervalPattern.make(name="Seventh major", interval=Interval.make(diatonic=6, chromatic=11)),
    IntervalPattern.make(name="Octave", interval=Interval.make(diatonic=7, chromatic=12)),


    IntervalPattern.make(name="Unison augmented", interval=Interval.make(diatonic=0, chromatic=1)),
    IntervalPattern.make(name="Second augmented", interval=Interval.make(diatonic=1, chromatic=3)),
    IntervalPattern.make(name="Third dimished", interval=Interval.make(diatonic=2, chromatic=3)),
    IntervalPattern.make(name="Third augmented", interval=Interval.make(diatonic=2, chromatic=5)),
    IntervalPattern.make(name="Fourth diminished", interval=Interval.make(diatonic=3, chromatic=4)),
    IntervalPattern.make(name="Fifth diminished", interval=Interval.make(diatonic=5, chromatic=6)),
    IntervalPattern.make(name="Fifth augmented", interval=Interval.make(diatonic=5, chromatic=8)),
    IntervalPattern.make(name="Sixth diminished", interval=Interval.make(diatonic=5, chromatic=7)),
    IntervalPattern.make(name="Sixth augmented", interval=Interval.make(diatonic=5, chromatic=10)),
    IntervalPattern.make(name="Seventh diminished", interval=Interval.make(diatonic=6, chromatic=9)),
    IntervalPattern.make(name="Seventh augmented", interval=Interval.make(diatonic=6, chromatic=12)),
    IntervalPattern.make(name="Octave diminished", interval=Interval.make(diatonic=7, chromatic=11)),
    IntervalPattern.make(name="Octave augmented", interval=Interval.make(diatonic=7, chromatic=13)),
]


  #  IntervalPattern.make(name="Second diminished", interval=Interval.make(diatonic=1, chromatic=0)),
  # interval list assume no repetition. maybe correct one day,