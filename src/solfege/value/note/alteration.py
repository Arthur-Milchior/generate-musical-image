from dataclasses import dataclass
import math
from typing import assert_never
from solfege.value.interval.interval_mode import IntervalMode
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote
from utils.easyness import ClassWithEasyness
from utils.util import assert_equal_length

LILY = "LILY"
FILE_NAME = "FILE_NAME"
FULL_NAME = "TEXT"
DEBUG = "DEBUG"
NAME_UP_TO_OCTAVE = "ANKI"

fixed_length_symbol_space_simple =["♭", " ", "#"]
fixed_length_symbol_space_double =["♭♭", "♭ ", "  ", "# ", "𝄪 "]
fixed_length_ascii_space_simple  = [
                    "flat ",
                    "     ",
                    "sharp",]
fixed_length_ascii_space_double  = [
                    "double flat ",
                    "flat        ",
                    "            ",
                    "sharp       ",
                    "double_sharp",
                ]
assert_equal_length(fixed_length_symbol_space_simple)
assert_equal_length(fixed_length_symbol_space_double)
assert_equal_length(fixed_length_ascii_space_simple)
assert_equal_length(fixed_length_ascii_space_double)
fixed_length_ascii_underscore_simple = [s.replace(" ", "_") for s in fixed_length_ascii_space_simple]
fixed_length_ascii_underscore_double = [s.replace(" ", "_") for s in fixed_length_ascii_space_double]
fixed_length_symbol_underscore_simple = [s.replace(" ", "_") for s in fixed_length_symbol_space_simple]
fixed_length_symbol_underscore_double = [s.replace(" ", "_") for s in fixed_length_symbol_space_double]
asciis = [s.replace(" ", "") for s in fixed_length_symbol_space_simple]
symbols = [s.replace(" ", "") for s in fixed_length_symbol_space_double]


@dataclass(frozen=True)
class Alteration(IntervalMode, ClassWithEasyness):
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
                return fixed_length_ascii_underscore_double[self.value + 2]
            elif fixed_length == FixedLengthOutput.UNDERSCORE_SIMPLE:
                return [
                    "double_flat",
                    *fixed_length_ascii_underscore_simple,
                    "double_sharp",
                ][self.value + 2]
            elif fixed_length == FixedLengthOutput.SPACE_DOUBLE:
                return fixed_length_ascii_space_double[self.value + 2]
            elif fixed_length == FixedLengthOutput.SPACE_SIMPLE:
                return [
                    "double flat",
                    *fixed_length_ascii_space_simple,
                    "double_sharp",
                ][self.value + 2]
            elif fixed_length == FixedLengthOutput.NO:
                return asciis[self.value + 2]
            assert_never(fixed_length)
        elif alteration_output == AlterationOutput.SYMBOL:
            if fixed_length == FixedLengthOutput.SPACE_DOUBLE:
                return fixed_length_ascii_space_double[self.value + 2]
            elif fixed_length == FixedLengthOutput.SPACE_SIMPLE:
                return ["♭♭", *fixed_length_symbol_space_simple, "𝄪"][self.value + 2]
            if fixed_length == FixedLengthOutput.UNDERSCORE_DOUBLE:
                return fixed_length_ascii_underscore_double[self.value + 2]
            elif fixed_length == FixedLengthOutput.UNDERSCORE_SIMPLE:
                return ["♭♭", *fixed_length_symbol_underscore_simple, "𝄪"][self.value + 2]
            elif fixed_length == FixedLengthOutput.NO:
                return symbols[self.value + 2]
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

    #pragma mark - ClassWithEasyness

    def easy_key(self):
        return self.value if self.value > 0 else -self.value


alteration_symbols = "𝄪♭#"

DOUBLE_FLAT = Alteration(-2)
FLAT = Alteration(-1)
NATURAL = Alteration(0)
SHARP = Alteration(1)
DOUBLE_SHARP = Alteration(2)


ChromaticNote.AlterationClass = Alteration
