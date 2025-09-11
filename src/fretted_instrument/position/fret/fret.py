from dataclasses import dataclass
import dataclasses
from typing import Dict, Generator, List, Optional, Self, Tuple, Type, Union

from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_optional_typing, assert_typing
from fretted_instrument.position.consts import *

from math import pow

FRET_THICKNESS = 7
TOP_FRET_THICKNESS = FRET_THICKNESS*1.4

@dataclass(frozen=True)
class Fret(ChromaticInterval, DataClassWithDefaultArgument):
    """
    Represents one of the fret of the fretted_instrument.

    None represents a string that is not played and is assumed to be greater than any played string."""
    value: Optional[int]

    def require_value(self):
        """Assert this fret corresponds to a played note."""
        assert self.value is not None
        assert_typing(self.value, int)
        return self.value
    
    @classmethod
    def _make_single_argument(cls, arg: int) -> Self:
        assert_optional_typing(arg, int)
        return cls(arg)

    def name(self):
        if self.value is None:
            return "x"
        return str(self.value)
    
    def is_played(self):
        return isinstance(self.value, int)
    
    def is_open(self):
        return self.value == 0
    
    def is_not_played(self):
        return self.value == None
    
    def is_closed(self):
        return isinstance(self.value, int) and self.value > 0
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "value")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        # not calling super because we accept None value
        #super().__post_init__()
        assert_optional_typing(self.value, int)

    def add(self, instrument: "FrettedInstrument", other: Union[ChromaticInterval, int]) -> Self:
        return self.sub(instrument, -other)
    
    def thickness(self, absolute: bool):
        """The thickness of the fret. If absolute, the 0th fret is bigger to represents the top of the board."""
        if self.require_value() == 0 and absolute:
            return TOP_FRET_THICKNESS
        return FRET_THICKNESS
    
    def __lt__(self, other: "Fret"):
        if self.value is None:
            return False
        if other.value is None:
            return True
        return self.value < other.value
    
    def __eq__(self, other: "Fret"):
        assert_typing(other, Fret)
        return self.value == other.value
    
    def height(self):
        value = self.require_value()
        if value == 0: 
            return 0
        return HEIGHT_OF_FIRST_FRET * pow(RATIO_FRET_HEIGHT, value-1)
    
    def y_fret(self):
        return MARGIN + HEIGHT_OF_FIRST_FRET * ((1-pow(RATIO_FRET_HEIGHT, self.require_value())) / (1-RATIO_FRET_HEIGHT))
    
    def y_dots(self):
        return self.y_fret() - self.height() / 2
    
    def x_dots(self) -> List[float]:
        value = self.require_value()
        if value == 0: 
            return []
        x_one_dot = [WIDTH / 2]
        x_two_dots = [WIDTH /5, 4*WIDTH / 5]
        return {0: x_two_dots, 3: x_one_dot, 5: x_one_dot, 7: x_one_dot, 9:x_one_dot}.get(value % 12, [])

    def fret_svg(self, absolute: bool):
        """Returns the svg for this fret.
        If `absolute`, the 0th one is bigger."""
        y = int(self.y_fret())
        return f"""<line x1="{0}" y1="{y}" x2="{int(WIDTH)}" y2="{y}" stroke-width="{self.thickness(absolute)}" stroke="black" /><!--Fret {self.value}-->"""

    def dot_svg(self, x:float):
        return f"""<circle cx="{int(x)}" cy="{int(self.y_dots())}" r="{int(CIRCLE_RADIUS)}" fill="grey" stroke="black" stroke-width="4"/>"""
    
    def dots_svg(self) -> List[str]:
        return [self.dot_svg(x) for x in self.x_dots()]

    def svg(self, absolute: bool) -> List[str]:
        """The SVG tag for the fret itself. 
        Also, if absolute is true, for the dot that indicate which line it is."""
        l = [self.fret_svg(absolute)]
        if absolute:
            l += self.dots_svg()
        return l

    def all_frets_up_to_here(self, allow_open: bool):
        """The set of all frets up to here."""
        from fretted_instrument.position.fret.frets import Frets
        if self.value in (None, 0):
            closed_fret_interval = None
        else:
            closed_fret_interval = (Fret(1), self.value)
        return Frets.make(closed_fret_interval=closed_fret_interval, allow_open=allow_open)
    
    def transpose(self, transpose: Union[int, ChromaticInterval], transpose_open: bool, transpose_not_played: bool):
        transpose = ChromaticInterval.make_single_argument(transpose)
        if self.is_not_played():
            assert transpose_not_played
            return self
        if not transpose_open and self.is_open():
            return self
        return dataclasses.replace(self, value=self.require_value() + transpose.value)
    
    def __neg__(self):
        # A fret has no inverse value.
        return NotImplemented
    
    def sub(self, instrument: "FrettedInstrument", other: Tuple[ChromaticInterval, int]) -> ChromaticInterval:
        if self.value is None:
            return self
        if isinstance(other, int):
            other = ChromaticInterval(other)
        if not isinstance(other, ChromaticInterval):
            return NotImplemented
        delta = self.value - other.value
        if isinstance(other, Fret):
            return ChromaticInterval(delta)
        
        if delta < 0:
            return None
        if delta > instrument.last_fret().value:
            return None
        if delta > instrument.number_of_frets:
            return None

        return Fret(delta)
    
    def __sub__(self, other):
        raise Exception("Use .sub")