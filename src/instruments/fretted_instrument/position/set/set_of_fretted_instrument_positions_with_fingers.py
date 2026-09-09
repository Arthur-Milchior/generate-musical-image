
import dataclasses
from dataclasses import dataclass
from typing import ClassVar, Optional, Self, Type
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentType
from instruments.fretted_instrument.position.fretted_instrument_position_with_fingers import PositionOnFrettedInstrumentWithFingers, FrettedInstrumentPositionWithFingersFrozenList
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.constants import COLOR_FIFTH, DEFAULT_COLOR, COLOR_QUALITY, COLOR_THIRD, COLOR_TONIC
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.interval_dependant_colored_position_maker import ColorsWithTonic
from instruments.fretted_instrument.position.set.abstract_set_of_fretted_instrument_positions import AbstractSetOfFrettedPositions
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.frozenlist import FrozenList
from utils.util import assert_typing

@dataclass(frozen=True, repr=False)
class ScaleColors(ColorsWithTonic):
    #pragma mark - Colors
    name: ClassVar[str] = "scale_colors"

    #pragma mark - ColorsWithTonic
    def get_color_from_interval(self, chromatic_interval: ChromaticInterval):
        color = [COLOR_TONIC, 
         DEFAULT_COLOR, DEFAULT_COLOR,
         COLOR_THIRD, COLOR_THIRD,
         DEFAULT_COLOR,
         COLOR_FIFTH, COLOR_FIFTH, COLOR_FIFTH,
         DEFAULT_COLOR, COLOR_QUALITY, COLOR_QUALITY][chromatic_interval.in_base_octave().value]
        assert_typing(color, str)
        return color
        
@dataclass(frozen=True, eq=False)
class SetOfFrettedInstrumentPositionsWithFingers(AbstractSetOfFrettedPositions[PositionOnFrettedInstrumentWithFingers]):
    """A set of position on the instrument, each position with a finger."""
    type: ClassVar[Type[PositionOnFrettedInstrument]] = PositionOnFrettedInstrumentWithFingers
    _frozen_list_type: ClassVar[Type[FrozenList[PositionOnFrettedInstrumentType]]] = FrettedInstrumentPositionWithFingersFrozenList

    def resolve_fingers(self, instrument: FrettedInstrument) -> Self:
        """Return `self` with each position's candidate `fingers` narrowed to the single finger expected to play it.

        Fingers are chosen along the melodic (chromatic) order of the notes: the lowest candidate finger is picked
        for the first note; each subsequent note is narrowed against the previously chosen finger via
        `PositionOnFrettedInstrumentWithFingers.restrict_to_compatible_fingering` (the same compatibility check the
        scale/arpeggio generator itself uses to build `fingers` in the first place), then the lowest of what
        remains compatible is kept."""
        assert_typing(instrument, FrettedInstrument)
        previous_pos: Optional[PositionOnFrettedInstrumentWithFingers] = None
        new_positions = []
        for pos in self:
            if pos.fret.is_not_played():
                new_positions.append(pos)
                continue
            if previous_pos is not None:
                pos = pos.restrict_to_compatible_fingering(instrument, previous_pos, chord=False)
            resolved_pos = pos.restrict_to_specific_fingers(frozenset({min(pos.fingers)}))
            new_positions.append(resolved_pos)
            previous_pos = resolved_pos
        return dataclasses.replace(self, positions=self._frozen_list_type(new_positions))

    #pragma mark - SvgSaver

    def _svg_name_base(self, **kwargs) -> str:
        # The diagram also displays a finger number on each note (see `resolve_fingers`); make that explicit in the
        # file name so it's unambiguous which images have finger numbers and which don't.
        return f"{super()._svg_name_base(**kwargs)}_with_finger_numbers"

class SetOfFrettedInstrumentPositionsWithFingersFrozenList(FrozenList[SetOfFrettedInstrumentPositionsWithFingers]):
    """A list containing sets of fingered-positions on the instrument."""
    type = SetOfFrettedInstrumentPositionsWithFingers