from solfege.interval.alteration import TooBigAlteration
from solfege.note.base import _Note
from solfege.interval.chromatic import ChromaticInterval, TestChromaticInterval
from util import MyException


class ChromaticNote(_Note, ChromaticInterval):
    IntervalClass = ChromaticInterval
    # The role this note is most likely to play in the standard chords
    # Especially used for guitar cards
    role = ["unison", None, None, "third", "third", "third", "fifth", "fifth", "fifth", "interval", "interval",
            "interval"]

    def get_color(self, color=True):
        """Color to print the note in lilypond"""
        return "black"

    def get_note_name(self, withOctave=False):
        noteName = ["C", "C#", "D", "E♭", "E", "F", "F#", "G", "A♭", "A", "B♭", "B"][self.get_number() % 12]
        octave = str(self.get_octave(scientificNotation=True)) if withOctave else ""
        return noteName + octave

    def get_note(self, clazz=None):
        """A solfège note. Diatonic note is guessed. The default class is
        Note. May return None if no diatonic note can be guessed. """
        diatonic = self.get_diatonic()
        if diatonic is None:
            return None
        if clazz is None:
            from solfege.note.note import Note
            clazz = Note
        diatonic = diatonic.get_number()
        chromatic = self.get_number()
        return clazz(diatonic=diatonic, chromatic=chromatic)

    def lily(self, color=True):
        """Lilypond representation of this note. Colored according to
        getColor, unless color is set to False.
        """
        if ("lily", color) not in self.dic:
            diatonic = self.get_diatonic()
            try:
                alteration = self.get_alteration()
            except TooBigAlteration as tba:
                tba.addInformation("Note", self)
                tba.addInformation("Base note", self.base.get_note())
                tba.addInformation("Base pos", self.base)
                tba.addInformation("interval", self.get_interval())
                tba.addInformation("Role", self.role)
                raise
            lily = f"{diatonic.get_interval_name()}{alteration.lily()}{self.get_diatonic().lily_octave()}"
            if color:
                color = self.get_color()
                if color is None:
                    exception = MyException()
                    exception.addInformation("Note", self)
                    exception.addInformation("Base pos", self.base)
                    if self.base:
                        exception.addInformation("Base note", self.base.get_note())
                    else:
                        exception.addInformation("Base note", "no base")
                    exception.addInformation("interval", self.get_interval())
                    exception.addInformation("Role", self.role)
                    raise exception
                lily = """\\tweak NoteHead.color  #(x11-color '%s)\n%s\n""" % (color, lily)
            self.dic[("lily", color)] = lily
        return self.dic[("lily", color)]


