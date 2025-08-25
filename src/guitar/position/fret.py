from dataclasses import dataclass
from typing import Generator, List, Optional, Union

from solfege.interval.chromatic import ChromaticInterval
from utils.util import assert_optional_type, assert_typing
from guitar.position.consts import *

from math import pow

FRET_THICKNESS = 7
TOP_FRET_THICKNESS = FRET_THICKNESS*1.4

@dataclass(frozen=True, eq=True)
class Fret(ChromaticInterval):
    """
    Represents one of the fret of the guitar.

    None represents a string that is not played and is assumed to be greater than any played string."""
    value: Optional[int]

    def require_value(self):
        """Assert this fret corresponds to a played note."""
        assert self.value is not None
        assert_typing(self.value, int)
        return self.value

    def __post_init__(self):
        assert_optional_type(self.value, int)

    def __add__(self, other: Union[ChromaticInterval, int]):
        if self.value is None:
            return self
        if isinstance(other, ChromaticInterval):
            other = other.value
        value = self.value + other
        if value < 0:
            return None
        fret = Fret(value)
        if fret > HIGHEST_FRET:
            return None
        return fret
    
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
    
    def dots_svg(self) -> Generator[str]:
        for x in self.x_dots():
            yield self.dot_svg(x)

    def svg(self, absolute: bool) -> Generator[str]:
        """The SVG tag for the fret itself. 
        Also, if absolute is true, for the dot that indicate which line it is."""
        yield self.fret_svg(absolute) 
        if absolute:
            yield from self.dots_svg()

    def all_frets_up_to_here(self, include_open: bool):
        """The set of all frets up to here."""
        from guitar.position.frets import Frets
        return Frets(1, self.value, True)

    def below(self):
        return Fret(self.require_value() + 1)

    def above(self):
        return Fret(self.require_value() - 1)


NOT_PLAYED = Fret(None)
OPEN_FRET = Fret(0)
HIGHEST_FRET = Fret(24)