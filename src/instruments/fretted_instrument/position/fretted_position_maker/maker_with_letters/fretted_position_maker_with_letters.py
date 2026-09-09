


from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.positions_consts import CIRCLE_RADIUS, CIRCLE_STROKE_WIDTH, FINGER_LABEL_FONT_SIZE_RATIO, FINGER_LABEL_OFFSET_RATIO, FONT_SIZE
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.constants import BACKGROUND_COLOR, DEFAULT_COLOR
from instruments.fretted_instrument.position.fretted_position_maker.fretted_position_maker import FrettedPositionMaker, FrettedPositionMaker
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position_with_fingers import PositionOnFrettedInstrumentWithFingers
from utils.svg.svg_atom import svg_circle, svg_text


@dataclass(frozen=True)
class FrettedPositionMakerWithLetter(FrettedPositionMaker):
    """A `FrettedPositionMaker` that draws each played position as a circle with a text label inside it (the
    label's content is provided by subclasses via `text`, e.g. a note name or an interval role), plus an
    optional finger-number label for positions that carry fingers."""
    style: Optional[str]#"fill: red;font: italic 12px serif;"
    """Optional inline SVG `style` attribute value applied to the text label(s), e.g. `"fill: red;font: italic 12px serif;"`."""
    circle_color: Optional[str]
    """The outline color of the circle; defaults to `DEFAULT_COLOR` when `None` (see `require_color`)."""
    text_size: int
    """The font size, in SVG units, of the main text label."""

    # def style(self) -> Generator[str]:
    #     if self.color is not None:
    #         yield f".colored {{fill: {self.color} }}"

    def require_color(self):
        """The circle's outline color: `circle_color` if set, otherwise `DEFAULT_COLOR`."""
        if self.circle_color is None:
            return DEFAULT_COLOR
        return self.circle_color

    def svg_lines(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        """Yield the SVG for `pos`: the "not played" marker if `pos` isn't played, otherwise a circle plus the
        `text` label, plus a finger-number label if `pos` is a `PositionOnFrettedInstrumentWithFingers`."""
        if pos.fret.is_not_played():
            yield from pos.string.svg_for_x(pos.fret.absolute)
            return
        x = pos.string.x()
        y = pos.fret.y_dots()
        yield f"""{svg_circle(x, y, int(CIRCLE_RADIUS), BACKGROUND_COLOR, self.require_color(), CIRCLE_STROKE_WIDTH)}<!-- String N° {pos.string.value}, position {pos.fret.value}-->"""
        text = self.text(instrument, pos)
        yield from svg_text(text, x, y, style=self.style, font_size=self.text_size, )
        if isinstance(pos, PositionOnFrettedInstrumentWithFingers):
            finger_x = x + CIRCLE_RADIUS * FINGER_LABEL_OFFSET_RATIO
            finger_y = y + CIRCLE_RADIUS * FINGER_LABEL_OFFSET_RATIO
            finger_font_size = round(self.text_size * FINGER_LABEL_FONT_SIZE_RATIO)
            yield from svg_text(pos.finger_label(), finger_x, finger_y, style=self.style, font_size=finger_font_size)

    def __str__(self) -> str:
        """A short identifier including the tonic's value, used when naming generated files. Note: relies on
        a `tonic` attribute that this class does not itself declare — only meaningful for subclasses (e.g.
        `FrettedPositionMakerForInterval`) that add one; other subclasses must override `__str__`."""
        return f"tonic_{self.tonic.value}"

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `circle_color`/`style` to `None` and `text_size` to `FONT_SIZE`."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        kwargs["circle_color"] = None
        kwargs["style"] = None
        kwargs["text_size"] = FONT_SIZE
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Normalize constructor arguments: make `style`, `circle_color` and `text_size` keyword arguments."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "style")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "circle_color")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "text_size")
        return args, kwargs
    # Must be implemetned by subclasses

    @abstractmethod
    def text(self) -> str:
        """The text label to draw inside the circle for a given position. Implemented by subclasses."""
        ...

