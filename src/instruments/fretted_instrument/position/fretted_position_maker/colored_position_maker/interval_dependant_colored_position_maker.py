
from abc import ABC, abstractmethod
from dataclasses import dataclass
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.colored_position_from_note import Colors
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_typing


@dataclass(frozen=True)
class ColorsWithTonic(Colors, ABC):
    """A `Colors` position-maker whose color choice depends on the note's interval above a fixed `tonic`,
    rather than on the note's absolute pitch."""
    tonic: ChromaticNote
    """The reference note (e.g. the scale/chord root) that colors are computed relative to."""
    #Must be implemented by subclasses

    @abstractmethod
    def get_color_from_interval(self, chromatic_interval: ChromaticInterval) -> str:
        """The color for a note at `chromatic_interval` above `tonic`. Implemented by subclasses."""
        ...
    #pragma mark - dataclass

    def __post_init__(self) -> None:
        """Validate that `tonic` is a `ChromaticNote`."""
        assert_typing(self.tonic, ChromaticNote)

    #Pragma mark Colors

    def __str__(self) -> str:
        """A short identifier for this maker, including the tonic's value, used when naming generated files."""
        return f"{self.__class__.__name__}_with_tonic_{self.tonic.value}"

    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        """The color for `chromatic_note`, computed from its interval above `tonic` via `get_color_from_interval`."""
        assert_typing(chromatic_note, ChromaticNote)
        return self.get_color_from_interval(chromatic_note - self.tonic)