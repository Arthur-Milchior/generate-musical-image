from .scale_pattern import *


class TestScalePattern(unittest.TestCase):

    def test_ne(self):
        self.assertNotEquals(minor_melodic,
                             ScalePattern[Interval](["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], four_flats))
        self.assertNotEquals(minor_melodic, ScalePattern[Interval](["Minor melodic"], [2, 1, 2, 2, 2, 2],
                                                                   three_flats, suppress_warning=False))
        self.assertNotEquals(minor_melodic, ScalePattern[Interval](["Minor"], [2, 1, 2, 2, 2, 2, 1],
                                                                   three_flats))

    def test_eq(self):
        self.assertEquals(minor_melodic.interval_for_signature, three_flats)
        self.assertEquals(minor_melodic._diatonic_sum, 7)
        self.assertEquals(minor_melodic._chromatic_sum, 12)
        self.assertEquals(minor_melodic._intervals, [
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=1, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=1, diatonic=1),
        ])

    def test_get_notes(self):
        tonic = Note(diatonic=0, chromatic=0)
        self.assertEquals(minor_melodic.get_notes(tonic),
                          [
                              Note(diatonic=0, chromatic=0),
                              Note(diatonic=1, chromatic=2),
                              Note(diatonic=2, chromatic=3),
                              Note(diatonic=3, chromatic=5),
                              Note(diatonic=4, chromatic=7),
                              Note(diatonic=5, chromatic=9),
                              Note(diatonic=6, chromatic=11),
                              Note(diatonic=7, chromatic=12),
                          ])

    def test_neg(self):
        reversed = -minor_melodic
        expected = ScalePattern[Interval](["Minor melodic"],
                                          [
                                              Interval(diatonic=-1, chromatic=- 1),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-1),
                                              Interval(diatonic=-1, chromatic=-2)], three_flats, increasing=False,
                                          record=False)
        self.assertEquals(reversed,
                          expected)

    def test_generate(self):
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=2, diatonic=1),
            Note(chromatic=3, diatonic=2),
            Note(chromatic=5, diatonic=3),
            Note(chromatic=7, diatonic=4),
            Note(chromatic=9, diatonic=5),
            Note(chromatic=11, diatonic=6),
            Note(chromatic=12, diatonic=7),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0))
        self.assertEquals(expected, generated)

    def test_generate_two(self):
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=2, diatonic=1),
            Note(chromatic=3, diatonic=2),
            Note(chromatic=5, diatonic=3),
            Note(chromatic=7, diatonic=4),
            Note(chromatic=9, diatonic=5),
            Note(chromatic=11, diatonic=6),
            Note(chromatic=12, diatonic=7),
            Note(chromatic=14, diatonic=8),
            Note(chromatic=15, diatonic=9),
            Note(chromatic=17, diatonic=10),
            Note(chromatic=19, diatonic=11),
            Note(chromatic=21, diatonic=12),
            Note(chromatic=23, diatonic=13),
            Note(chromatic=24, diatonic=14),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=2)
        self.assertEquals(expected, generated)
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=2, diatonic=1),
            Note(chromatic=3, diatonic=2),
            Note(chromatic=5, diatonic=3),
            Note(chromatic=7, diatonic=4),
            Note(chromatic=9, diatonic=5),
            Note(chromatic=11, diatonic=6),
            Note(chromatic=12, diatonic=7),
            Note(chromatic=14, diatonic=8),
            Note(chromatic=15, diatonic=9),
            Note(chromatic=17, diatonic=10),
            Note(chromatic=19, diatonic=11),
            Note(chromatic=21, diatonic=12),
            Note(chromatic=23, diatonic=13),
            Note(chromatic=24, diatonic=14),
            Note(chromatic=26, diatonic=15),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=2, add_an_extra_note=True)
        self.assertEquals(expected, generated)

    def test_generate_minus_two(self):
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=-1, diatonic=-1),
            Note(chromatic=-3, diatonic=-2),
            Note(chromatic=-5, diatonic=-3),
            Note(chromatic=-7, diatonic=-4),
            Note(chromatic=-9, diatonic=-5),
            Note(chromatic=-10, diatonic=-6),
            Note(chromatic=-12, diatonic=-7),
            Note(chromatic=-13, diatonic=-8),
            Note(chromatic=-15, diatonic=-9),
            Note(chromatic=-17, diatonic=-10),
            Note(chromatic=-19, diatonic=-11),
            Note(chromatic=-21, diatonic=-12),
            Note(chromatic=-22, diatonic=-13),
            Note(chromatic=-24, diatonic=-14),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=-2)
        self.assertEquals(expected, generated)
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=-1, diatonic=-1),
            Note(chromatic=-3, diatonic=-2),
            Note(chromatic=-5, diatonic=-3),
            Note(chromatic=-7, diatonic=-4),
            Note(chromatic=-9, diatonic=-5),
            Note(chromatic=-10, diatonic=-6),
            Note(chromatic=-12, diatonic=-7),
            Note(chromatic=-13, diatonic=-8),
            Note(chromatic=-15, diatonic=-9),
            Note(chromatic=-17, diatonic=-10),
            Note(chromatic=-19, diatonic=-11),
            Note(chromatic=-21, diatonic=-12),
            Note(chromatic=-22, diatonic=-13),
            Note(chromatic=-24, diatonic=-14),
            Note(chromatic=-25, diatonic=-15),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=-2, add_an_extra_note=True)
        self.assertEquals(expected, generated)

    def test_number_of_intervals(self):
        self.assertEquals(minor_melodic.number_of_intervals(), 7)
        self.assertEquals(pentatonic_minor.number_of_intervals(), 5)
