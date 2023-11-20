import unittest

from solfege.interval.intervalmode import IntervalMode

LILY = "LILY"
FILE_NAME = "FILE_NAME"
TEXT = "TEXT"
MONOSPACE = "MONOSPACE"


class Alteration(IntervalMode):
    def lily(self):
        """Text to obtain this alteration in Lilypond"""
        return ["eses", "es", "", "is", "isis"][self.get_number() + 2]

    def get_note_name(self, usage: str):
        """The name of this note.

        Args: `for_file` -- whether we should avoid non ascii symbol"""
        if usage == MONOSPACE:
            return ["♭♭", "♭ ", "  ", "# ", "𝄪 "][self.get_number() + 2]
        if usage == TEXT:
            return ["♭♭", "♭", "", "#", "𝄪"][self.get_number() + 2]
        if usage == FILE_NAME:
            return [
                "double_flat",
                "flat_",
                "_____",
                "sharp",
                "double_sharp",
            ][self.get_number() + 2]
        assert usage == LILY
        return self.lily()

    @staticmethod
    def from_name(name: str):
        return {
            "#": Alteration(1),
            "##": Alteration(2),
            "": Alteration(0),
            "♭": Alteration(-1),
            "♭♭": Alteration(-2),
        }[name]


class TestAlterationNote(unittest.TestCase):
    def test_from_name(self):
        self.assertEquals(Alteration.from_name("#"), Alteration(1))
        with self.assertRaises(Exception):
            self.assertEquals(Alteration.from_name("###"), Alteration(1))
