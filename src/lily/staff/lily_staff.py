
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, List

from solfege.value.key.key import Key
from solfege.value.note.clef import Clef
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing, indent


@dataclass(frozen=True)
class LilyStaff(DataClassWithDefaultArgument):
    """Base class for the LilyPond code of a single staff (clef + key signature + note content), subclassed for a
    single note, a scale, or a chord."""
    clef: Clef
    """The clef (`Clef.TREBLE`/`Clef.BASS`) this staff is rendered with."""
    first_key: Key
    """The key signature to display on the staff."""

    def staff_lily_code(self) -> str:
        """A lilypond staff.

        The key is the given one.

        The note are decorated with the fingering given in argument.

        Bass for left hand and treble for right

        Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
        """
        return f"""\\new Staff{{
  \\override Staff.TimeSignature.stencil = ##f
  \\omit Staff.BarLine
  \\omit PianoStaff.SpanBar
  \\time 30/4
  \\set Staff.printKeyCancellation = ##f
  \\clef {self.clef}
  \\key {self.first_key.lily_key()} \\major
{indent(self.staff_content())}
}}"""
    

    # # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Dict:
        """No extra defaults beyond the parent's; forwards to `DataClassWithDefaultArgument`."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs

    def __post_init__(self) -> None:
        """Validate that `clef` and `first_key` were given the right types."""
        assert_typing(self.clef, Clef)
        assert_typing(self.first_key, Key)
        return super().__post_init__()


    # Must be implemented by subclass

    @abstractmethod
    def staff_content(self) -> str:
        """The LilyPond code for the notes/content of this staff (without the surrounding `\\new Staff{...}`
        wrapper), to be implemented by each subclass."""
        ...


@dataclass(frozen=True)
class FakeLilyStaff(LilyStaff):
    """Test double for `LilyStaff` whose content is an arbitrary fixed string, useful when exercising
    `staff_lily_code()` without going through a real note/scale/chord staff."""
    content: str
    """The literal LilyPond content string returned by `staff_content()`."""

    #pragma mark - LilyStaff
    def staff_content(self) -> str:
        """Return the fixed `content` string given at construction."""
        return self.content