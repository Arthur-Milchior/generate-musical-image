import unittest
from typing import Optional

from solfege.interval.chromatic import ChromaticInterval
from solfege.interval.diatonic import DiatonicInterval


class SolfegeInterval:
    pass


class SolfegeInterval(ChromaticInterval):
    """A solfège interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass = DiatonicInterval
    ChromaticClass = ChromaticInterval

    def __init__(self, chromatic: Optional[int] = None, diatonic: Optional[int] = None, alteration: Optional[int] =None,
                 toCopy: Optional[SolfegeInterval] = None,
                 none=None, **kwargs):
        """If toCopy is present, it is copied

        Otherwise, chromatic and diatonic are used.
        Otherwise, if chromatic is present, it supposed to be the exact value.
        otherwise, alteration should be present, and chromatic is the sum of diatonic and alteration
        """
        assert (alteration is not None or chromatic is not None or toCopy is not None or none is not None)
        if none:
            super().__init__(none=none)
            assert (chromatic is None)
            assert (diatonic is None)
            assert (alteration is None)
            assert (toCopy is None)
        elif toCopy:
            assert (chromatic is None)
            assert (diatonic is None)
            assert (alteration is None)
            assert (isinstance(toCopy, SolfegeInterval))
            super().__init__(chromatic=toCopy.getNumber())
            self.diatonic = toCopy.getDiatonic()
        else:
            self.diatonic = self.DiatonicClass(diatonic=diatonic)
            if chromatic is not None:
                assert (isinstance(chromatic, int))
                super().__init__(chromatic=chromatic)
            else:
                assert alteration
                assert (isinstance(alteration, int))
                self.initChromaticAbsent(alteration)
                super().__init__(chromatic=self.diatonic.get_chromatic().get_number() + alteration)

    def __eq__(self, other):
        diatonicEq = self.get_diatonic() == other.get_diatonic()
        chromaticEq = super().__eq__(other)
        return diatonicEq and chromaticEq

    def __hash__(self):
        return hash(self.get_chromatic())

    def __neg__(self):
        Class = self.ClassToTransposeTo or self.__class__
        return Class(chromatic=-self.get_number(), diatonic=-self.get_diatonic().get_number())

    def get_chromatic(self):
        return self.ChromaticClass(chromatic=self.get_number())

    def get_diatonic(self):
        return self.diatonic

    def __repr__(self):
        return f"{self.__class__.__name__}(chromatic = {self.get_chromatic().get_number()}, diatonic = { self.get_diatonic().get_number()})"

    def __add__(self, other):
        if not isinstance(other, SolfegeInterval):
            raise Exception("Adding a solfege interval to something which is not a solfege interval")
        diatonic = self.get_diatonic().get_number() + other.get_diatonic().get_number()
        chromatic = self.get_chromatic().get_number() + other.get_chromatic().get_number()
        Class = self.ClassToTransposeTo or self.__class__
        interval = Class(chromatic=chromatic, diatonic=diatonic)
        return interval

    def add_octave(self, nb):
        Class = self.ClassToTransposeTo or self.__class__
        return Class(chromatic=self.get_chromatic().add_octave(nb).get_number(),
                     diatonic=self.get_diatonic().add_octave(nb).get_number())

    def get_octave(self):
        return self.get_diatonic().get_octave()

    def get_same_note_in_base_octave(self):
        octaveToAdd = -self.get_octave()
        return self.add_octave(octaveToAdd)

ChromaticInterval.RelatedSolfegeClass = SolfegeInterval
SolfegeInterval.IntervalClass = SolfegeInterval


class TestChromaticInterval(unittest.TestCase):
    minus_octave = SolfegeInterval(-12, -7)
    minus_second_minor = SolfegeInterval(-1, -1)
    unison = SolfegeInterval(0, 0)
    second_minor = SolfegeInterval(1, 1)
    second_major = SolfegeInterval(2, 1)
    third_minor = SolfegeInterval(3, 2)
    octave = SolfegeInterval(12, 7)

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())

    def test_has_number(self):
        self.assertTrue(self.unison.has_number())

    def test_get_number(self):
        self.assertEquals(self.unison.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.unison, self.unison)
        self.assertNotEquals(self.second_major, self.unison)
        self.assertEquals(self.second_major, self.second_major)

    def test_add(self):
        self.assertEquals(self.second_major + self.second_minor, self.third_minor)

    def test_neg(self):
        self.assertEquals(-self.second_minor, self.minus_second_minor)

    def test_sub(self):
        self.assertEquals(self.third_minor - self.second_major, self.second_minor)

    def test_lt(self):
        self.assertLess(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_major, self.second_major)

    def test_repr(self):
        self.assertEquals(repr(self.second_major), "SolfegeInterval(chromatic = 2, diatonic = 1)")

    def test_get_octave(self):
        self.assertEquals(self.unison.get_octave(), 0)
        self.assertEquals(self.minus_octave.get_octave(), -1)
        self.assertEquals(self.octave.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(self.octave.add_octave(-1), self.unison)
        self.assertEquals(self.unison.add_octave(1), self.octave)
        self.assertEquals(self.octave.add_octave(-2), self.minus_octave)
        self.assertEquals(self.minus_octave.add_octave(2), self.octave)

    def test_same_note_in_base_octave(self):
        self.assertEquals(self.octave.get_same_note_in_base_octave(), self.unison)
        self.assertEquals(self.minus_octave.get_same_note_in_base_octave(), self.unison)
        self.assertEquals(self.unison.get_same_note_in_base_octave(), self.unison)
        self.assertEquals(self.second_major.get_same_note_in_base_octave(), self.second_major)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.second_major.same_notes_in_different_octaves(self.unison))
        self.assertFalse(self.second_major.same_notes_in_different_octaves(self.octave))
        self.assertFalse(self.second_major.same_notes_in_different_octaves(self.minus_octave))
        self.assertTrue(self.unison.same_notes_in_different_octaves(self.unison))
        self.assertTrue(self.unison.same_notes_in_different_octaves(self.octave))
        self.assertTrue(self.unison.same_notes_in_different_octaves(self.minus_octave))
        self.assertTrue(self.octave.same_notes_in_different_octaves(self.minus_octave))
