
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, List

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_typing


COLOR_TONIC = "blue"
COLOR_SECOND = "brown"
COLOR_THIRD = "red"
COLOR_FOURTH = "green"
COLOR_FIFTH = "orange"
COLOR_QUALITY = "purple"
DEFAUL_COLOR = "black"

@dataclass(frozen=True)
class Colors(ABC):

    # Must be implemented by subclasses
    @abstractmethod
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        return NotImplemented

    @abstractmethod
    def __repr__(self) -> str: ...


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
    
    def __repr__(self) -> str: 
        return f"{self.__class__.__name__}({self.tonic.value})"
    
    def get_color_from_note(self, chromatic_note: ChromaticNote):
        assert_typing(chromatic_note, ChromaticNote)
        return self.get_color_from_interval(chromatic_note - self.tonic)
    

@dataclass(frozen=True)
class RestrictedColorsWithTonic(Colors):
    colors: ColorsWithTonic
    colored_intervals: ChromaticIntervalFrozenList

    # pragma mark - Colors

    def __repr__(self):
        return f"{self.__class__.__name__}({self.colors}, [{", ".join(str(interval.value) for interval in self.colored_intervals)}])"
    
    def get_color_from_note(self, chromatic_note: ChromaticNote):
        interval = chromatic_note - self.colors.tonic
        if interval.in_base_octave() not in self.colored_intervals:
            return "black"
        return self.colors.get_color_from_interval(interval)