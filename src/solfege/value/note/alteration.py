from dataclasses import dataclass
from typing import assert_never
from solfege.value.interval.interval_mode import IntervalMode
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote

LILY = "LILY"
FILE_NAME = "FILE_NAME"
FULL_NAME = "TEXT"
DEBUG = "DEBUG"
NAME_UP_TO_OCTAVE = "ANKI"


@dataclass(frozen=True)
class Alteration(IntervalMode):
    def lily_in_scale(self):
        """Text to obtain this alteration in Lilypond"""
        return ["eses", "es", "", "is", "isis"][self.value + 2]

    def get_name(self, alteration_output: AlterationOutput, fixed_length: FixedLengthOutput = FixedLengthOutput.NO):
        """return fixed length except for double alteration"""
        if alteration_output == AlterationOutput.LILY:
            assert fixed_length == FixedLengthOutput.NO
            return ["eses", "es", "", "is", "isis"][self.value + 2]
        elif alteration_output == AlterationOutput.ASCII:
            if fixed_length == FixedLengthOutput.UNDERSCORE_DOUBLE:
                return [
                    "double_flat_",
                    "flat________",
                    "____________",
                    "sharp_______",
                    "double_sharp",
                ][self.value + 2]
            elif fixed_length == FixedLengthOutput.UNDERSCORE_SIMPLE:
                return [
                    "double_flat",
                    "flat_",
                    "_____",
                    "sharp",
                    "double_sharp",
                ][self.value + 2]
            elif fixed_length == FixedLengthOutput.SPACE_DOUBLE:
                return [
                    "double flat ",
                    "flat        ",
                    "            ",
                    "sharp       ",
                    "double_sharp",
                ][self.value + 2]
            elif fixed_length == FixedLengthOutput.SPACE_SIMPLE:
                return [
                    "double flat",
                    "flat ",
                    "     ",
                    "sharp",
                    "double_sharp",
                ][self.value + 2]
            elif fixed_length == FixedLengthOutput.NO:
                return [
                    "double_flat",
                    "flat",
                    "",
                    "sharp",
                    "double_sharp",
                ][self.value + 2]
            assert_never(fixed_length)
        elif alteration_output == AlterationOutput.SYMBOL:
            if fixed_length == FixedLengthOutput.SPACE_DOUBLE:
                return ["♭♭", "♭ ", "  ", "# ", "𝄪 "][self.value + 2]
            elif fixed_length == FixedLengthOutput.SPACE_SIMPLE:
                return ["♭♭", "♭", " ", "#", "𝄪"][self.value + 2]
            if fixed_length == FixedLengthOutput.UNDERSCORE_DOUBLE:
                return ["♭♭", "♭_", "__", "#_", "𝄪_"][self.value + 2]
            elif fixed_length == FixedLengthOutput.UNDERSCORE_SIMPLE:
                return ["♭♭", "♭", "_", "#", "𝄪"][self.value + 2]
            elif fixed_length == FixedLengthOutput.NO:
                return ["♭♭", "♭", "", "#", "𝄪"][self.value + 2]
            assert_never(fixed_length)

    @staticmethod
    def from_name(name: str):
        return {
            "#": SHARP,
            "##": DOUBLE_SHARP,
            "": NATURAL,
            "♭": FLAT,
            "♭♭": DOUBLE_FLAT,
            "𝄪": DOUBLE_SHARP,
        }[name]


alteration_symbols = "𝄪♭#"

DOUBLE_FLAT = Alteration(-2)
FLAT = Alteration(-1)
NATURAL = Alteration(0)
SHARP = Alteration(1)
DOUBLE_SHARP = Alteration(2)


ChromaticNote.AlterationClass = Alteration
