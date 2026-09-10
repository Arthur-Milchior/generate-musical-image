from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, Iterator, List, Tuple, Type, Union
from solfege.pattern.solfege_pattern import SolfegePattern
from solfege.value.interval.interval import Interval
from utils.recording.record_keeper import RecordKeeperType

@dataclass(frozen=True)
class IntervalPattern(SolfegePattern, ABC):
    """A pattern for a single interval (e.g. "Third major"), as opposed to a chord/scale pattern which
    holds several intervals. Built from a name and a single `interval` argument (relative to the
    unison); see module-level `intervals_up_to_octave` below for the full registered list."""

    """See SoflegePattern"""
    name_to_pattern: ClassVar[Dict[str, "IntervalPattern"]] = dict()
    """Registry of all `IntervalPattern` instances, keyed by name (see `SolfegePattern`)."""
    all_patterns: ClassVar[List['IntervalPattern']] = list()
    """All registered `IntervalPattern` instances, in creation order (see `SolfegePattern`)."""

    @classmethod
    def _get_instantiation_type(cls) -> Type["Chord"]:
        """Interval patterns are never instantiated into a concrete note-holding object, unlike
        chords/scales."""
        # We won't instantiate those
        return NotImplemented

    @classmethod
    def _new_record_keeper(cls) -> RecordKeeperType:
        """Interval patterns are not recorded in a `RecordKeeper` (there's no "which interval pattern
        matches this interval" lookup use case, unlike chords/scales)."""
        # we won't record interval
        return NotImplemented

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Translate the constructor's simplified `name`/`interval` arguments into the underlying
        `SolfegePattern` fields: wraps `name` into a singleton `names` list, disables recording, and
        builds `_absolute_intervals` as `[unison, interval]` (every pattern starts from the unison)."""
        def singleton(x: str) -> List[str]:
            """Wrap `x` in a single-element list."""
            return [x]
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "name", singleton)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "interval", lambda interval: [Interval.make(0,0), Interval.make_single_argument(interval)])
        kwargs["record"] = False
        kwargs["names"] = kwargs["name"]
        kwargs["_absolute_intervals"] = kwargs["interval"]
        del kwargs["name"]
        del kwargs["interval"]
        return super()._clean_arguments_for_constructor(args, kwargs)


second_minor_interval = Interval.make(_diatonic=1, _chromatic=1)
second_minor_pattern = IntervalPattern.make(name="Second minor", interval=second_minor_interval)
intervals_up_to_octave = [
    second_minor_pattern,
    IntervalPattern.make(name="Second major", interval=Interval.make(_diatonic=1, _chromatic=2)),
    IntervalPattern.make(name="Third minor", interval=Interval.make(_diatonic=2, _chromatic=3)),
    IntervalPattern.make(name="Third major", interval=Interval.make(_diatonic=2, _chromatic=4)),
    IntervalPattern.make(name="Fourth just", interval=Interval.make(_diatonic=3, _chromatic=5)),
    IntervalPattern.make(name="Fourth augmented", interval=Interval.make(_diatonic=3, _chromatic=6)),
    IntervalPattern.make(name="Fifth just", interval=Interval.make(_diatonic=5, _chromatic=7)),
    IntervalPattern.make(name="Sixth minor", interval=Interval.make(_diatonic=5, _chromatic=8)),
    IntervalPattern.make(name="Sixth major", interval=Interval.make(_diatonic=5, _chromatic=9)),
    IntervalPattern.make(name="Seventh minor", interval=Interval.make(_diatonic=6, _chromatic=10)),
    IntervalPattern.make(name="Seventh major", interval=Interval.make(_diatonic=6, _chromatic=11)),
    IntervalPattern.make(name="Octave", interval=Interval.make(_diatonic=7, _chromatic=12)),


    IntervalPattern.make(name="Unison augmented", interval=Interval.make(_diatonic=0, _chromatic=1)),
    IntervalPattern.make(name="Second augmented", interval=Interval.make(_diatonic=1, _chromatic=3)),
    IntervalPattern.make(name="Third dimished", interval=Interval.make(_diatonic=2, _chromatic=3)),
    IntervalPattern.make(name="Third augmented", interval=Interval.make(_diatonic=2, _chromatic=5)),
    IntervalPattern.make(name="Fourth diminished", interval=Interval.make(_diatonic=3, _chromatic=4)),
    IntervalPattern.make(name="Fifth diminished", interval=Interval.make(_diatonic=5, _chromatic=6)),
    IntervalPattern.make(name="Fifth augmented", interval=Interval.make(_diatonic=5, _chromatic=8)),
    IntervalPattern.make(name="Sixth diminished", interval=Interval.make(_diatonic=5, _chromatic=7)),
    IntervalPattern.make(name="Sixth augmented", interval=Interval.make(_diatonic=5, _chromatic=10)),
    IntervalPattern.make(name="Seventh diminished", interval=Interval.make(_diatonic=6, _chromatic=9)),
    IntervalPattern.make(name="Seventh augmented", interval=Interval.make(_diatonic=6, _chromatic=12)),
    IntervalPattern.make(name="Octave diminished", interval=Interval.make(_diatonic=7, _chromatic=11)),
    IntervalPattern.make(name="Octave augmented", interval=Interval.make(_diatonic=7, _chromatic=13)),
]


  #  IntervalPattern.make(name="Second diminished", interval=Interval.make(_diatonic=1, _chromatic=0)),
  # interval list assume no repetition. maybe correct one day,