import unittest

from solfege.interval import ChromaticInterval
from solfege.interval.abstract import AbstractInterval


class DiatonicInterval(AbstractInterval):
    """An interval, where we count the number of note in the major scale,
    and ignore the note which are absent. B and B# can't be
    distinguished, since A# does not really exist. However, this would
    allow to distinguish between B# and C"""
    number_of_interval_in_an_octave = 7

    # RelatedChromaticClass = ChromaticInterval moved to __init__

    def __add__(self, other):
        if not isinstance(other, DiatonicInterval):
            raise Exception(
                "Adding a DiatonicInterval interval to something which is not a DiatonicInterval but %s" % other)
        return super().__add__(other)

    def get_chromatic(self, scale="Major") -> ChromaticInterval:
        """
        Give the chromatic interval associated to the current diatonic interval in some scale.
          By default, the scale is the major one."""
        # TODO scale= scale.dic[scale] currently, only major is used
        return self.RelatedChromaticClass(12 * self.get_octave() + [0, 2, 4, 5, 7, 9, 11][self.get_number() % 7])

    def get_interval_name(self, showOctave=True):
        if self.get_number() == 0:
            return "unison"
        size = abs(self.get_number())
        role = size % 7
        nb_octave = size // 7
        text = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh"][role]

        if nb_octave > 0 and showOctave:
            prefix = f"{nb_octave} octaves" if (nb_octave > 1) else "octave"
            if role != 0:
                text = f"{prefix} and {text}"
            else:
                text = prefix
        if self.get_number() < 0:
            text += " decreasing"
        return text


DiatonicInterval.IntervalClass = DiatonicInterval


