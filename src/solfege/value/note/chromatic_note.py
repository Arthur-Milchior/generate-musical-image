from dataclasses import dataclass
from typing import ClassVar, Optional, Self, Type, Union
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.note.clef import Clef
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.value.chromatic import Chromatic
from solfege.value.note.singleton_note import AbstractSingletonNote
from solfege.value.singleton import Singleton
from utils.easyness import ClassWithEasyness
from utils.frozenlist import FrozenList
from utils.util import assert_typing, img_tag


@dataclass(frozen=True, repr=False, eq=False)
class ChromaticNote(AbstractSingletonNote[ChromaticInterval], ClassWithEasyness[int], Chromatic):
    """A note represented solely by its chromatic (half-tone) position, with no diatonic
    information (so it cannot distinguish e.g. G# from Ab)."""
    AlterationClass: ClassVar[Type[Chromatic]]
    """The chromatic class used to represent this note's alteration."""
    IntervalClass: ClassVar[Type[Singleton]] = ChromaticInterval
    """The interval class produced when adding/subtracting `ChromaticNote` instances."""
    @staticmethod
    def from_name(name: str) -> "ChromaticNote":
        """Parse a note name (e.g. "C#4") via `Note.from_name` and return its chromatic part."""
        from solfege.value.note.note import Note
        return Note.from_name(name).get_chromatic()

    def get_color(self, color: bool=True) -> str:
        """Color to print the note in lilypond"""
        return "black"

    def get_note(self, cls: Optional[Type["Note"]] = None) -> "Note":
        """A solfège note. Diatonic note is guessed. The default class is
        Note. May return None if no diatonic note can be guessed. """
        from solfege.value.note.note import Note
        diatonic = Note.from_chromatic(self)._diatonic
        if cls is None:
            from solfege.value.note.note import Note
            cls = Note
        diatonic = diatonic
        return cls(_diatonic=diatonic, _chromatic=self)

    def is_white_key_on_piano(self) -> bool:
        """Whether this note corresponds to a black note of the keyboard"""
        return not self.is_black_key_on_piano()

    def is_black_key_on_piano(self) -> bool:
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().value % 12) in blacks
    
    @classmethod
    def _make_single_argument(cls, value: Union[int, str]) -> Self:
        """Build a `ChromaticNote` from either its chromatic int value or a note name string
        (resolved through `Note.from_name`)."""
        if isinstance(value, str):
            from solfege.value.note.note import Note
            return Note.from_name(value).get_chromatic()
        assert_typing(value, int)
        return cls(value)

    #Pragma mark - AbstractNote

    def get_name_up_to_octave(self,
                              alteration_output: AlterationOutput,
                              note_output: NoteOutput,
                              fixed_length: FixedLengthOutput) -> str:
        """Guess a diatonic spelling (via `get_note`) and delegate name formatting to it."""
        return self.get_note().get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

    def non_ambiguous_string_for_file_name(self) -> str:
        """Guess a diatonic spelling (via `Note.from_chromatic`) and delegate to it, since a
        chromatic-only value alone is ambiguous (e.g. G# vs Ab)."""
        from solfege.value.note.note import Note
        note = Note.from_chromatic(self)
        return note.non_ambiguous_string_for_file_name()

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> int:
        """White notes are easier than black ones."""
        return self.get_note().easy_key()

ChromaticNote.ChromaticClass = ChromaticNote

class ChromaticNoteFrozenList(FrozenList[ChromaticNote]):
    """A `FrozenList` specialized to hold `ChromaticNote` elements."""
    type = ChromaticNote

ChromaticIntervalFrozenList.note_frozen_list_type = ChromaticNoteFrozenList