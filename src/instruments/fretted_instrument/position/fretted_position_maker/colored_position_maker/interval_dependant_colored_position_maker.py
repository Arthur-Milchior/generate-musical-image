
from abc import ABC, abstractmethod
from dataclasses import dataclass
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.colored_position_from_note import Colors
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_typing


@dataclass(frozen=True)
class ColorsWithTonic(Colors, ABC):
    tonic: ChromaticNote
    #Must be implemented by subclasses

    @abstractmethod
    def get_color_from_interval(self, chromatic_interval: ChromaticInterval) -> str:
        return NotImplemented
    
    #pragma mark - dataclass

    def __post_init__(self):
        assert_typing(self.tonic, ChromaticNote)
    
    #Pragma mark Colors
    
    def __str__(self) -> str: 
        return f"{self.__class__.__name__}_with_tonic_{self.tonic.value}"
    
    def get_color_from_note(self, chromatic_note: ChromaticNote):
        assert_typing(chromatic_note, ChromaticNote)
        return self.get_color_from_interval(chromatic_note - self.tonic)