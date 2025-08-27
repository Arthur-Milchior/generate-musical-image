from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, Iterable

from solfege.interval.interval import Interval
from solfege.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalType
from utils.util import assert_all_same_class


class Third(Enum):
    MINOR = "minor"
    MAJOR = "major"
    NONE = "none"
    BOTH = "both"

class Fifth(Enum):
    JUST = "just"
    AUGMENTED = "augmented"
    DIMINISHED = "diminished"
    NONE = "none"
    MULTIPLE = "multiple"
    """Not osemthing that should occurs with diminished"""
    NOT_APPLICABLE = "not applicable"

class Quality(Enum):
    NONE = "NONE"
    MULTIPLE = "multiple"
    SIXTH = "sixth"
    SEVENTH_MINOR = "SEVENTH MINOR"
    SEVENTH_MAJOR = "SEVENTH MAJOR"

@dataclass(frozen=True)
class SetOfIntervals(Generic[ChromaticIntervalType]): # type: ignore
    """A set of intervals.
    
    """
    intervals: frozenset[ChromaticInterval]

    @classmethod
    def make(cls, intervals: Iterable[ChromaticInterval]):
        intervals_in_base_octave = frozenset({interval.in_base_octave() for interval in intervals})
        return cls(intervals_in_base_octave)

    def __post_init__(self):
        # Checks all elements have the same class
        assert_all_same_class(self.intervals)
        for interval in self.intervals:
            assert interval == interval.in_base_octave()

    def __repr__(self):
        return f"""{self.__class__.__name__}(intervals = {self.intervals})"""

    def __contains__(self, interval: ChromaticInterval):
        """Whether this note belongs to the set (up to octave)"""
        return interval.in_base_octave() in self.intervals

    def __iter__(self):
        """Intervals belonging to this set."""
        l = list(self.intervals)
        l.sort()
        return iter(l)

    def __add__(self, other: Interval):
        from solfege.note.note import Note
        from solfege.note.set.set_of_notes import SetOfNotes
        if isinstance(other, Note):
            return SetOfNotes([interval + other for interval in self.intervals])
        return SetOfIntervals.make([interval + other for interval in self.intervals])

    def __eq__(self, other: SetOfIntervals[ChromaticInterval]):
        return self.intervals == other.intervals

    def __repr__(self):
        return f"""SetOfIntervals.make(set_={self.intervals})"""
    
    def inversion(self, new_bass: Interval):
        return (self + (-new_bass))

    def inversions(self):
        for inversion, interval in enumerate(self):
            yield Inversion(inversion, self.inversion(interval))

    def is_minor(self):
        return ChromaticInterval(3) in self

    def contains_tonic(self):
        return ChromaticInterval(0) in self

    def is_major(self):
        return ChromaticInterval(4) in self

    def third(self) -> Third:
        """The kind of third(s) of this chord"""
        if self.is_minor():
            if self.is_major():
                return Third.BOTH
            else:
                return Third.MINOR
        elif self.is_major():
            return Third.MAJOR
        else:
            return Third.NONE

    def is_fifth_dimished(self):
        return ChromaticInterval(6) in self

    def is_fifth_augmented(self):
        return ChromaticInterval(8) in self

    def is_fifth_just(self):
        return ChromaticInterval(7) in self

    def fifth(self):
        """If the 5th is diminished, and third is minor return "diminished".
        If the 5th is just, return the empty string.
        Otherwise return false
        """
        augmented = self.is_fifth_augmented()
        diminished = self.is_fifth_dimished()
        just = self.is_fifth_just()
        numberFifth = len([fifth for fifth in [just, diminished, augmented] if fifth])
        if numberFifth == 0:
            return Fifth.NONE
        elif numberFifth > 1:
            return Fifth.MULTIPLE
        elif diminished:
            if self.is7th_maj() or self.is7th_min():
                return Fifth.NOT_APPLICABLE
            else:
                return Fifth.DIMINISHED
        elif just:
            return Fifth.JUST
        elif augmented:
            if self.is6th() or self.is7th_min():
                return Fifth.NOT_APPLICABLE
            else:
                return Fifth.AUGMENTED

    def has_quality(self):
        """Whether there is no 6th nor 7th"""
        return (self.is6th() or self.is7th_min() or self.is7th_maj())

    def is6th(self):
        return ChromaticInterval(9) in self

    def is7th_min(self):
        return ChromaticInterval(10) in self

    def is7th_maj(self):
        return ChromaticInterval(11) in self

    def quality(self):
        """The quality of the chord. False if it has multiple potential note which can be considered as distinct quality."""
        sixth = self.is6th()
        seventhMinor = self.is7th_min()
        seventhMajor = self.is7th_maj()
        numberQuality = len([quality for quality in [sixth, seventhMajor, seventhMinor] if quality])
        if numberQuality == 0:
            return  Quality.NONE
        elif numberQuality > 1:
            return  Quality.MULTIPLE
        elif sixth:
            return  Quality.SIXTH
        elif seventhMinor:
            return  Quality.SEVENTH_MINOR
        assert seventhMajor
        return  Quality.SEVENTH_MAJOR

    # def contains567(self):
    #     """Whether it has a fifth or a quality"""
    #     return  (self.fifth() not in {} or self.quality())

    def get_pattern(self):
        from solfege.chord.chord_pattern import ChordPattern
        return ChordPattern.get_pattern_from_chromatic_interval(self.intervals)
    
    def get_pattern_name(self):
        chord = self.get_pattern()
        if chord is None:
            return None
        else:
            return chord.first_of_the_names()
    
@dataclass(frozen=True)
class Inversion:
    inversion: int
    intervals: SetOfIntervals