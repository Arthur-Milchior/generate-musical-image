import unittest
from typing import Optional

from solfege.interval.interval import _Interval


class ChromaticInterval(_Interval):
    """A chromatic interval. Counting the number of half tone between two notes"""
    modulo = 12

    """the diatonic class to which such a chromatic class must be converted"""
    # RelatedDiatonicClass = solfege.Interval.diatonic.DiatonicInterval
    # moved to init because cyclic dependencies

    def __init__(self, chromatic=None, value=None, **kwargs):
        if value is None:
            assert (chromatic is not None)
            value = chromatic
        else:
            assert (chromatic is None)
        super().__init__(value=value, callerClass=ChromaticInterval, **kwargs)

    def __add__(self, other):
        if not isinstance(other, ChromaticInterval):
            raise Exception(
                f"Adding a ChromaticInterval interval to something which is not a ChromaticInterval but {other}")
        return super().__add__(other)

    def get_diatonic(self):
        """If this note belong to the diatonic scale, give it.
        Otherwise, give the adjacent diatonic note."""
        if "diatonic" not in self.dic:
            diatonic = self.RelatedDiatonicClass(diatonic=[0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6][
                                                              self.get_same_note_in_base_octave().get_number()] + 7 * self.get_octave())
            self.dic["diatonic"] = diatonic
        return self.dic["diatonic"]

    def get_alteration(self):
        """The alteration, added to `self.getDiatonic()` to obtain `self`"""
        import solfege.interval.alteration
        chromaticFromDiatonic = self.get_diatonic().get_chromatic()
        try:
            return solfege.interval.alteration.Alteration(chromatic=self.get_number() - chromaticFromDiatonic.get_number())
        except solfege.interval.alteration.TooBigAlteration as tba:
            tba.addInformation("Solfege interval", self)
            raise

    def get_solfege(self, diatonicNumber: Optional[int] = None):
        """A note. Same chromatic. Diatonic is as close as possible (see getDiatonicNote) or is the note given."""
        if diatonicNumber is None:
            diatonic = self.get_diatonic().get_number()
        return self.RelatedSolfegeClass(diatonic=diatonic, chromatic=self.get_number())

    def get_name(self, kind=None, octave=True, side=False):
        """The name of the interval.

        octave -- For example: if this variable is set true, the name is given as "supertonic and one octave".
        Otherwise, if it is set to None, the variable is given as "eight"

        side -- Whether to add "increasing" or "decreasing"

        kind -- if a number is given, then we consider that we want major/minor, and not a full name
        todo
        """
        if self < 0:
            name = (-self).get_name(kind=kind, octave=octave, side=False)
            if side:
                return name + " decreasing"
            else:
                return name
        if octave:
            nbOctave = self.get_octave()
            pos = self.get_number() % 12
            if nbOctave > 1:
                name = "%d octaves" % nbOctave
            elif nbOctave == 1:
                name = "An octave"
            else:
                name = ""
            nameBis = \
                ["" if nbOctave else "unison", "second minor", "second major", "third minor", "third major", "fourth",
                 "tritone", "fifth", "sixth minor", "sixth major", "seventh minor", "seventh major"][pos]
            if nameBis:
                name += "and " + nameBis
            if side:
                name += " increasing"
            return name


ChromaticInterval.IntervalClass = ChromaticInterval


