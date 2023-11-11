import unittest

from solfege.interval.base import _Interval


class DiatonicInterval(_Interval):
    """An interval, where we count the number of notes in the major scale,
    and ignore the notes which are absent. B and B# can't be
    distinguished, since A# does not really exist. However, this would
    allow to distinguish between B# and C"""
    modulo = 7
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
    seconde = DiatonicInterval(1)
    seconde_descendante = DiatonicInterval(-1)
    tierce = DiatonicInterval(2)
    quarte = DiatonicInterval(3)
    octave = DiatonicInterval(7)
    septieme = DiatonicInterval(6)
    septieme_descendante = DiatonicInterval(-6)
    octave_descendante = DiatonicInterval(-7)
    seconde_descendante_descendante = DiatonicInterval(-8)

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())

    def test_has_number(self):
        self.assertTrue(self.unison.has_number())

    def test_get_number(self):
        self.assertEquals(self.unison.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.unison, self.unison)
        self.assertNotEquals(self.seconde, self.unison)
        self.assertEquals(self.seconde, self.seconde)

    def test_add(self):
        self.assertEquals(self.seconde + self.tierce, self.quarte)

    def test_neg(self):
        self.assertEquals(-self.seconde, self.seconde_descendante)

    def test_sub(self):
        self.assertEquals(self.quarte - self.tierce, self.seconde)

    def test_lt(self):
        self.assertLess(self.seconde, self.tierce)
        self.assertLessEqual(self.seconde, self.tierce)
        self.assertLessEqual(self.seconde, self.seconde)

    def test_repr(self):
        self.assertEquals(repr(self.seconde), "DiatonicInterval(1)")

    def test_get_octave(self):
        self.assertEquals(self.unison.get_octave(), 0)
        self.assertEquals(self.septieme.get_octave(), 0)
        self.assertEquals(self.septieme_descendante.get_octave(), -1)
        self.assertEquals(self.octave_descendante.get_octave(), -1)
        self.assertEquals(self.seconde_descendante_descendante.get_octave(), -2)
        self.assertEquals(self.octave.get_octave(), 1)

    def test_lily_octave(self):
        self.assertEquals(self.unison.lily_octave(), "'")
        self.assertEquals(self.septieme.lily_octave(), "'")
        self.assertEquals(self.septieme_descendante.lily_octave(), "")
        self.assertEquals(self.octave_descendante.lily_octave(), "")
        self.assertEquals(self.seconde_descendante_descendante.lily_octave(), ",")
        self.assertEquals(self.octave.lily_octave(), "''")

    def test_add_octave(self):
        self.assertEquals(self.octave.add_octave(-1), self.unison)
        self.assertEquals(self.unison.add_octave(1), self.octave)
        self.assertEquals(self.octave.add_octave(-2), self.octave_descendante)
        self.assertEquals(self.octave_descendante.add_octave(2), self.octave)

    def test_same_note_in_base_octave(self):
        self.assertEquals(self.octave.get_same_note_in_base_octave(), self.unison)
        self.assertEquals(self.octave_descendante.get_same_note_in_base_octave(), self.unison)
        self.assertEquals(self.unison.get_same_note_in_base_octave(), self.unison)
        self.assertEquals(self.seconde.get_same_note_in_base_octave(), self.seconde)
        self.assertEquals(self.seconde_descendante.get_same_note_in_base_octave(), self.septieme)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.seconde.same_notes_in_different_octaves(self.unison))
        self.assertFalse(self.seconde.same_notes_in_different_octaves(self.octave))
        self.assertFalse(self.seconde.same_notes_in_different_octaves(self.octave_descendante))
        self.assertFalse(self.seconde.same_notes_in_different_octaves(self.seconde_descendante))
        self.assertTrue(self.unison.same_notes_in_different_octaves(self.unison))
        self.assertTrue(self.unison.same_notes_in_different_octaves(self.octave))
        self.assertTrue(self.unison.same_notes_in_different_octaves(self.octave_descendante))
        self.assertTrue(self.octave.same_notes_in_different_octaves(self.octave_descendante))

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
