import unittest

from solfege.interval.abstract import AbstractInterval


class DiatonicInterval(AbstractInterval):
    """An interval, where we count the number of notes in the major scale,
    and ignore the notes which are absent. B and B# can't be
    distinguished, since A# does not really exist. However, this would
    allow to distinguish between B# and C"""
    number_of_interval_in_an_octave = 7

    # RelatedChromaticClass = ChromaticInterval moved to __init__

    def __init__(self, diatonic=None, value=None, **kwargs):
        if value is None:
            assert (diatonic is not None)
            value = diatonic
        else:
            assert (diatonic is None)
        super().__init__(value=value, callerClass=DiatonicInterval, **kwargs)

    def __add__(self, other):
        if not isinstance(other, DiatonicInterval):
            raise Exception(
                "Adding a DiatonicInterval interval to something which is not a DiatonicInterval but %s" % other)
        return super().__add__(other)

    def get_chromatic(self, scale="Major"):
        """
        Give the chromatic interval associated to the current diatonic interval in some scale.
          By default, the scale is the major one."""
        # TODO scale= Scale.dic[scale] currently, only major is used
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

    def lily_octave(self):
        """The string which allow to obtain correct octave in lilypond."""
        octave = self.get_octave()
        octave_shift = octave + 1
        if octave_shift > 0:
            return "'" * octave_shift
        elif octave_shift < 0:
            return "," * (-octave_shift)
        else:
            return ""


DiatonicInterval.IntervalClass = DiatonicInterval


