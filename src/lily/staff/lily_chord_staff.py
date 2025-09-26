from dataclasses import dataclass
from typing import Dict, List
from lily.staff.lily_staff import LilyStaff
from solfege.value.key.key import Key
from solfege.value.note.note import NoteFrozenList
from utils.util import indent


@dataclass(frozen=True)
class LilyChordStaff(LilyStaff):
    notes: NoteFrozenList

    def staff_content(self) -> str:
            
            return f"""{self._get_ottava_str()}<
{indent(" ".join(note.syntax_for_lily() for note in self.notes))}
>"""
    
    def _get_ottava_str(self):
         ot = self.get_ottava()
         if ot is 0:
              return ""
         return f"\ottava {ot}\n"
    
    def get_ottava(self):
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
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notes", NoteFrozenList)
        return args, kwargs

    def __post_init__(self):
        super().__post_init__()