class TestChromaticInterval(unittest.TestCase):
    zero = ChromaticInterval(0)
    un = ChromaticInterval(1)
    moins_un = ChromaticInterval(-1)
    deux = ChromaticInterval(2)
    trois = ChromaticInterval(3)
    sept = ChromaticInterval(7)
    six = ChromaticInterval(6)
    onze = ChromaticInterval(11)
    douze = ChromaticInterval(12)
    moins_six = ChromaticInterval(-6)
    moins_sept = ChromaticInterval(-7)
    moins_huit = ChromaticInterval(-8)
    moins_onze = ChromaticInterval(-11)
    moins_douze = ChromaticInterval(-12)
    moins_treize = ChromaticInterval(-13)

    def test_is_note(self):
        self.assertFalse(self.zero.is_note())

    def test_has_number(self):
        self.assertTrue(self.zero.has_number())

    def test_get_number(self):
        self.assertEquals(self.zero.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.zero, self.zero)
        self.assertNotEquals(self.un, self.zero)
        self.assertEquals(self.un, self.un)

    def test_add(self):
        self.assertEquals(self.un + self.deux, self.trois)

    def test_neg(self):
        self.assertEquals(-self.un, self.moins_un)

    def test_sub(self):
        self.assertEquals(self.trois - self.deux, self.un)

    def test_lt(self):
        self.assertLess(self.un, self.deux)
        self.assertLessEqual(self.un, self.deux)
        self.assertLessEqual(self.un, self.un)

    def test_repr(self):
        self.assertEquals(repr(self.un), "ChromaticInterval(1)")

    def test_get_octave(self):
        self.assertEquals(self.zero.get_octave(), 0)
        self.assertEquals(self.six.get_octave(), 0)
        self.assertEquals(self.moins_onze.get_octave(), -1)
        self.assertEquals(self.moins_douze.get_octave(), -1)
        self.assertEquals(self.moins_treize.get_octave(), -2)
        self.assertEquals(self.douze.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(self.douze.add_octave(-1), self.zero)
        self.assertEquals(self.zero.add_octave(1), self.douze)
        self.assertEquals(self.douze.add_octave(-2), self.moins_douze)
        self.assertEquals(self.moins_douze.add_octave(2), self.douze)

    def test_same_note_in_base_octave(self):
        self.assertEquals(self.douze.get_same_note_in_base_octave(), self.zero)
        self.assertEquals(self.moins_douze.get_same_note_in_base_octave(), self.zero)
        self.assertEquals(self.zero.get_same_note_in_base_octave(), self.zero)
        self.assertEquals(self.un.get_same_note_in_base_octave(), self.un)
        self.assertEquals(self.moins_un.get_same_note_in_base_octave(), self.onze)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.un.same_notes_in_different_octaves(self.zero))
        self.assertFalse(self.un.same_notes_in_different_octaves(self.douze))
        self.assertFalse(self.un.same_notes_in_different_octaves(self.moins_douze))
        self.assertFalse(self.un.same_notes_in_different_octaves(self.moins_un))
        self.assertTrue(self.zero.same_notes_in_different_octaves(self.zero))
        self.assertTrue(self.zero.same_notes_in_different_octaves(self.douze))
        self.assertTrue(self.zero.same_notes_in_different_octaves(self.moins_douze))
        self.assertTrue(self.douze.same_notes_in_different_octaves(self.moins_douze))
        
    def test_get_diatonic(self):
        from solfege.interval.diatonic import DiatonicInterval
        self.assertEquals(ChromaticInterval(0).get_diatonic(), DiatonicInterval(0))
        self.assertEquals(ChromaticInterval(1).get_diatonic(), DiatonicInterval(0))
        self.assertEquals(ChromaticInterval(2).get_diatonic(), DiatonicInterval(1))
        self.assertEquals(ChromaticInterval(3).get_diatonic(), DiatonicInterval(2))
        self.assertEquals(ChromaticInterval(4).get_diatonic(), DiatonicInterval(2))
        self.assertEquals(ChromaticInterval(5).get_diatonic(), DiatonicInterval(3))
        self.assertEquals(ChromaticInterval(6).get_diatonic(), DiatonicInterval(3))
        self.assertEquals(ChromaticInterval(7).get_diatonic(), DiatonicInterval(4))
        self.assertEquals(ChromaticInterval(8).get_diatonic(), DiatonicInterval(5))
        self.assertEquals(ChromaticInterval(9).get_diatonic(), DiatonicInterval(5))
        self.assertEquals(ChromaticInterval(10).get_diatonic(), DiatonicInterval(6))
        self.assertEquals(ChromaticInterval(11).get_diatonic(), DiatonicInterval(6))
        self.assertEquals(ChromaticInterval(12).get_diatonic(), DiatonicInterval(7))
        self.assertEquals(ChromaticInterval(13).get_diatonic(), DiatonicInterval(7))
        self.assertEquals(ChromaticInterval(14).get_diatonic(), DiatonicInterval(8))
        self.assertEquals(ChromaticInterval(-1).get_diatonic(), DiatonicInterval(-1))
        self.assertEquals(ChromaticInterval(-2).get_diatonic(), DiatonicInterval(-1))
        self.assertEquals(ChromaticInterval(-3).get_diatonic(), DiatonicInterval(-2))
        self.assertEquals(ChromaticInterval(-4).get_diatonic(), DiatonicInterval(-2))
        self.assertEquals(ChromaticInterval(-5).get_diatonic(), DiatonicInterval(-3))
        self.assertEquals(ChromaticInterval(-6).get_diatonic(), DiatonicInterval(-4))
        self.assertEquals(ChromaticInterval(-7).get_diatonic(), DiatonicInterval(-4))
        self.assertEquals(ChromaticInterval(-8).get_diatonic(), DiatonicInterval(-5))
        self.assertEquals(ChromaticInterval(-9).get_diatonic(), DiatonicInterval(-5))
        self.assertEquals(ChromaticInterval(-10).get_diatonic(), DiatonicInterval(-6))
        self.assertEquals(ChromaticInterval(-11).get_diatonic(), DiatonicInterval(-7))
        self.assertEquals(ChromaticInterval(-12).get_diatonic(), DiatonicInterval(-7))
        self.assertEquals(ChromaticInterval(-13).get_diatonic(), DiatonicInterval(-8))
        self.assertEquals(ChromaticInterval(-14).get_diatonic(), DiatonicInterval(-8))

    def test_get_solfege(self):
        from solfege.interval.solfege import SolfegeInterval
        self.assertEquals(ChromaticInterval(0).get_solfege(), SolfegeInterval(0, 0))
        self.assertEquals(ChromaticInterval(1).get_solfege(), SolfegeInterval(1, 0))
        self.assertEquals(ChromaticInterval(2).get_solfege(), SolfegeInterval(2, 1))
        self.assertEquals(ChromaticInterval(3).get_solfege(), SolfegeInterval(3, 2))
        self.assertEquals(ChromaticInterval(4).get_solfege(), SolfegeInterval(4, 2))
        self.assertEquals(ChromaticInterval(5).get_solfege(), SolfegeInterval(5, 3))
        self.assertEquals(ChromaticInterval(6).get_solfege(), SolfegeInterval(6, 3))
        self.assertEquals(ChromaticInterval(7).get_solfege(), SolfegeInterval(7, 4))
        self.assertEquals(ChromaticInterval(8).get_solfege(), SolfegeInterval(8, 5))
        self.assertEquals(ChromaticInterval(9).get_solfege(), SolfegeInterval(9, 5))
        self.assertEquals(ChromaticInterval(10).get_solfege(), SolfegeInterval(10, 6))
        self.assertEquals(ChromaticInterval(11).get_solfege(), SolfegeInterval(11, 6))
        self.assertEquals(ChromaticInterval(12).get_solfege(), SolfegeInterval(12, 7))
        self.assertEquals(ChromaticInterval(13).get_solfege(), SolfegeInterval(13, 7))
        self.assertEquals(ChromaticInterval(14).get_solfege(), SolfegeInterval(14, 8))
        self.assertEquals(ChromaticInterval(-1).get_solfege(), SolfegeInterval(-1, -1))
        self.assertEquals(ChromaticInterval(-2).get_solfege(), SolfegeInterval(-2, -1))
        self.assertEquals(ChromaticInterval(-3).get_solfege(), SolfegeInterval(-3, -2))
        self.assertEquals(ChromaticInterval(-4).get_solfege(), SolfegeInterval(-4, -2))
        self.assertEquals(ChromaticInterval(-5).get_solfege(), SolfegeInterval(-5, -3))
        self.assertEquals(ChromaticInterval(-6).get_solfege(), SolfegeInterval(-6, -4))
        self.assertEquals(ChromaticInterval(-7).get_solfege(), SolfegeInterval(-7, -4))
        self.assertEquals(ChromaticInterval(-8).get_solfege(), SolfegeInterval(-8, -5))
        self.assertEquals(ChromaticInterval(-9).get_solfege(), SolfegeInterval(-9, -5))
        self.assertEquals(ChromaticInterval(-10).get_solfege(), SolfegeInterval(-10, -6))
        self.assertEquals(ChromaticInterval(-11).get_solfege(), SolfegeInterval(-11, -7))
        self.assertEquals(ChromaticInterval(-12).get_solfege(), SolfegeInterval(-12, -7))
        self.assertEquals(ChromaticInterval(-13).get_solfege(), SolfegeInterval(-13, -8))
        self.assertEquals(ChromaticInterval(-14).get_solfege(), SolfegeInterval(-14, -8))

    def test_get_alteration(self):
        from solfege.interval.alteration import Alteration
        self.assertEquals(ChromaticInterval(0).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(1).get_alteration(), Alteration(1))
        self.assertEquals(ChromaticInterval(2).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(3).get_alteration(), Alteration(-1))
        self.assertEquals(ChromaticInterval(4).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(5).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(6).get_alteration(), Alteration(1))
        self.assertEquals(ChromaticInterval(7).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(8).get_alteration(), Alteration(-1))
        self.assertEquals(ChromaticInterval(9).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(10).get_alteration(), Alteration(-1))
        self.assertEquals(ChromaticInterval(11).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(12).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(13).get_alteration(), Alteration(1))
        self.assertEquals(ChromaticInterval(14).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-1).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-2).get_alteration(), Alteration(-1))
        self.assertEquals(ChromaticInterval(-3).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-4).get_alteration(), Alteration(-1))
        self.assertEquals(ChromaticInterval(-5).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-6).get_alteration(), Alteration(1))
        self.assertEquals(ChromaticInterval(-7).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-8).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-9).get_alteration(), Alteration(-1))
        self.assertEquals(ChromaticInterval(-10).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-11).get_alteration(), Alteration(1))
        self.assertEquals(ChromaticInterval(-12).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-13).get_alteration(), Alteration(0))
        self.assertEquals(ChromaticInterval(-14).get_alteration(), Alteration(-1))