class TestChromaticNote(TestChromaticInterval):
    C4 = ChromaticNote(0)
    D4 = ChromaticNote(2)
    B3 = ChromaticNote(-1)
    E4 = ChromaticNote(4)
    F4 = ChromaticNote(5)
    C5 = ChromaticNote(12)
    B4 = ChromaticNote(11)
    D3 = ChromaticNote(-10)
    C3 = ChromaticNote(-12)
    B2 = ChromaticNote(-13)

    def test_is_note(self):
        self.assertTrue(self.C4.is_note())

    def test_has_number(self):
        self.assertTrue(self.C4.has_number())

    def test_get_number(self):
        self.assertEquals(self.C4.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.C4, self.C4)
        self.assertNotEquals(self.D4, self.C4)
        self.assertEquals(self.D4, self.D4)

    def test_add(self):
        self.assertEquals(self.D4 + self.third_minor, self.F4)
        self.assertEquals(self.third_minor + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.third_minor, self.D4)
        self.assertEquals(self.F4 - self.D4, self.third_minor)
        with self.assertRaises(Exception):
            _ = self.third_minor - self.D4

    def test_lt(self):
        self.assertLess(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEquals(repr(self.D4), "ChromaticNote(2)")

    def test_get_octave(self):
        self.assertEquals(self.C4.get_octave(), 0)
        self.assertEquals(self.B4.get_octave(), 0)
        self.assertEquals(self.D3.get_octave(), -1)
        self.assertEquals(self.C3.get_octave(), -1)
        self.assertEquals(self.B2.get_octave(), -2)
        self.assertEquals(self.C5.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(self.C5.add_octave(-1), self.C4)
        self.assertEquals(self.C4.add_octave(1), self.C5)
        self.assertEquals(self.C5.add_octave(-2), self.C3)
        self.assertEquals(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        self.assertEquals(self.C5.get_same_note_in_base_octave(), self.C4)
        self.assertEquals(self.C3.get_same_note_in_base_octave(), self.C4)
        self.assertEquals(self.C4.get_same_note_in_base_octave(), self.C4)
        self.assertEquals(self.D4.get_same_note_in_base_octave(), self.D4)
        self.assertEquals(self.B3.get_same_note_in_base_octave(), self.B4)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.C4))
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.C5))
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.C3))
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.B3))
        self.assertTrue(self.C4.same_notes_in_different_octaves(self.C4))
        self.assertTrue(self.C4.same_notes_in_different_octaves(self.C5))
        self.assertTrue(self.C4.same_notes_in_different_octaves(self.C3))
        self.assertTrue(self.C5.same_notes_in_different_octaves(self.C3))

    def test_get_interval_name(self):
        self.assertEquals(ChromaticNote(0).get_note_name(), "C")
        self.assertEquals(ChromaticNote(1).get_note_name(), "C#")
        self.assertEquals(ChromaticNote(2).get_note_name(), "D")
        self.assertEquals(ChromaticNote(3).get_note_name(), "E♭")
        self.assertEquals(ChromaticNote(4).get_note_name(), "E")
        self.assertEquals(ChromaticNote(5).get_note_name(), "F")
        self.assertEquals(ChromaticNote(6).get_note_name(), "F#")
        self.assertEquals(ChromaticNote(7).get_note_name(), "G")
        self.assertEquals(ChromaticNote(8).get_note_name(), "A♭")
        self.assertEquals(ChromaticNote(9).get_note_name(), "A")
        self.assertEquals(ChromaticNote(10).get_note_name(), "B♭")
        self.assertEquals(ChromaticNote(11).get_note_name(), "B")
        self.assertEquals(ChromaticNote(12).get_note_name(), "C")
        self.assertEquals(ChromaticNote(13).get_note_name(), "C#")
        self.assertEquals(ChromaticNote(14).get_note_name(), "D")
        self.assertEquals(ChromaticNote(-1).get_note_name(), "B")
        self.assertEquals(ChromaticNote(-2).get_note_name(), "B♭")
        self.assertEquals(ChromaticNote(-3).get_note_name(), "A")
        self.assertEquals(ChromaticNote(-4).get_note_name(), "A♭")
        self.assertEquals(ChromaticNote(-5).get_note_name(), "G")
        self.assertEquals(ChromaticNote(-6).get_note_name(), "F#")
        self.assertEquals(ChromaticNote(-7).get_note_name(), "F")
        self.assertEquals(ChromaticNote(-8).get_note_name(), "E")
        self.assertEquals(ChromaticNote(-9).get_note_name(), "E♭")
        self.assertEquals(ChromaticNote(-10).get_note_name(), "D")
        self.assertEquals(ChromaticNote(-11).get_note_name(), "C#")
        self.assertEquals(ChromaticNote(-12).get_note_name(), "C")
        self.assertEquals(ChromaticNote(-13).get_note_name(), "B")
        self.assertEquals(ChromaticNote(-14).get_note_name(), "B♭")

    def test_get_name_with_octave(self):
        self.assertEquals(ChromaticNote(0).get_note_name(withOctave=True), "C4")
        self.assertEquals(ChromaticNote(1).get_note_name(withOctave=True), "C#4")
        self.assertEquals(ChromaticNote(2).get_note_name(withOctave=True), "D4")
        self.assertEquals(ChromaticNote(3).get_note_name(withOctave=True), "E♭4")
        self.assertEquals(ChromaticNote(4).get_note_name(withOctave=True), "E4")
        self.assertEquals(ChromaticNote(5).get_note_name(withOctave=True), "F4")
        self.assertEquals(ChromaticNote(6).get_note_name(withOctave=True), "F#4")
        self.assertEquals(ChromaticNote(7).get_note_name(withOctave=True), "G4")
        self.assertEquals(ChromaticNote(8).get_note_name(withOctave=True), "A♭4")
        self.assertEquals(ChromaticNote(9).get_note_name(withOctave=True), "A4")
        self.assertEquals(ChromaticNote(10).get_note_name(withOctave=True), "B♭4")
        self.assertEquals(ChromaticNote(11).get_note_name(withOctave=True), "B4")
        self.assertEquals(ChromaticNote(12).get_note_name(withOctave=True), "C5")
        self.assertEquals(ChromaticNote(13).get_note_name(withOctave=True), "C#5")
        self.assertEquals(ChromaticNote(14).get_note_name(withOctave=True), "D5")
        self.assertEquals(ChromaticNote(-1).get_note_name(withOctave=True), "B3")
        self.assertEquals(ChromaticNote(-2).get_note_name(withOctave=True), "B♭3")
        self.assertEquals(ChromaticNote(-3).get_note_name(withOctave=True), "A3")
        self.assertEquals(ChromaticNote(-4).get_note_name(withOctave=True), "A♭3")
        self.assertEquals(ChromaticNote(-5).get_note_name(withOctave=True), "G3")
        self.assertEquals(ChromaticNote(-6).get_note_name(withOctave=True), "F#3")
        self.assertEquals(ChromaticNote(-7).get_note_name(withOctave=True), "F3")
        self.assertEquals(ChromaticNote(-8).get_note_name(withOctave=True), "E3")
        self.assertEquals(ChromaticNote(-9).get_note_name(withOctave=True), "E♭3")
        self.assertEquals(ChromaticNote(-10).get_note_name(withOctave=True), "D3")
        self.assertEquals(ChromaticNote(-11).get_note_name(withOctave=True), "C#3")
        self.assertEquals(ChromaticNote(-12).get_note_name(withOctave=True), "C3")
        self.assertEquals(ChromaticNote(-13).get_note_name(withOctave=True), "B2")
        self.assertEquals(ChromaticNote(-14).get_note_name(withOctave=True), "B♭2")

    def test_get_solfege(self):
        from solfege.note.note import Note
        self.assertEquals(ChromaticNote(0).get_solfege(), Note(0, 0))
        self.assertEquals(ChromaticNote(1).get_solfege(), Note(1, 0))
        self.assertEquals(ChromaticNote(2).get_solfege(), Note(2, 1))
        self.assertEquals(ChromaticNote(3).get_solfege(), Note(3, 2))
        self.assertEquals(ChromaticNote(4).get_solfege(), Note(4, 2))
        self.assertEquals(ChromaticNote(5).get_solfege(), Note(5, 3))
        self.assertEquals(ChromaticNote(6).get_solfege(), Note(6, 3))
        self.assertEquals(ChromaticNote(7).get_solfege(), Note(7, 4))
        self.assertEquals(ChromaticNote(8).get_solfege(), Note(8, 5))
        self.assertEquals(ChromaticNote(9).get_solfege(), Note(9, 5))
        self.assertEquals(ChromaticNote(10).get_solfege(), Note(10, 6))
        self.assertEquals(ChromaticNote(11).get_solfege(), Note(11, 6))
        self.assertEquals(ChromaticNote(12).get_solfege(), Note(12, 7))
        self.assertEquals(ChromaticNote(13).get_solfege(), Note(13, 7))
        self.assertEquals(ChromaticNote(14).get_solfege(), Note(14, 8))
        self.assertEquals(ChromaticNote(-1).get_solfege(), Note(-1, -1))
        self.assertEquals(ChromaticNote(-2).get_solfege(), Note(-2, -1))
        self.assertEquals(ChromaticNote(-3).get_solfege(), Note(-3, -2))
        self.assertEquals(ChromaticNote(-4).get_solfege(), Note(-4, -2))
        self.assertEquals(ChromaticNote(-5).get_solfege(), Note(-5, -3))
        self.assertEquals(ChromaticNote(-6).get_solfege(), Note(-6, -4))
        self.assertEquals(ChromaticNote(-7).get_solfege(), Note(-7, -4))
        self.assertEquals(ChromaticNote(-8).get_solfege(), Note(-8, -5))
        self.assertEquals(ChromaticNote(-9).get_solfege(), Note(-9, -5))
        self.assertEquals(ChromaticNote(-10).get_solfege(), Note(-10, -6))
        self.assertEquals(ChromaticNote(-11).get_solfege(), Note(-11, -7))
        self.assertEquals(ChromaticNote(-12).get_solfege(), Note(-12, -7))
        self.assertEquals(ChromaticNote(-13).get_solfege(), Note(-13, -8))
        self.assertEquals(ChromaticNote(-14).get_solfege(), Note(-14, -8))
