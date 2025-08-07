import unittest

from solfege.interval.intervalmode import IntervalMode

LILY = "LILY"
FILE_NAME = "FILE_NAME"
FULL_NAME = "TEXT"
DEBUG = "DEBUG"
NAME_UP_TO_OCTAVE = "ANKI"


class Alteration(IntervalMode):
    def lily_in_scale(self):
        """Text to obtain this alteration in Lilypond"""
        return ["eses", "es", "", "is", "isis"][self.get_number() + 2]

    def get_symbol_name(self, fixed_length: bool = True):
        """The name of this note of fixed length"""
        if fixed_length:
            return ["♭♭", "♭", "", "#", "𝄪"][self.get_number() + 2]
        return ["♭♭", "♭ ", "  ", "# ", "𝄪 "][self.get_number() + 2]

    def get_ascii_name(self, fixed_length: bool = True):
        """return fixed length except for double alteration"""
        if fixed_length:
            return [
                "double_flat",
                "flat_",
                "_____",
                "sharp",
                "double_sharp",
            ][self.get_number() + 2]
        else:
            return [
                "double_flat",
                "flat",
                "",
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


