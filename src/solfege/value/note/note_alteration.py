from dataclasses import dataclass
from typing import ClassVar, assert_never
from solfege.value.interval.alteration.alteration import Alteration
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput
from solfege.value.note.chromatic_note import ChromaticNote
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
asciis = [s.replace(" ", "") for s in fixed_length_ascii_space_double]
symbols = [s.replace(" ", "") for s in fixed_length_symbol_space_double]


@dataclass(frozen=True)
class NoteAlteration(Alteration):
    """The alteration (sharp/flat count) applied to a note, e.g. the +1 in G#. Values range from
    -2 (double flat) to +2 (double sharp)."""

    def syntax_for_lily(self):
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
        """Parse a symbol ("#", "##", "", "♭", "♭♭", "𝄪") into the matching `NoteAlteration`
        singleton."""
        return {
            "#": SHARP,
            "##": DOUBLE_SHARP,
            "": NATURAL,
            "♭": FLAT,
            "♭♭": DOUBLE_FLAT,
            "𝄪": DOUBLE_SHARP,
        }[name]
    
    #pragma mark - Alteration

    min_value: ClassVar[int] = -2
    """A note alteration may go as low as double flat."""
    max_value: ClassVar[int] = 2
    """A note alteration may go as high as double sharp."""


alteration_symbols = "𝄪♭#"

DOUBLE_FLAT = NoteAlteration.make(-2)
FLAT = NoteAlteration.make(-1)
NATURAL = NoteAlteration.make(0)
SHARP = NoteAlteration.make(1)
DOUBLE_SHARP = NoteAlteration.make(2)


ChromaticNote.AlterationClass = NoteAlteration
