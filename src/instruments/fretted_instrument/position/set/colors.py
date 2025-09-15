
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_typing


COLOR_TONIC = "red"
COLOR_SECOND = "yellow"
COLOR_THIRD = "blue"
COLOR_FOURTH = "orange"
COLOR_FIFTH = "grey"
COLOR_QUALITY = "green"
COLOR_OTHER = "purple"
COLOR_UNINTERESTING = "black"

@dataclass(frozen=True)
class Colors(ABC):
    # Must be implemented by subclasses

    name: ClassVar[str]

    @abstractmethod
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        return NotImplemented

    def __post_init__(self):
        assert_typing(self.name, str)


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
        super().__post_init__()
    
    #Pragma mark Colors
    
    def get_color_from_note(self, chromatic_note: ChromaticNote):
        assert_typing(chromatic_note, ChromaticNote)
        return self.get_color_from_interval(chromatic_note - self.tonic)
    
