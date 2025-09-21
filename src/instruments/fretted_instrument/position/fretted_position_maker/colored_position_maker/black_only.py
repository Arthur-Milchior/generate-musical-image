from dataclasses import dataclass

from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.colored_position_from_note import Colors
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.constants import DEFAULT_COLOR
from solfege.value.note.chromatic_note import ChromaticNote


@dataclass(frozen=True)
class BlackOnly(Colors):
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        return DEFAULT_COLOR

    def __str__(self) -> str:
        return "black_only"