class TestDiatonicInterval(unittest.TestCase):
    unison = DiatonicInterval(0)
    second = DiatonicInterval(1)
    second_descending = DiatonicInterval(-1)
    third = DiatonicInterval(2)
    fourth = DiatonicInterval(3)
    octave = DiatonicInterval(7)
    seventh = DiatonicInterval(6)
    seventh_descending = DiatonicInterval(-6)
    octave_descending = DiatonicInterval(-7)
    second_twice_descending = DiatonicInterval(-8)

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())

    def test_has_number(self):
        self.assertTrue(self.unison.has_number())

    def test_get_number(self):
        self.assertEquals(self.unison.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.unison, self.unison)
        self.assertNotEquals(self.second, self.unison)
        self.assertEquals(self.second, self.second)

    def test_add(self):
        self.assertEquals(self.second + self.third, self.fourth)

    def test_neg(self):
        self.assertEquals(-self.second, self.second_descending)

    def test_sub(self):
        self.assertEquals(self.fourth - self.third, self.second)

    def test_lt(self):
        self.assertLess(self.second, self.third)
        self.assertLessEqual(self.second, self.third)
        self.assertLessEqual(self.second, self.second)

    def test_repr(self):
        self.assertEquals(repr(self.second), "DiatonicInterval(value=1)")

    def test_get_octave(self):
        self.assertEquals(self.unison.get_octave(), 0)
        self.assertEquals(self.seventh.get_octave(), 0)
        self.assertEquals(self.seventh_descending.get_octave(), -1)
        self.assertEquals(self.octave_descending.get_octave(), -1)
        self.assertEquals(self.second_twice_descending.get_octave(), -2)
        self.assertEquals(self.octave.get_octave(), 1)

    def test_lily_octave(self):
        self.assertEquals(self.unison.lily_octave(), "'")
        self.assertEquals(self.seventh.lily_octave(), "'")
        self.assertEquals(self.seventh_descending.lily_octave(), "")
        self.assertEquals(self.octave_descending.lily_octave(), "")
        self.assertEquals(self.second_twice_descending.lily_octave(), ",")
        self.assertEquals(self.octave.lily_octave(), "''")

    def test_add_octave(self):
        self.assertEquals(self.octave.add_octave(-1), self.unison)
        self.assertEquals(self.unison.add_octave(1), self.octave)
        self.assertEquals(self.octave.add_octave(-2), self.octave_descending)
        self.assertEquals(self.octave_descending.add_octave(2), self.octave)

    def test_same_interval_in_base_octave(self):
        self.assertEquals(self.octave.get_in_base_octave(), self.unison)
        self.assertEquals(self.octave_descending.get_in_base_octave(), self.unison)
        self.assertEquals(self.unison.get_in_base_octave(), self.unison)
        self.assertEquals(self.second.get_in_base_octave(), self.second)
        self.assertEquals(self.second_descending.get_in_base_octave(), self.seventh)

    def test_same_interval_in_different_octaves(self):
        self.assertFalse(self.second.equals_modulo_octave(self.unison))
        self.assertFalse(self.second.equals_modulo_octave(self.octave))
        self.assertFalse(self.second.equals_modulo_octave(self.octave_descending))
        self.assertFalse(self.second.equals_modulo_octave(self.second_descending))
        self.assertTrue(self.unison.equals_modulo_octave(self.unison))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave_descending))
        self.assertTrue(self.octave.equals_modulo_octave(self.octave_descending))

    def test_get_chromatic(self):
        from solfege.interval.chromatic import ChromaticInterval
        self.assertEquals(DiatonicInterval(0).get_chromatic(), ChromaticInterval(0))
        self.assertEquals(DiatonicInterval(1).get_chromatic(), ChromaticInterval(2))
        self.assertEquals(DiatonicInterval(2).get_chromatic(), ChromaticInterval(4))
        self.assertEquals(DiatonicInterval(3).get_chromatic(), ChromaticInterval(5))
        self.assertEquals(DiatonicInterval(4).get_chromatic(), ChromaticInterval(7))
        self.assertEquals(DiatonicInterval(5).get_chromatic(), ChromaticInterval(9))
        self.assertEquals(DiatonicInterval(6).get_chromatic(), ChromaticInterval(11))
        self.assertEquals(DiatonicInterval(7).get_chromatic(), ChromaticInterval(12))
        self.assertEquals(DiatonicInterval(8).get_chromatic(), ChromaticInterval(14))
        self.assertEquals(DiatonicInterval(9).get_chromatic(), ChromaticInterval(16))
        self.assertEquals(DiatonicInterval(-1).get_chromatic(), ChromaticInterval(-1))
        self.assertEquals(DiatonicInterval(-2).get_chromatic(), ChromaticInterval(-3))
        self.assertEquals(DiatonicInterval(-3).get_chromatic(), ChromaticInterval(-5))
        self.assertEquals(DiatonicInterval(-4).get_chromatic(), ChromaticInterval(-7))
        self.assertEquals(DiatonicInterval(-5).get_chromatic(), ChromaticInterval(-8))
        self.assertEquals(DiatonicInterval(-6).get_chromatic(), ChromaticInterval(-10))
        self.assertEquals(DiatonicInterval(-7).get_chromatic(), ChromaticInterval(-12))
        self.assertEquals(DiatonicInterval(-8).get_chromatic(), ChromaticInterval(-13))
        self.assertEquals(DiatonicInterval(-9).get_chromatic(), ChromaticInterval(-15))

    def test_get_name_no_octave(self):
        self.assertEquals(DiatonicInterval(0).get_interval_name(showOctave=False), "unison")
        self.assertEquals(DiatonicInterval(1).get_interval_name(showOctave=False), "second")
        self.assertEquals(DiatonicInterval(2).get_interval_name(showOctave=False), "third")
        self.assertEquals(DiatonicInterval(3).get_interval_name(showOctave=False), "fourth")
        self.assertEquals(DiatonicInterval(4).get_interval_name(showOctave=False), "fifth")
        self.assertEquals(DiatonicInterval(5).get_interval_name(showOctave=False), "sixth")
        self.assertEquals(DiatonicInterval(6).get_interval_name(showOctave=False), "seventh")
        self.assertEquals(DiatonicInterval(7).get_interval_name(showOctave=False), "unison")
        self.assertEquals(DiatonicInterval(8).get_interval_name(showOctave=False), "second")
        self.assertEquals(DiatonicInterval(9).get_interval_name(showOctave=False), "third")
        self.assertEquals(DiatonicInterval(-1).get_interval_name(showOctave=False), "second decreasing")
        self.assertEquals(DiatonicInterval(-2).get_interval_name(showOctave=False), "third decreasing")
        self.assertEquals(DiatonicInterval(-3).get_interval_name(showOctave=False), "fourth decreasing")
        self.assertEquals(DiatonicInterval(-4).get_interval_name(showOctave=False), "fifth decreasing")
        self.assertEquals(DiatonicInterval(-5).get_interval_name(showOctave=False), "sixth decreasing")
        self.assertEquals(DiatonicInterval(-6).get_interval_name(showOctave=False), "seventh decreasing")
        self.assertEquals(DiatonicInterval(-7).get_interval_name(showOctave=False), "unison decreasing")
        self.assertEquals(DiatonicInterval(-8).get_interval_name(showOctave=False), "second decreasing")
        self.assertEquals(DiatonicInterval(-9).get_interval_name(showOctave=False), "third decreasing")

    def test_get_name_with_octave(self):
        self.assertEquals(DiatonicInterval(0).get_interval_name(showOctave=True), "unison")
        self.assertEquals(DiatonicInterval(1).get_interval_name(showOctave=True), "second")
        self.assertEquals(DiatonicInterval(2).get_interval_name(showOctave=True), "third")
        self.assertEquals(DiatonicInterval(3).get_interval_name(showOctave=True), "fourth")
        self.assertEquals(DiatonicInterval(4).get_interval_name(showOctave=True), "fifth")
        self.assertEquals(DiatonicInterval(5).get_interval_name(showOctave=True), "sixth")
        self.assertEquals(DiatonicInterval(6).get_interval_name(showOctave=True), "seventh")
        self.assertEquals(DiatonicInterval(7).get_interval_name(showOctave=True), "octave")
        self.assertEquals(DiatonicInterval(8).get_interval_name(showOctave=True), "octave and second")
        self.assertEquals(DiatonicInterval(9).get_interval_name(showOctave=True), "octave and third")
        self.assertEquals(DiatonicInterval(10).get_interval_name(showOctave=True), "octave and fourth")
        self.assertEquals(DiatonicInterval(11).get_interval_name(showOctave=True), "octave and fifth")
        self.assertEquals(DiatonicInterval(12).get_interval_name(showOctave=True), "octave and sixth")
        self.assertEquals(DiatonicInterval(13).get_interval_name(showOctave=True), "octave and seventh")
        self.assertEquals(DiatonicInterval(14).get_interval_name(showOctave=True), "2 octaves")
        self.assertEquals(DiatonicInterval(15).get_interval_name(showOctave=True), "2 octaves and second")
        self.assertEquals(DiatonicInterval(16).get_interval_name(showOctave=True), "2 octaves and third")
        self.assertEquals(DiatonicInterval(-1).get_interval_name(showOctave=True), "second decreasing")
        self.assertEquals(DiatonicInterval(-2).get_interval_name(showOctave=True), "third decreasing")
        self.assertEquals(DiatonicInterval(-3).get_interval_name(showOctave=True), "fourth decreasing")
        self.assertEquals(DiatonicInterval(-4).get_interval_name(showOctave=True), "fifth decreasing")
        self.assertEquals(DiatonicInterval(-5).get_interval_name(showOctave=True), "sixth decreasing")
        self.assertEquals(DiatonicInterval(-6).get_interval_name(showOctave=True), "seventh decreasing")
        self.assertEquals(DiatonicInterval(-7).get_interval_name(showOctave=True), "octave decreasing")
        self.assertEquals(DiatonicInterval(-8).get_interval_name(showOctave=True), "octave and second decreasing")
        self.assertEquals(DiatonicInterval(-9).get_interval_name(showOctave=True), "octave and third decreasing")
        self.assertEquals(DiatonicInterval(-10).get_interval_name(showOctave=True), "octave and fourth decreasing")
        self.assertEquals(DiatonicInterval(-11).get_interval_name(showOctave=True), "octave and fifth decreasing")
        self.assertEquals(DiatonicInterval(-12).get_interval_name(showOctave=True), "octave and sixth decreasing")
        self.assertEquals(DiatonicInterval(-13).get_interval_name(showOctave=True), "octave and seventh decreasing")
        self.assertEquals(DiatonicInterval(-14).get_interval_name(showOctave=True), "2 octaves decreasing")
        self.assertEquals(DiatonicInterval(-15).get_interval_name(showOctave=True), "2 octaves and second decreasing")
        self.assertEquals(DiatonicInterval(-16).get_interval_name(showOctave=True), "2 octaves and third decreasing")

    def test_mul(self):
        self.assertEquals(self.unison * 4, self.unison)
        self.assertEquals(self.second * 2, self.third)
        self.assertEquals(2 * self.second, self.third)
        self.assertEquals(4 * self.unison, self.unison)

    def test_one_octave(self):
        self.assertEquals(DiatonicInterval.get_one_octave(), DiatonicInterval(value=7))