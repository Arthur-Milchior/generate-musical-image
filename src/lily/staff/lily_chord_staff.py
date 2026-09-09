from dataclasses import dataclass
from typing import Dict, List
from lily.staff.lily_staff import LilyStaff
from solfege.value.key.key import Key
from solfege.value.note.note import NoteFrozenList
from utils.util import indent


@dataclass(frozen=True)
class LilyChordStaff(LilyStaff):
    """A staff rendering a single chord: all `notes` stacked as one simultaneous LilyPond chord (`<...>`), with an
    optional `\\ottava` marking if the chord falls outside the staff's normal range."""
    notes: NoteFrozenList
    """The notes making up the chord, rendered stacked together."""

    def staff_content(self) -> str:
            """The LilyPond chord construct `<note note ...>`, prefixed with an `\\ottava` directive if
            `get_ottava()` is non-zero."""
            return f"""{self._get_ottava_str()}<
{indent(" ".join(note.syntax_for_lily() for note in self.notes))}
>"""

    def _get_ottava_str(self):
         """The `\\ottava N` LilyPond directive line for the current octave shift, or `""` if no shift is needed."""
         ot = self.get_ottava()
         if ot is 0:
              return ""
         return f"\ottava {ot}\n"

    def get_ottava(self):
         """The net `\\ottava` shift to apply: `get_8_va()` if positive (notes above the staff), the negation of
         `get_8_vb()` if that is positive (notes below the staff), else 0. At most one of the two is expected to be
         non-zero."""
         va = self.get_8_va()
         vb = self.get_8_vb()
         if va != 0:
              assert vb is 0
              return va
         if vb != 0:
              return -vb
         return 0

    def get_8_va(self):
         """Return the number of octave in 8va"""
         return 0

    def get_8_vb(self):
         """Return the number of octave in 8vb"""
         return 0

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """No extra defaults beyond the parent's; forwards to `LilyStaff`."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Coerce a plain iterable passed as `notes` into a `NoteFrozenList`."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notes", NoteFrozenList)
        return args, kwargs

    def __post_init__(self):
        """Delegate validation to `LilyStaff.__post_init__`."""
        super().__post_init__()