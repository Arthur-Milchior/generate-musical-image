


from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.consts import CIRCLE_RADIUS, CIRCLE_STROKE_WIDTH, FONT_SIZE
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.constants import BACKGROUND_COLOR, DEFAULT_COLOR
from instruments.fretted_instrument.position.fretted_position_maker.fretted_position_maker import FrettedPositionMaker, FrettedPositionMaker
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from utils.svg.svg_atom import svg_circle, svg_text


@dataclass(frozen=True)
class FrettedPositionMakerWithLetter(FrettedPositionMaker):
    style: Optional[str]#"fill: red;font: italic 12px serif;"
    circle_color: Optional[str]
    text_size: int

    # def style(self) -> Generator[str]:
    #     if self.color is not None:
    #         yield f".colored {{fill: {self.color} }}"

    def require_color(self):
        if self.circle_color is None:
            return DEFAULT_COLOR
        return self.circle_color

    def _svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        if pos.fret.is_not_played():
            yield from pos.string.svg_for_x(pos.fret.absolute)
            return
        x = pos.string.x()
        y = pos.fret.y_dots()
        yield f"""{svg_circle(x, y, int(CIRCLE_RADIUS), BACKGROUND_COLOR, self.require_color(), CIRCLE_STROKE_WIDTH)}<!-- String N° {pos.string.value}, position {pos.fret.value}-->"""
        text = self.text(instrument, pos)
        yield from svg_text(text, x, y, style=self.style, font_size=self.text_size, )

    def __str__(self) -> str:
        return f"tonic_{self.tonic.value}"
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        kwargs["circle_color"] = None
        kwargs["style"] = None
        kwargs["text_size"] = FONT_SIZE
        return kwargs
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "style")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "circle_color")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "text_size")
        return args, kwargs
    # Must be implemetned by subclasses

    @abstractmethod
    def text(self) -> str: ...

