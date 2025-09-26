
from abc import abstractmethod
from dataclasses import dataclass

from solfege.value.key.key import Key
from solfege.value.note.clef import Clef
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing, indent


@dataclass(frozen=True)
class LilyStaff(DataClassWithDefaultArgument):
    clef: Clef
    first_key: Key

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
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs
    
    def __post_init__(self):
        assert_typing(self.clef, Clef)
        assert_typing(self.first_key, Key)
        return super().__post_init__()


    # Must be implemented by subclass

    @abstractmethod
    def staff_content(self) -> str:...


@dataclass(frozen=True)
class FakeLilyStaff(LilyStaff):
    content: str

    #pragma mark - LilyStaff
    def staff_content(self):
        return self.content