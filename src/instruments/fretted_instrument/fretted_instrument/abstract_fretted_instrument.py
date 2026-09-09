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
    """The tuning-independent characteristics of a family of fretted instruments (e.g. "a guitar", regardless of
    which tuning it is strung with) -- how many frets and strings it has, its clef, and how far apart fingers can
    reasonably be placed. See `FrettedInstrument` for the class that pairs this with an actual `Tuning`."""

    _name: str
    """The instrument family's identifier (e.g. "guitar", "bass", "ukulele"), used to build generated file/folder names."""
    number_of_frets: int
    """How many frets the instrument has (excluding the open/nut position)."""
    clef: Clef
    """The clef notes of this instrument are notated in."""
    number_of_strings: int
    """How many strings the instrument has."""
    finger_to_fret_delta_chord: Dict[int, Dict[int, FretDelta]]=field(compare=False)
    """finger_to_fret_delta_chord[i][j] is the range of fret distances allowed between fingers i and j when
    generating chords (fingers can be spread further apart than when playing a scale, since a chord holds still)."""
    finger_to_fret_delta_scale: Dict[int, Dict[int, FretDelta]]=field(compare=False)
    """Same as `finger_to_fret_delta_chord`, but the range of fret distances allowed between fingers i and j when
    generating scales."""
    number_of_scales_reachable_per_string: IntFrozenList
    """For each string (by index), how many of the generated multi-octave scales are expected to reach it -- used
    to sanity-check scale generation coverage per instrument."""

    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Deep-copy and symmetrize `finger_to_fret_delta_chord`/`finger_to_fret_delta_scale` (deriving delta[j][i]
        as `-delta[i][j]`) and coerce `clef`/`number_of_scales_reachable_per_string` to their expected types."""
        def clean_finger_to_fret_delta(open_strings: Dict[int, Dict[int, FretDelta]]):
            """Deep-copy `open_strings` (a finger-to-finger-to-`FretDelta` mapping, named for the constructor
            argument this coercion is applied to) and fill in the reverse deltas: `[higher][lower]` becomes
            `-delta[lower][higher]` for every finger pair, so callers only need to specify one direction."""
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
            """Coerce a list of open-string notes into a `ChromaticNoteFrozenList`. (Currently unused by any
            constructor argument below.)"""
            return ChromaticNoteFrozenList(open_strings)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_name", type=str)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_frets", type=int)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_strings", type=int)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "finger_to_fret_delta_chord", clean_finger_to_fret_delta)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "finger_to_fret_delta_scale", clean_finger_to_fret_delta)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "clef", type=Clef)
        #Copying to ensure we don't modify the input dic
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_scales_reachable_per_string", IntFrozenList, type=IntFrozenList)
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        """Validate finger/fret-delta ranges are within [0, 4] fingers, symmetric, and that
        `number_of_scales_reachable_per_string` has one non-negative entry per string."""
        assert_typing(self._name, str)
        assert_typing(self.number_of_frets, int)
        assert_typing(self.clef, Clef)
        for finger_for_first_note, dic in self.finger_to_fret_delta_chord.items():
            assert 0<= finger_for_first_note <= 4, f"{finger_for_first_note}"
            for finger_for_next_note, delta in dic.items():
                assert 0 <= finger_for_next_note <= 4, f"{finger_for_next_note}"
                assert finger_for_first_note != finger_for_next_note
                assert_typing(delta, FretDelta)
                assert delta == -self.finger_to_fret_delta_chord[finger_for_next_note][finger_for_first_note]
        assert len(self.number_of_scales_reachable_per_string) == self.number_of_strings
        for number_of_scale in self.number_of_scales_reachable_per_string:
            assert_typing(number_of_scale, int)
            assert 0 <= number_of_scale

        super().__post_init__()