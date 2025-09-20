from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, List

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.consts import CIRCLE_RADIUS, CIRCLE_STROKE_WIDTH, FONT_SIZE, MARGIN, STROKE_WIDTH
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.svg.svg_atom import svg_circle, svg_text
from utils.util import assert_iterable_typing, assert_typing


COLOR_TONIC = "blue"
COLOR_SECOND = "brown"
COLOR_THIRD = "red"
COLOR_FOURTH = "green"
COLOR_FIFTH = "orange"
COLOR_QUALITY = "purple"
DEFAULT_COLOR = "black"
BACKGROUND_COLOR = "white"


@dataclass(frozen=True)
class FretPositionSvgGenerator(ABC):
    #instrument:FrettedInstrument

    @abstractmethod
    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:...

    @abstractmethod
    def __str__(self) -> str: ...

@dataclass(frozen=True)
class PositionWithIntervalLetters(FretPositionSvgGenerator):
    tonic: ChromaticNote
    
    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        if pos.fret.is_not_played():
            yield from pos.string.svg_for_x(pos.fret.absolute)
            return
        x = pos.string.x()
        y = pos.fret.y_dots()
        note = pos.get_chromatic()
        interval = note - self.tonic
        yield f"""{svg_circle(x, y, int(CIRCLE_RADIUS), BACKGROUND_COLOR, DEFAULT_COLOR, CIRCLE_STROKE_WIDTH)}<!-- String N° {pos.string.value}, position {pos.fret.value}-->"""
        text = ["1", "2m", "2M", "3m", "3M", "4", "T", "5", "6m", "6M", "7m", "7M"][interval.in_base_octave().value]
        yield from svg_text(text, x, y, font_size=FONT_SIZE)

    def __str__(self) -> str:
        return f"tonic_{self.tonic.value}"
    
    def __post_init__(self):
        assert self.tonic.is_in_base_octave(accepting_octave=False)
        


@dataclass(frozen=True)
class Colors(FretPositionSvgGenerator):

    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        stroke_color = self.get_color_from_note(pos.get_chromatic())
        fill_color = "white" if pos.fret.is_open() else (stroke_color)
        if pos.fret.is_not_played():
            yield from pos.string.svg_for_x(pos.fret.absolute)
            return
        x = pos.string.x()
        y = pos.fret.y_dots()
        yield f"""{svg_circle(int(x), int(y), int(CIRCLE_RADIUS), fill_color, stroke_color, STROKE_WIDTH)}<!-- String N° {pos.string.value}, position {pos.fret.value}-->"""


    # Must be implemented by subclasses
    @abstractmethod
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        return NotImplemented

@dataclass(frozen=True)
class BlackOnly(Colors):
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        return DEFAULT_COLOR

    def __str__(self) -> str:
        return "black_only"


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
    

@dataclass(frozen=True)
class ConditionalFretPositionSvgGenerator(FretPositionSvgGenerator):
    colors_for_selected_note: FretPositionSvgGenerator
    selected_notes: ChromaticNoteList
    colors_for_non_selected_notes: FretPositionSvgGenerator

    # pragma mark - Colors

    def __str__(self):
        return f"{self.__class__.__name__}_with_tonic_{self.colors_for_selected_note.tonic}_restricted_to_intervals_[{"_".join(str(interval.value) for interval in self.colored_intervals)}])"
    

    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        colors = self.colors_for_selected_note if pos.get_chromatic().in_base_octave() in self.selected_notes else self.colors_for_non_selected_notes
        return colors.svg_content(instrument, pos)

    # def get_color_from_note(self, chromatic_note: ChromaticNote):
    #     interval = chromatic_note - self.colors.tonic
    #     if interval.in_base_octave() not in self.colored_intervals:
    #         return "black"
    #     return self.colors.get_color_from_interval(interval)
    
    def __post_init__(self):
        assert self.selected_notes.is_in_base_octave()

@dataclass(frozen=True)
class ConditionalFretPositionWithTonicSvgGenerator(FretPositionSvgGenerator):
    colors_for_selected_interval: FretPositionSvgGenerator
    selected_intervals: List[int]
    colors_for_non_selected_intervals: FretPositionSvgGenerator
    tonic: ChromaticNote

    def __post_init__(self):
        assert_typing(self.colors_for_non_selected_intervals, FretPositionSvgGenerator)
        assert_iterable_typing(self.selected_intervals, int)
        assert_typing(self.colors_for_non_selected_intervals, FretPositionSvgGenerator)
        assert_typing(self.tonic, ChromaticNote)

    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        if pos.fret.is_played():
            interval = pos.get_chromatic() - self.tonic if pos.fret.is_played() else None
            colors = self.colors_for_selected_interval if interval.in_base_octave().value in self.selected_intervals else self.colors_for_non_selected_intervals
        else:
            colors = self.colors_for_non_selected_intervals
        yield from colors.svg_content(instrument, pos)
    
    def __str__(self):
        return f"""{str(self.colors_for_selected_interval)}_tonic_{self.tonic.value}_{"-".join(str(interval) for interval in self.selected_intervals)}_{str(self.colors_for_non_selected_intervals)}"""