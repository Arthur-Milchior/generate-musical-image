import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from instruments.fretted_instrument.position.positions_consts import DISTANCE_BETWEEN_STRING
from instruments.fretted_instrument.position.fret.fret_delta import FretDelta
from solfege.value.note.chromatic_note import ChromaticNoteFrozenList
from solfege.value.note.clef import Clef
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import IntFrozenList
from utils.util import assert_optional_typing, assert_typing, ensure_folder



@dataclass(frozen=True, unsafe_hash=True)
class AbstractFrettedInstrument(DataClassWithDefaultArgument):
    _name: str
    number_of_frets: int
    clef: Clef
    number_of_strings: int
    """finger_to_fret_delta[i][j] is the possible number of frets between fingers i and j"""
    finger_to_fret_delta: Dict[int, Dict[int, FretDelta]]=field(compare=False)
    number_of_scales_reachable_per_string: IntFrozenList

    # pragma mark - DataClassWithDefaultArgument
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_finger_to_fret_delta(open_strings: Dict[int, Dict[int, FretDelta]]):
            # Ensure modifications are not applied to the dic
            open_strings = copy.deepcopy(open_strings)
            assert_typing(open_strings, dict)
            for lower in range(4):
                for higher in range (lower+1, 5):
                    delta = open_strings[lower][higher]
                    assert_typing(delta, FretDelta)
                    open_strings[higher][lower] = -delta
            return open_strings
        def clean_open_strings(open_strings):
            return ChromaticNoteFrozenList(open_strings)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_name", type=str)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_frets", type=int)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_strings", type=int)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "finger_to_fret_delta", clean_finger_to_fret_delta)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "clef", type=Clef)
        #Copying to ensure we don't modify the input dic
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_scales_reachable_per_string", IntFrozenList, type=IntFrozenList)
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        assert_typing(self._name, str)
        assert_typing(self.number_of_frets, int)
        assert_typing(self.clef, Clef)
        for finger_for_first_note, dic in self.finger_to_fret_delta.items():
            assert 0<= finger_for_first_note <= 4, f"{finger_for_first_note}"
            for finger_for_next_note, delta in dic.items():
                assert 0 <= finger_for_next_note <= 4, f"{finger_for_next_note}"
                assert finger_for_first_note != finger_for_next_note
                assert_typing(delta, FretDelta)
                assert delta == -self.finger_to_fret_delta[finger_for_next_note][finger_for_first_note]
        assert len(self.number_of_scales_reachable_per_string) == self.number_of_strings
        for number_of_scale in self.number_of_scales_reachable_per_string:
            assert_typing(number_of_scale, int)
            assert 0 <= number_of_scale

        super().__post_init__()