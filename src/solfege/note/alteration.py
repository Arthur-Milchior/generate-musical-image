import unittest

from solfege.interval.intervalmode import IntervalMode

LILY = "LILY"
FILE_NAME = "FILE_NAME"
FULL_NAME = "TEXT"
DEBUG = "DEBUG"
NAME_UP_TO_OCTAVE = "ANKI"


class Alteration(IntervalMode):
    def lily(self):
        """Text to obtain this alteration in Lilypond"""
        return ["eses", "es", "", "is", "isis"][self.get_number() + 2]

    def get_symbol_name(self):
        """The name of this note.

        Args: `for_file` -- whether we should avoid non ascii symbol"""
        return ["♭♭", "♭ ", "  ", "# ", "𝄪 "][self.get_number() + 2]

    def get_ascii_name(self):
        return [
            "double_flat",
            "flat_",
            "_____",
            "sharp",
            "double_sharp",
        ][self.get_number() + 2]

    @staticmethod
    def from_name(name: str):
        return {
            "#": Alteration(1),
            "##": Alteration(2),
            "": Alteration(0),
            "♭": Alteration(-1),
            "♭♭": Alteration(-2),
            "𝄪": Alteration(2)
        }[name]


alteration_symbols = "𝄪♭#"


class TestAlterationNote(unittest.TestCase):
    def test_from_name(self):
        self.assertEquals(Alteration.from_name("𝄪"), Alteration(2))
        self.assertEquals(Alteration.from_name("#"), Alteration(1))
        with self.assertRaises(Exception):
            self.assertEquals(Alteration.from_name("###"), Alteration(1))
