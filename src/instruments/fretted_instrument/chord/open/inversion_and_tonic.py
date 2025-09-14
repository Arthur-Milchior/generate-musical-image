from dataclasses import dataclass
from typing import Dict, List

from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.value.note.chromatic_note import ChromaticNote
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing


@dataclass(frozen=True)
class InversionAndTonic(DataClassWithDefaultArgument):
    inversion: InversionPattern
    tonic: ChromaticNote

    def __post_init__(self):
        assert_typing(self.inversion, InversionPattern)
        assert_typing(self.tonic, ChromaticNote)
        assert self.tonic.in_base_octave() == self.tonic
        return super().__post_init__()
    
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "inversion")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "tonic", lambda note: note.in_base_octave())
        return super()._clean_arguments_for_constructor(args, kwargs)
    