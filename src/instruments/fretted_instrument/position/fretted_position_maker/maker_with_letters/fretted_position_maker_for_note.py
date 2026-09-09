
from dataclasses import dataclass
from typing import Dict, List

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_with_letters import FrettedPositionMakerWithLetter
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from utils.util import assert_typing


@dataclass(frozen=True)
class FrettedPositionMakerForNote(FrettedPositionMakerWithLetter):
    """A `FrettedPositionMakerWithLetter` that labels each position with its absolute note name (e.g. "C#4")
    rather than an interval role."""
    #pragma mark - FrettedPositionMakerForInterval

    def text(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument):
        """The note name (with octave, symbol-style alteration, letter notation, no fixed length) for `pos`'s
        chromatic note."""
        note = pos.get_chromatic()
        return note.get_name_with_octave(
            octave_notation=OctaveOutput.MIDDLE_IS_4, 
            alteration_output=AlterationOutput.SYMBOL,
            note_output=NoteOutput.LETTER,
            fixed_length=FixedLengthOutput.NO,
        )